import datetime
import json
import os
import time

import click
import colored
import requests
from colored import stylize
from web3 import Web3

API_KEY = os.environ['ETHERSCAN_API_KEY']
ETHERSCAN_API = "https://api.etherscan.io/api"
CONTRACT_ADDRESS = '0x2129fF6000b95A973236020BCd2b2006B0D8E019'

BLOCK_TIME = 15
BLOCK_PER_HOUR = 3600 / BLOCK_TIME


def get_latest_block() -> int:
    url = f"{ETHERSCAN_API}?module=proxy&action=eth_blockNumber&apikey={API_KEY}"
    resp = requests.get(url)
    hex_block = json.loads(resp.text)["result"]
    return int(hex_block, 16)


@click.command()
@click.option('--minus-hours', help='Minus X Hours', default=0)
def main(minus_hours: str):
    w3 = Web3(Web3.WebsocketProvider('wss://mainnet.infura.io/ws/v3/4773d0d7fed74f2c934eb6dc7f4f16a7'))
    print(w3.isConnected())
    contract_address = Web3.toChecksumAddress(CONTRACT_ADDRESS)

    url = f"{ETHERSCAN_API}?module=contract&action=getabi&address={CONTRACT_ADDRESS}&apikey={API_KEY}"
    resp = requests.get(url)
    json_resp = json.loads(resp.text)
    contract_abi = json_resp['result']
    my_contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    latest_block = get_latest_block() - minus_hours * BLOCK_PER_HOUR

    while True:
        print('.')
        myfilter = my_contract.events.Unfreeze.createFilter(fromBlock=int(latest_block), toBlock='latest')
        event_list = myfilter.get_all_entries()
        for event in event_list:
            print(stylize(f'[UNSTACK][{datetime.datetime.now()}] https://etherscan.io/address/{event["args"]["owner"]}', colored.fg('red')))

        approve_filter = my_contract.events.Approval.createFilter(fromBlock=int(latest_block), toBlock='latest')
        event_list = approve_filter.get_all_entries()
        for event in event_list:
            print(f'[APPROVE][{datetime.datetime.now()}] https://etherscan.io/address/{event["args"]["owner"]}')


        time.sleep(10)
        latest_block = int(get_latest_block())

main()
