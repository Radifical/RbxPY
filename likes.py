import hashlib
import base64
import json
import time
import os
from requests.exceptions import Timeout
import requests
from dotenv import load_dotenv

load_dotenv()

DATA_STORE_API_KEY = os.getenv("DATA_STORE_API_KEY")
# UNIVERSE ID can be obtained by using https://apis.roblox.com/universes/v1/places/139974381056346/universe
UNIVERSE_ID = 9624826225
DATASTORE_NAME = "likes"  # DATASTORE_NAME and ENTRY_KEY don't require any changes
ENTRY_KEY = "likes"
SCOPE = "global"  # this doesn't require any changes
WAIT_TIME_SECONDS = 300  # 5 minutes

while True:
    time.sleep(WAIT_TIME_SECONDS)  # wait between updates
    # votes response could timeout, will handle this another time
    votes_response = requests.get(
        f"https://games.roblox.com/v1/games/votes?universeIds={UNIVERSE_ID}",
        timeout=60,
        headers={"Accept": "application/json"},
    )
    if votes_response.status_code == 200:
        upvotes = str(votes_response.json()["data"][0]["upVotes"])
        encoded = str.encode(json.dumps(upvotes))
        checksum = hashlib.md5(encoded).digest()
        checksum = base64.b64encode(checksum)
        try:
            datastore_response = requests.post(
                f"https://apis.roblox.com/datastores/v1/universes/{UNIVERSE_ID}/standard-datastores/datastore/entries/entry",
                timeout=60,
                params={
                    "datastoreName": DATASTORE_NAME,
                    "entryKey": ENTRY_KEY,
                    "scope": SCOPE,
                },
                headers={
                    "Content-Type": "application/octet-stream",
                    "content-md5": checksum,
                    "x-api-key": DATA_STORE_API_KEY,
                    "roblox-entry-attributes": "{}",
                },
                data=encoded,
            )
            if datastore_response.status_code != 200:
                print(datastore_response.text, datastore_response.status_code)
        except Timeout:
            print("Request to Roblox Data Store API timed out.")