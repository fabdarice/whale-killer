#!/usr/bin/env python
import datetime
import json
import os
import time

import click
import colored
import requests
from colored import stylize

from holders.ampl import ADDRESSES as AMPL_ADDRESSES
from holders.sta import ADDRESSES as STA_ADDRESSES
from holders.suku import ADDRESSES as SUKU_ADDRESSES

BLOCK_TIME = 15
BLOCK_PER_DAY = 86400 / BLOCK_TIME
API_KEY = os.environ['ETHERSCAN_API_KEY']
ETHERSCAN_API = "https://api.etherscan.io/api"
DELAY_SLEEP_SEC = 0.5


TOP_HOLDERS_MAPPING = {
    'AMPL': AMPL_ADDRESSES,
    'SUKU': SUKU_ADDRESSES,
    'STA': STA_ADDRESSES,
}


@click.command()
@click.option('--token', prompt='The Token Name')
@click.option('--since-block', help='Since X Blocks', default=0)
def main(token: str, since_block: int):
    print(f'Scanning for {token} Whales...')
    latest_block = get_latest_block() - since_block
    top_holders = TOP_HOLDERS_MAPPING[f'{token.upper()}']
    while True:
        for i, account in enumerate(top_holders):
            get_internal_txs(i, account, latest_block, token)
            time.sleep(DELAY_SLEEP_SEC)
        latest_block = get_latest_block() - (
            DELAY_SLEEP_SEC * len(top_holders) / BLOCK_TIME
        )


def get_latest_block() -> int:
    url = f"{ETHERSCAN_API}?module=proxy&action=eth_blockNumber&apikey={API_KEY}"
    resp = requests.get(url)
    hex_block = json.loads(resp.text)["result"]
    return int(hex_block, 16)


def get_internal_txs(i: int, account: str, from_block: int, token: str):
    url = f"{ETHERSCAN_API}?module=account&action=tokentx&address={account}&startblock={from_block}&page=1&offset=50&sort=asc&apikey={API_KEY}"
    resp = requests.get(url)
    json_resp = json.loads(resp.text)
    try:
        ampl_results = [
            result
            for result in json_resp["result"]
            if result["tokenSymbol"] == token
        ]
        if len(ampl_results):
            print(
                "---------------------------------------------------------------------"
            )
            print(
                "---------------------------------------------------------------------"
            )
            print(stylize(f"[#{i}][ACCOUNT : {account}]", colored.attr("bold")))
            for result in ampl_results:
                value = int(result["value"]) / (10 ** int(result["tokenDecimal"]))
                if result["from"] == account:
                    print(
                        stylize(
                            "DANGER - TRANSFER OUT >>>>>>>>>>>>>", colored.fg("red")
                        )
                    )
                    notify("Whale Detected", f"{value} {token}")
                else:
                    print(stylize("TRANSFER IN <<<<<<<<<<<<<<", colored.fg("green")))
                date = datetime.datetime.fromtimestamp(
                    int(result["timeStamp"])
                ).strftime("%Y-%m-%d %H:%M:%S")
                print(f"Timestamp: {date}")
                print(f'Hash: https://etherscan.io/tx/{result["hash"]}')
                print(f"Value: {value} {token} \n")

    except Exception:
        pass


def notify(title, text):
    os.system(
        """
              osascript -e 'display notification "{}" with title "{}"'
              """.format(
            text, title
        )
    )


main()
