from time import sleep

from piccolo.columns import Varchar
from piccolo.table import Table


class Token(Table):
    name = Varchar(length=100)
    symbol = Varchar(length=10)


import requests

# https://tracker.icon.community/api/v1/transactions?limit=1&to=hx49a23bd156932485471f582897bf1bec5f875751&sort=asc


def get_funder_address(address):
    print(f"Checking {address}...")
    url = f"https://tracker.icon.community/api/v1/transactions?limit=1&to={address}&sort=asc"
    r = requests.get(url)
    data = r.json()
    funder_address = data[0].get("from_address")
    return funder_address


def main():
    address = "hxe5327aade005b19cb18bc993513c5cfcacd159e9"

    while True:
        next_address = get_funder_address(address)

        address = next_address

        sleep(0.5)


main()
