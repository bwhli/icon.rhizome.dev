import csv
import json
from datetime import datetime

import requests


def get_block(timestamp: int) -> int:
    r = requests.get(
        f"https://icon.rhizome.dev/api/v1/tools/timestamp-to-block/{timestamp}/"
    )
    data = r.json()
    return data["block"]


def calculate_usd_value(value: str, block_number: int = 0) -> dict:
    r = requests.get(
        f"https://icon.rhizome.dev/api/v1/tools/calculate-usd-value/?value={value}&block_number={block_number}"
    )
    usd_value = r.json()
    return usd_value


SM_ADDRESS = "hx04ebbde6f4af6638679e37eaf706e6135b81336a"

BEN_ADDRESS = "hxe70351dce99ef6bb0573765e541b77ce22409896"
BRIAN_ADDRESS = "hx9b402cbf72f713efd6b8d7a709cb6eb7ed7695cd"
MIKE_ADDRESS = "hxa0d27d26ec39d7e088508f17ef503949a0a85f00"

CRAFT_ESCROW_ADDRESS = "cx9c4698411c6d9a780f605685153431dcda04609f"

LIMIT = 100


START_BLOCK = get_block(1640995200000000)
END_BLOCK = get_block(1672531200000000)


def get_craft_sales():
    internal_transactions = []
    i = 0

    while True:
        skip = int(i * LIMIT)

        url = f"https://tracker.icon.community/api/v1/transactions/internal/address/{SM_ADDRESS}?limit={LIMIT}&skip={skip}&start_block_number={START_BLOCK}&end_block_number={END_BLOCK}"
        r = requests.get(url)

        if r.status_code != 200:
            break

        transactions = r.json()
        for transaction in transactions:

            if (
                transaction["block_timestamp"] < START_BLOCK
                or transaction["block_timestamp"] > END_BLOCK
            ):
                continue

            if transaction["from_address"] == CRAFT_ESCROW_ADDRESS:
                r = requests.get(
                    f"https://icon.rhizome.dev/api/v1/tools/calculate-usd-value/?value={transaction['value']}&block_number={transaction['block_number']}"
                )
                transaction_details = r.json()
                row = [
                    datetime.utcfromtimestamp(
                        transaction["block_timestamp"] / 1_000_000
                    ),  # fmt: skip
                    transaction_details["data"]["icx_value_decimal"],
                    transaction_details["data"]["usd_value"],
                    transaction["hash"],
                ]
                print(row)
                internal_transactions.append(row)

        i += 1

        with open(
            "/Users/brianli/Desktop/2022_craft-sales.csv", mode="w+", newline=""
        ) as f:
            writer = csv.writer(f)
            writer.writerows(sorted(internal_transactions))


def get_contractor_payments(contractor_address: str):
    payments = []

    i = 0

    while True:
        skip = LIMIT * i
        url = f"https://tracker.icon.community/api/v1/transactions?limit={LIMIT}&skip={skip}&to={contractor_address}&from={SM_ADDRESS}&start_block_number={START_BLOCK}&end_block_number={END_BLOCK}"
        print(url)
        r = requests.get(url)

        if r.status_code != 200:
            break

        transactions = r.json()
        for transaction in transactions:
            value_decimal = transaction["value_decimal"]
            if value_decimal > 0:
                block_number = transaction["block_number"]
                tx_value_details = calculate_usd_value(transaction["value"], block_number)  # fmt: skip
                print(tx_value_details)
                row = [
                    datetime.utcfromtimestamp(
                        transaction["block_timestamp"] / 1_000_000
                    ),
                    tx_value_details["data"]["icx_value_decimal"],
                    tx_value_details["data"]["usd_value"],
                    transaction["hash"],
                ]
                payments.append(row)

        i += 1

        with open(
            f"/Users/brianli/Desktop/2022_contractor-payment-{contractor_address}.csv",
            mode="w+",
            newline="",
        ) as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "ICX Amount", "USD Value", "Transaction Hash"])
            writer.writerows(sorted(payments))


def main():
    # get_craft_sales()
    get_contractor_payments(BEN_ADDRESS)
    get_contractor_payments(BRIAN_ADDRESS)
    get_contractor_payments(MIKE_ADDRESS)


if __name__ == "__main__":
    main()
