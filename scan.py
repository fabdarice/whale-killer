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
from holders.ampl import UNISWAP as AMPL_UNISWAP
from holders.lid import ADDRESSES as LID_ADDRESSES
from holders.lid import UNISWAP as LID_UNISWAP
from holders.meta import ADDRESSES as MTA_ADDRESSES
from holders.meta import UNISWAP as MTA_UNISWAP
from holders.myx import ADDRESSES as MYX_ADDRESSES
from holders.myx import UNISWAP as MYX_UNISWAP
from holders.orion import ADDRESSES as ORN_ADDRESSES
from holders.orion import UNISWAP as ORN_UNISWAP
from holders.power import ADDRESSES as POWER_ADDRESSES
from holders.power import UNISWAP as POWER_UNISWAP
from holders.sta import ADDRESSES as STA_ADDRESSES
from holders.sta import UNISWAP as STA_UNISWAP
from holders.suku import ADDRESSES as SUKU_ADDRESSES
from holders.tellor import ADDRESSES as TRB_ADDRESSES
from holders.tellor import UNISWAP as TRB_UNISWAP

BLOCK_TIME = 15
BLOCK_PER_HOUR = 3600 / BLOCK_TIME
BLOCK_PER_DAY = 86400 / BLOCK_TIME
API_KEY = os.environ['ETHERSCAN_API_KEY']
ETHERSCAN_API = "https://api.etherscan.io/api"
DELAY_SLEEP_SEC = 0.5


TOP_HOLDERS_MAPPING = {
    'AMPL': AMPL_ADDRESSES,
    'SUKU': SUKU_ADDRESSES,
    'STA': STA_ADDRESSES,
    'ORN': ORN_ADDRESSES,
    'TRB': TRB_ADDRESSES,
    'MTA': MTA_ADDRESSES,
    'MYX': MYX_ADDRESSES,
    'LID': LID_ADDRESSES,
    'POWER': POWER_ADDRESSES,
}

UNISWAP_MAPPING = {
    'STA': STA_UNISWAP,
    'AMPL': AMPL_UNISWAP,
    'ORN': ORN_UNISWAP,
    'TRB': TRB_UNISWAP,
    'MTA': MTA_UNISWAP,
    'MYX': MYX_UNISWAP,
    'LID': LID_UNISWAP,
    'POWER': POWER_UNISWAP
}


@click.command()
@click.option('--token', prompt='The Token Name')
@click.option('--minus-hours', help='Minus X Hours', default=0)
@click.option('--uniswap-only', help='Only Uniswap From/To', default=True)
def main(token: str, minus_hours: int, uniswap_only: bool):
    print(f'Scanning for {token} Whales...')
    latest_block = get_latest_block() - minus_hours * BLOCK_PER_HOUR
    top_holders = TOP_HOLDERS_MAPPING[f'{token.upper()}']
    while True:
        for i, account in enumerate(top_holders):
            get_internal_txs(i, account, latest_block, token, uniswap_only)
            time.sleep(DELAY_SLEEP_SEC)
        latest_block = get_latest_block() - (
            DELAY_SLEEP_SEC * len(top_holders) / BLOCK_TIME
        )


def get_latest_block() -> int:
    url = f"{ETHERSCAN_API}?module=proxy&action=eth_blockNumber&apikey={API_KEY}"
    resp = requests.get(url)
    hex_block = json.loads(resp.text)["result"]
    return int(hex_block, 16)


def get_internal_txs(i: int, account: str, from_block: int, token: str, uniswap_only: bool):
    url = f"{ETHERSCAN_API}?module=account&action=tokentx&address={account}&startblock={from_block}&page=1&offset=50&sort=asc&apikey={API_KEY}"
    resp = requests.get(url)
    json_resp = json.loads(resp.text)
    try:
        results = [
            result
            for result in json_resp["result"]
            if result["tokenSymbol"] == token and (not uniswap_only or result['to'] == UNISWAP_MAPPING[token] or result['from'] == UNISWAP_MAPPING[token])
        ]
        if len(results):
            print(
                "---------------------------------------------------------------------"
            )
            print(
                "---------------------------------------------------------------------"
            )

            print(stylize(f"[#{i}][ACCOUNT : {account}]", colored.attr("bold")))
            for result in results:

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
