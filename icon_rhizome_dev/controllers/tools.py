import asyncio
import csv
import io
from datetime import datetime, timezone

import pandas as pd
from pydantic import BaseModel, ValidationError, validator
from rich import print
from starlite import Body, Controller, RequestEncodingType, Template, get, post

from icon_rhizome_dev.balanced import Balanced
from icon_rhizome_dev.balanced.balanced_dex import BalancedDex, BalancedDividendClaim
from icon_rhizome_dev.constants import SM_DISCORD_ADDRESSES
from icon_rhizome_dev.icx_async import IcxAsync
from icon_rhizome_dev.models.icx import IcxTransaction
from icon_rhizome_dev.s3 import S3
from icon_rhizome_dev.tracker import Tracker
from icon_rhizome_dev.utils import Utils


class ToolsController(Controller):
    """
    A controller for routes relating to ICX transactions.
    """

    path = f"/tools"

    class IcxStakingRewardsExporterFormData(BaseModel):
        icxAddress: str
        year: int

        @validator("icxAddress")
        def validate_icx_address(cls, v):
            if v.startswith("hx") and len(v) == 42:
                return v
            else:
                raise ValidationError

    @get(path="/")
    async def get_tools(self) -> Template:
        return Template(
            name="tools/index.html",
            context={
                "title": "ICON Tools",
            },
        )

    @get(path="/address-book/")
    async def get_address_book(self) -> Template:
        return Template(
            name="tools/address_book/index.html",
            context={
                "title": "ICON Tools",
            },
        )

    @get(path="/balanced/dividends/")
    async def get_balanced_dividends(
        self,
        icx_address: str,
        year: int = 2022,
    ) -> None:

        # Get start and end blocks
        year_start_ts = int(datetime(year, 1, 1, tzinfo=timezone.utc).timestamp())
        year_end_ts = int(datetime(year + 1, 1, 1, tzinfo=timezone.utc).timestamp())
        year_start_block = await Tracker.get_block_from_timestamp(year_start_ts, block_number_only=True)  # fmt: skip
        year_end_block = await Tracker.get_block_from_timestamp(year_end_ts, block_number_only=True)  # fmt: skip

        claim_transactions = []

        # Grab some stuff for V2 dividend claims.
        i = 0
        limit = 100
        while True:
            skip = int(i * limit)
            print(f"Scraping tracker API for V1 dividend claims... ({i + 1}/n)")

            transactions = await Tracker.get_transactions(
                from_address=icx_address,
                to_address=Balanced.CONTRACT_BALANCED_DIVIDENDS,
                method="claim",
                start_block_number=year_start_block,
                end_block_number=year_end_block,
                limit=limit,
                skip=skip,
            )

            if transactions is None:
                print(f"No transactions in iteration #{i}. Breaking out of loop!")
                break

            claim_transactions += transactions

            i += 1
            continue

        # Grab some stuff for V2 dividend claims.
        i = 0
        limit = 100
        while True:
            skip = int(i * limit)
            print(f"Scraping tracker API for V2 dividend claims... ({i + 1}/n)")

            transactions = await Tracker.get_transactions(
                from_address=icx_address,
                to_address=Balanced.CONTRACT_BALANCED_DIVIDENDS,
                method="claimDividends",
                start_block_number=year_start_block,
                end_block_number=year_end_block,
                limit=limit,
                skip=skip,
            )

            if transactions is None:
                print(f"No transactions in iteration #{i}. Breaking out of loop!")
                break

            claim_transactions += transactions

            i += 1
            continue

        # Build a list of transaction hashes.
        claim_transaction_hashes = [
            transaction.hash for transaction in claim_transactions
        ]

        print(
            f"Processing {len(claim_transaction_hashes)} dividend claims in {year}..."
        )

        dividend_claims: list[BalancedDividendClaim] = []

        async def _get_dividend_claim(transaction_hash: str) -> None:
            # Get token transfers associated with the transaction.
            token_transfers = await Tracker.get_token_transfers(
                transaction_hash=transaction_hash
            )
            for token_transfer in token_transfers:
                token_price_in_usd = await BalancedDex.get_token_price_in_usd(
                    token_transfer.token_contract_address,
                    token_transfer.block_number,
                )
                dividend_claim = BalancedDividendClaim(
                    contract=token_transfer.token_contract_address,
                    symbol=token_transfer.token_contract_symbol,
                    value=token_transfer.value_decimal,
                    value_in_usd=token_transfer.value_decimal * token_price_in_usd,
                    transaction_hash=token_transfer.transaction_hash,
                    block_number=token_transfer.block_number,
                    timestamp=token_transfer.block_timestamp,
                )
                dividend_claims.append(dividend_claim)
            return

        async with asyncio.TaskGroup() as tg:
            for tx_hash in claim_transaction_hashes:
                tg.create_task(_get_dividend_claim(tx_hash))

        dividend_claims.sort(key=lambda k: k.block_number)

        # Create CSV file.
        header_row = [
            "date",
            "block_number",
            "token_symbol",
            "token_contract",
            "value_claimed",
            "usd_value_claimed",
            "tx_hash",
        ]
        body_rows = [
            [
                dividend_claim.timestamp,
                dividend_claim.block_number,
                dividend_claim.symbol,
                dividend_claim.contract,
                dividend_claim.value,
                dividend_claim.value_in_usd,
                dividend_claim.transaction_hash,
            ]
            for dividend_claim in dividend_claims
        ]
        csv_stringio = Utils.generate_csv_file(header_row, body_rows)

        # Upload file to S3.
        s3 = S3()
        filename = f"reports/balanced-dividend-claims/{icx_address}-balanced-dividend-claims-{year}.csv"  # fmt: skip
        print(f"Uploading {filename} to S3...")
        s3.upload_file(filename, bytes(csv_stringio.getvalue(), encoding="utf-8"))
        print(f"Uploaded {filename} to S3!")

        return f"https://tools-rhizome-dev.s3.us-west-2.amazonaws.com/{filename}"

    @get(path="/cps-treasury-claims/")
    async def get_cps_treasury_claims(self, address: str) -> list:
        claims = await Tracker.get_token_transfers(
            "cxd965531d1cce5daad1d1d3ee1efb39ce68f442fc", address
        )
        return claims

    @post(path="/htmx/icx-staking-rewards-exporter/")
    async def get_tools_htmx_icx_staking_rewards_exporter(
        self,
        data: IcxStakingRewardsExporterFormData = Body(
            media_type=RequestEncodingType.URL_ENCODED
        ),
    ) -> Template:

        whitelisted_addresses = [
            "hx9b402cbf72f713efd6b8d7a709cb6eb7ed7695cd",  # Brian
            "hxdcfe54451c017ecd3efe4becd11bcc7ea1cf252e",  # Andrew
            "hx4a43790d44b07909d20fbcc233548fc80f7a4067",  # RHIZOME
        ]

        whitelisted_addresses = whitelisted_addresses + SM_DISCORD_ADDRESSES

        # Parse form data.
        icx_address = data.icxAddress
        year = data.year

        if icx_address not in whitelisted_addresses:
            is_valid_address = await Tracker.is_approved_voter(icx_address)
            if is_valid_address is False:
                return Template(
                    name="tools/htmx/icx_staking_rewards_exporter/submission_result_invalid_voter.html",
                    context={},
                )

        # Initialize array to hold I-Score claim transaction hashes.
        iscore_claim_transactions = []

        # Get start and end blocks
        year_start_ts = int(datetime(year, 1, 1, tzinfo=timezone.utc).timestamp())
        year_end_ts = int(datetime(year + 1, 1, 1, tzinfo=timezone.utc).timestamp())
        year_start_block = await Tracker.get_block_from_timestamp(year_start_ts, block_number_only=True)  # fmt: skip
        year_end_block = await Tracker.get_block_from_timestamp(year_end_ts, block_number_only=True)  # fmt: skip

        # Grab some stuff for Tracker.
        i = 0
        limit = 100
        while True:
            skip = int(i * limit)

            print(f"Scraping tracker API for I-Score claims... ({i + 1}/n)")
            transactions = await Tracker.get_transactions(
                from_address=icx_address,
                to_address="cx0000000000000000000000000000000000000000",
                method="claimIScore",
                start_block_number=year_start_block,
                end_block_number=year_end_block,
                limit=limit,
                skip=skip,
            )

            if transactions is None:
                break

            for transaction in transactions:
                iscore_claim_transactions.append(transaction)

            i += 1

            continue

        print(f"Processing {len(iscore_claim_transactions)} I-Score claims in {year}...")  # fmt: skip

        async def _generate_iscore_claim_record(transaction: IcxTransaction):
            try:
                block_number = transaction.block_number
                block_timestamp = transaction.block_timestamp / 1000000
                tx_hash = transaction.hash

                iscore_claimed, icx_usd_price = await asyncio.gather(
                    Tracker.get_iscore_claimed(tx_hash),
                    IcxAsync.get_icx_usd_price(block_number),
                )

                transaction_date = datetime.utcfromtimestamp(block_timestamp).isoformat()  # fmt: skip
                icx_claimed = iscore_claimed / 10**18 / 1000
                iscore_claim_record = {
                    "date": transaction_date,
                    "block_number": block_number,
                    "icx_claimed": icx_claimed,
                    "icx_usd_price": icx_usd_price,
                    "usd_value_claimed": icx_claimed * icx_usd_price,
                    "tx_hash": tx_hash,
                }
                print(f"Processed {tx_hash}...")
                return iscore_claim_record
            except Exception as e:
                print(transaction)
                print(e)

        iscore_claims = await asyncio.gather(
            *[
                _generate_iscore_claim_record(transaction)
                for transaction in iscore_claim_transactions
            ]
        )
        iscore_claims.sort(key=lambda k: k["block_number"])

        try:
            header_row = [
                "date",
                "block_number",
                "icx_claimed",
                "icx_usd_price",
                "usd_value_claimed",
                "tx_hash",
            ]
            body_rows = [iscore_claim.values() for iscore_claim in iscore_claims]
            csv_stringio = Utils.generate_csv_file(header_row, body_rows)

            # Initialize S3 class.
            print("Initializing S3 instance...")
            s3 = S3()

            # Upload file to S3.
            filename = f"icx-staking-rewards-reports/{icx_address}-icx-staking-rewards-{year}.csv"  # fmt: skip
            print(f"Uploading {filename} to S3...")
            s3.upload_file(filename, bytes(csv_stringio.getvalue(), encoding="utf-8"))
            print(f"Uploaded {filename} to S3!")

            # Create a dataframe from CSV data.
            df = pd.read_csv(io.StringIO(csv_stringio.getvalue()))
            distribution = df["icx_usd_price"]
            weights = df["icx_claimed"]

            total_icx_claimed = sum([claim["icx_claimed"] for claim in iscore_claims])
            total_usd_claimed = sum(
                [claim["usd_value_claimed"] for claim in iscore_claims]
            )
            average_icx_usd_claim_price = round(
                sum([distribution[i] * weights[i] for i in range(len(distribution))])
                / sum(weights),
                2,
            )

            print(total_icx_claimed, total_usd_claimed, average_icx_usd_claim_price)

            return Template(
                name="tools/htmx/icx_staking_rewards_exporter/submission_result_success.html",
                context={
                    "download_url": f"https://tools-rhizome-dev.s3.us-west-2.amazonaws.com/{filename}",
                    "total_icx_claimed": Utils.fmt(total_icx_claimed),
                    "total_usd_claimed": Utils.fmt(total_usd_claimed),
                    "average_icx_usd_claim_price": Utils.fmt(average_icx_usd_claim_price),  # fmt: skip
                    "year": year,
                },
            )

        except Exception as e:
            print(e)
