import hashlib
import base64
import json
import time
from requests.exceptions import Timeout
import requests

DATA_STORE_API_KEY = "Eq8X5a5+1ESYaBA2PI/ug65Vud5EHCd9PwHgeb3lb9A3+RXQZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluTnBaeTB5TURJeExUQTNMVEV6VkRFNE9qVXhPalE1V2lJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaGRXUWlPaUpTYjJKc2IzaEpiblJsY201aGJDSXNJbWx6Y3lJNklrTnNiM1ZrUVhWMGFHVnVkR2xqWVhScGIyNVRaWEoyYVdObElpd2lZbUZ6WlVGd2FVdGxlU0k2SWtWeE9GZzFZVFVyTVVWVFdXRkNRVEpRU1M5MVp6WTFWblZrTlVWSVEyUTVVSGRJWjJWaU0yeGlPVUV6SzFKWVVTSXNJbTkzYm1WeVNXUWlPaUl4TlRVME56SXdNelFpTENKbGVIQWlPakUzTmprNE5ETTBOek1zSW1saGRDSTZNVGMyT1Rnek9UZzNNeXdpYm1KbUlqb3hOelk1T0RNNU9EY3pmUS5WbUk3dnBybXlVbktWVXlxcGRkeHd4bk16TjZWbWxMODRNNkhQMmFxQ1F1RWp3TUpjVFpiaDBjUjhZNEJTNWZVcFNlZFVHeWFRY2lFeDh4TFc0Q2ptdXFfZWpQT3hvS0kzMUZITjBtT3RaLU9udVo2NWRsWjBFVloyeGMzV3BNc1BHa1RkNXl5V2lROVNHcEZVd0xrSFg4V2s3NjNUS1pVRFAxYmdqOHhQYVp1Nnd6NmJLRXJYU1VZOE5rc3NFbFBPSk96RTJqQ0NudnRBUG1iNEl2SElmenNaWHlTcHgwVlVRbDVxNWxTOXJDOExUUUdIc0J2QUZiOTlvaU5CNF9kSXFFcFB2UHZJd2FnR2ZraWcxa2hoN2FnbHcxNHlrNHhJY3ZtdU9NOGtzUzdRQVI0Q2pMMUQ1UTZNTW1kQVhRdUI2d2hmMjBST0EtMFRndmIzUk5DZWc="  # don't hardcode in real deployments
UNIVERSE_ID = 9624826225
DATASTORE_NAME = "likes"
ENTRY_KEY = "likes"
SCOPE = "global"
WAIT_TIME_SECONDS = 60  # 5 minutes

SET_ENTRY_URL = (
    f"https://apis.roblox.com/datastores/v1/universes/{UNIVERSE_ID}"
    "/standard-datastores/datastore/entries/entry"
)
VOTES_URL = f"https://games.roblox.com/v1/games/votes?universeIds={UNIVERSE_ID}"

print("hi")
while True:
    print("Starting updater...")
    time.sleep(WAIT_TIME_SECONDS)

    try:
        votes_response = requests.get(
            VOTES_URL,
            timeout=60,
            headers={"Accept": "application/json"},
        )
    except Timeout:
        print("Votes request timed out.")
        continue

    if votes_response.status_code != 200:
        print(votes_response.text, votes_response.status_code)
        continue

    votes_json = votes_response.json()
    upvotes = votes_json["data"][0]["upVotes"]

    payload = {"upVotes": upvotes}
    encoded = json.dumps(payload).encode("utf-8")

    checksum = base64.b64encode(hashlib.md5(encoded).digest()).decode("ascii")

    try:
        datastore_response = requests.post(
            SET_ENTRY_URL,
            timeout=60,
            params={
                "datastoreName": DATASTORE_NAME,
                "entryKey": ENTRY_KEY,
                "scope": SCOPE,
            },
            headers={
                "Content-Type": "application/octet-stream",
                "Content-MD5": checksum,
                "Content-Length": str(len(encoded)),
                "x-api-key": DATA_STORE_API_KEY,
                "roblox-entry-attributes": "{}",
            },
            data=encoded,
        )
        if datastore_response.status_code != 200:
            print(datastore_response.text, datastore_response.status_code)
        else:
            print("Wrote upVotes:", upvotes)
    except Timeout:
        print("Request to Roblox Data Store API timed out.")
