#!/usr/bin/env python
import datetime
import json
import os
import time

import colored
import requests
from colored import stylize

BLOCK_TIME = 15
BLOCK_PER_DAY = 86400 / BLOCK_TIME
API_KEY = 'Q1SZ3IFGXFTU4AGSGQ6GQUB5S9KBZIAEG8'
ETHERSCAN_API = 'https://api.etherscan.io/api'
DELAY_SLEEP_SEC = 0.5

TOP_ACCOUNTS = [
    '0xb22ed4bec314d475a8782e0b6869f0144d46859c',
    '0xbdb30cf89efdd8c7410d9b3d0de04bc41b962770',
    '0xf0d611b2610352600f7055e418e547e1c956c046',
    '0x89fe954538a92eca58adaec339ca6374af079a13',
    '0x6723b7641c8ac48a61f5f505ab1e9c03bb44a301',
    '0x7b32ec1a1768cff4a2ef7b34bc1783ee1f8965f9',
    '0x85a07da377a4de02409fa2a05616743f1392bb90',
    '0xa65ce68e9d62a6bb640a567926e215efe5ee11e0',
    '0x3dd9bc86880a0678df824df117dbc7d577c471c4',
    '0x27ce693e2efdf15b0705da999513c9a2403cf064',
    '0x56841730991ca95830fc7a7604bf790127ac362f',
    '0x6206e13b1e6634c76e4e73bcfac51c294cf7520d',
    '0x390aad4274545912d0d4e94c19349c00423c8e36',
    '0x13c210e4a2035446cf02e5b8ac42b6b9a12f8675',
    '0x2f5dcb123fe87bd4e7e14cf0a9345b790091b78e',
    '0x6ac3ca8a477ccf000b8cb648d7d730c8694dfc7b',
    '0x284ab219c9942c614a86a3fa0ca060317f8ef80e',
    '0xd8977d0fc93181057ffe23965a0531e16cbf8d82',
    '0x6ea5b0dda38273bc1816fc6b7df37c7e82f7a658'
]


def main():
    latest_block = get_latest_block() - BLOCK_PER_DAY
    while True:
        for account in TOP_ACCOUNTS:
            get_internal_txs(account, latest_block)
            time.sleep(DELAY_SLEEP_SEC)
        latest_block = get_latest_block() - (DELAY_SLEEP_SEC * len(TOP_ACCOUNTS) / BLOCK_TIME)



def get_latest_block() -> int:
    url = f'{ETHERSCAN_API}?module=proxy&action=eth_blockNumber&apikey={API_KEY}'
    resp = requests.get(url)
    hex_block = json.loads(resp.text)['result']
    return int(hex_block, 16)

def get_internal_txs(account: str, from_block: int):
    url = f'{ETHERSCAN_API}?module=account&action=tokentx&address={account}&startblock={from_block}&page=1&offset=10&sort=asc&apikey={API_KEY}'
    resp = requests.get(url)
    json_resp = json.loads(resp.text)
    ampl_results = [result for result in json_resp['result']
                    if result['tokenSymbol'] == 'AMPL']
    print('---------------------------------------------------------------------')
    print('---------------------------------------------------------------------')
    print(stylize(f'[ACCOUNT : {account}]', colored.attr('bold')))
    for result in ampl_results:
        value = int(result['value']) / (10 ** int(result['tokenDecimal']))
        if result['from'] == account:
            print(stylize('DANGER - TRANSFER OUT >>>>>>>>>>>>>', colored.fg('red')))
            notify('Whale Detected', f'{value} AMPL')
        else:
            print(stylize('TRANSFER IN <<<<<<<<<<<<<<', colored.fg('green')))
        date = datetime.datetime.fromtimestamp(int(result['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S')
        print(f'Timestamp: {date}')
        print(f'Hash: https://etherscan.io/tx/{result["hash"]}')
        # n = notify2.Notification('Whale Detected', f'{value} AMPL', 'notification-message-im')
        # n.show()
        print(f'Value: {value} AMPL \n')

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


main()
