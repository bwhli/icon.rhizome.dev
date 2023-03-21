import math
from concurrent.futures import ThreadPoolExecutor
from random import randint
from time import sleep

import requests

TRACKER_API_ENDPOINT = "https://tracker.v2.mainnet.sng.vultr.icon.community/api/v1"


LIMIT = 100


def get_total_tx(url: str):
    r = requests.head(url)
    return int(r.headers["x-total-count"])


def main():
    url = f"{TRACKER_API_ENDPOINT}/transactions?limit=100&skip=0&start_block_number=63367800&end_block_number=63411000"
    total_tx = get_total_tx(url)

    pages = math.ceil(total_tx / LIMIT)

    unique_addresses = set()

    def process(i: int):
        sleep(randint(2, 10) / 5)
        r = requests.get(
            f"{TRACKER_API_ENDPOINT}/transactions?limit={LIMIT}&skip={i * LIMIT}&start_block_number=63367800&end_block_number=63411000"
        )
        r.raise_for_status()
        transactions = r.json()
        for transaction in transactions:
            from_address = transaction["from_address"]
            to_address = transaction["to_address"]
            if from_address != "" and to_address.startswith("cx"):
                unique_addresses.add(from_address)
        print(f"Processed {i}/{pages} pages")
        return

    with ThreadPoolExecutor(max_workers=24) as executor:
        for i in range(pages):
            executor.submit(process, i)

    print(len(unique_addresses))


main()
