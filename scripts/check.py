import requests
from rich import print

SM_ICX_ADDRESS = "hx04ebbde6f4af6638679e37eaf706e6135b81336a"


r = requests.get(
    f"https://tracker.icon.community/api/v1/transactions?limit=100&from={SM_ICX_ADDRESS}"
)
tx = r.json()
print(tx)
