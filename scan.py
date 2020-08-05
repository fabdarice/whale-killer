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
API_KEY = os.environ['ETHERSCAN_API_KEY']
ETHERSCAN_API = "https://api.etherscan.io/api"
DELAY_SLEEP_SEC = 0.5

TOP_SUKU_HOLDERS = [
    "0xc05ec5235ce6050375adce1f86bbec949c3c366f",
    "0x15305250234aabb3246a7f6fb9718ec8964a20a9",
    "0x5348e5a31f5a854954c038a2c4186350e12d6fcb",
    "0x2465163431c6ef3bd27d8107ef84897c1953b163",
    "0x5dda4fc3a71a34dde2ba89d10a45b31a3c45f9b8",
    "0x9b4823a4c0e28b05c2efa898c20c36404c089789",
    "0xe5f114d72e09664afcb97cbc0296a37f36fcd4f4",
    "0x8d9004e297950cac958729153fd7bb707d691338",
    "0xe2fe1af4da9e151a613991d5788bea68d36b8059",
    "0x5ccbb4c11f4ece1e0f45cc19e5a8b534d2d08db9",
    "0x6bf1005a7d99f3d5e1ab2689d7035de24bf4539f",
    "0x34dceb3487614b4f357f548b4a0e58f0e7ba3d93",
    "0x34dceb3487614b4f357f548b4a0e58f0e7ba3d93",
    "0xc1165124be8dc53a3826a1aa1b6643e9138d167c",
    "0xa34868bdd719263aa6552a4a9695c913d303a36c",
    "0x86ddab699a51ad96d7b27036783403a4f04ae1de",
    "0xa310ecfa5dc579d3e397ccc10d28ed24c957be8d",
    "0xee50978c997ec3da572364d0faf983710fc0e9f6",
    "0xef3a1510473fc3b71d8cbb19e3dd0c10a3cabfec",
    "0x0c2e9a64c9382bc2f99b092b3d0c3164375536d3",
    "0x556754785b5428cb5c04b798ea993e5d3c550a66",
    "0x2d1f654a4f797ca6306b819f5c5609eccf3d6025",
    "0x47f6398617cc63c8dbef0d62cf89682e03527721",
    "0xc4603f48cedc5a390919ccdb522f174fa15ea44e",
    "0xc8e4888a1089e1810b3b0f14e24aaa278e518d27",
    "0xe1301695781e2c51cbd972f9db071a333bf9ed31",
    "0x7c5fc7cd37fe26a37150f2f322e48d7cd3c77447",
    "0x7c22ebf158ec2adef19ad746ed4b9ff73fe4a51a",
    "0xf7ebdd1897cde1e8183ab06a4ac94f6481780019",
    "0x05227e4fa98a6415ef1927e902dc781aa7ed518a",
    "0x89621b037cdaf3629ab9aa6079fc0bd77dab46fe",
    "0x3a94e375b2c55b699f336422f9201972681c2f76",
    "0x6537b61e48ce818455426286b2b61fec2f454606",
    "0x0537e9b7fdb0601dcbbef5ab9b2c7d3ce429b663",
]

TOP_AMPL_HOLDERS = [
    "0xb22ed4bec314d475a8782e0b6869f0144d46859c",
    "0xbdb30cf89efdd8c7410d9b3d0de04bc41b962770",
    "0xf0d611b2610352600f7055e418e547e1c956c046",
    "0x89fe954538a92eca58adaec339ca6374af079a13",
    "0x6723b7641c8ac48a61f5f505ab1e9c03bb44a301",
    "0x7b32ec1a1768cff4a2ef7b34bc1783ee1f8965f9",
    "0x85a07da377a4de02409fa2a05616743f1392bb90",
    "0xa65ce68e9d62a6bb640a567926e215efe5ee11e0",
    "0x3dd9bc86880a0678df824df117dbc7d577c471c4",
    '0x30ab95456e89450c6ea568a62f27f844995cf9e6',
    "0x27ce693e2efdf15b0705da999513c9a2403cf064",
    "0x56841730991ca95830fc7a7604bf790127ac362f",
    "0x6206e13b1e6634c76e4e73bcfac51c294cf7520d",
    "0x390aad4274545912d0d4e94c19349c00423c8e36",
    "0x13c210e4a2035446cf02e5b8ac42b6b9a12f8675",
    "0x2f5dcb123fe87bd4e7e14cf0a9345b790091b78e",
    "0x6ac3ca8a477ccf000b8cb648d7d730c8694dfc7b",
    "0x284ab219c9942c614a86a3fa0ca060317f8ef80e",
    "0xd8977d0fc93181057ffe23965a0531e16cbf8d82",
    "0x6ea5b0dda38273bc1816fc6b7df37c7e82f7a658",
    "0xe62ed6862da2cc362dad49f734c13d992a5a97a2",
    "0xb68d3d6103590826749527ea80171253bebf6129",
    "0xd54e46c138c3c84f4b39669cbe15f00697c078e5",
    "0xb60704d2cd7dcd1468675a68f4ec43791ce35ef9",
    "0x320bb16ad49c27825e619a1ce658aeb4bcd68af0",
    "0xc671a41162789649457058c4ee454d6fccd2c44c",
    "0x8f71c90eb559325e5ba23b2323b2e1b7e0e6fe13",
    "0x2d643e9c2dbe4c2878a5b0d15f14b5b40302e5d5",
    "0x274b7950c0b420e112b8b0f53c6fb7b2f1bfe954",
    "0x30f1d1ffad34b24bb8310ad9dd237b854b4daea7",
    "0x83811fdb8c4274d676af222cb9ecd8d63ef55fb4",
    "0x63df7d9d7795883d56ca290f94aba8a6aa4f6f22",
    "0xb18fec1821c05e0c3c692c3abf54af518af7cfe2",
    "0x996d5138843993cebc554c20d82310a43802aff1",
    "0x834e62d799e1ac21114f110c433a85afac36be12",
    "0x630db35a7dfcf53a56551afc86281959525a1f04",
    "0xfd27d5f814c1ce1f7012ba06a2a82d97225689a5",
    "0xf7f742bd5f7148115ac89c6dac568179e787c0e6",
    "0x971da287666762d75eaf70b4772be32e7f322ba2",
    '0xf10a04c222f150455ece627f729b5167d957e360',
    "0x02d48d196b17a04f1ca8ff9a822ceea80793a7ea",
    "0xd7b65068b5ac722626bafb447a00e051427d2dd4",
    "0x8bd3e86bb7470ab48436a8c5ff19a0f6e9121b42",
    "0x3078f22015436d621062f7cc8334774eb5685e97",
    "0xc30a8c89b02180f8c184c1b8e8f76af2b9d8f54d",
    "0x67100ca6a03c4027e0b232f721c26a26222ad1a9",
    "0xd6f0ecf849228358462c90a3e2154d475207d5df",
    "0x15861edaaeeea54addf36ae3cecb004d59de34a9",
    "0xc36c7b93e97d7e36135358e4b0f22e9e25079e87",
    "0x31ca8523ef4ab060085c13d90fcc5f590c2d14ec",
    "0x6cef76e236c6b0990f3a0dbc3a529281d726783c",
    "0xd56911c6ecb072d94584daf55f98014a5d654110",
    "0xfd7cb714a4310b5cd066501c8a566f67e82dc050",
    "0x2baba0cba8241fda56871589835e0b05ec64ca41",
    "0x94ad4001c7a411fa8d55044508170e65ca9f77ca",
    "0x94fdd794037628cda4c6d753abfa53ef8f1a5eb0",
    "0x0e333ad963d52aaae37e1bfa3d13c9d23c6a8850",
    "0x25376209ba75dff0a1ee75006bc3a4f8706ebf4a",
    "0x48e2c14cbc1509570ad1aab71b6292ea40166ac1",
    "0x42629988cdb805f177549d130f8e8afb445e2f2d",
    "0x7b4d5c97dacad35e404ecb970d65ced718df7bee",
    "0x441d7eb8a30af4745ddaba18c7476b393dce9de6",
    "0xa5f6ba5b6e935366eb10628344fde648751663a1",
    "0x68a0ce0a0feba5829e9bbb85bc43a4f3cd62af69",
    "0xfcde8b5fef8b4fbbfd111eb7d20395f66353d71d"
    "0x470487bcb944b0ab2dad52832ba9816eb45f7e40",
    "0x6f3a12d251063b9e06873875044ff5b53ebf0fdb",
    "0x9dfe1a419cf2dfdf8cb48998a8984c014d9192ff",
    "0x2d89d869a187a8775be99e80863eb3973f74bad0",
    '0x0e115a21c34708fda175cc9c924ba42a6d87f95d',
    '0x6d6075b67ea8a9bf2276ec42de689bcc59c2e65e',
    '0x3beaec38ee662b0de92fcb0cfdb31c2eb1b8d164',
    '0x6e6b0c9e77374f6c2cf26fe7fd096b02930e61fe',
    '0x964d9d1a532b5a5daeacbac71d46320de313ae9c',
    '0x0b30483057d6a7798378edba707d625116ed7640',
    '0x18b35d1799385a7548b1c8ed481c5c6ad4921f96',
    '0x37d50885b44500a2eacab7c93dd349590600f05f',
    '0x5701b444dc106089b56ba2193fd7f82234abc2b0',
    '0xf64eff52e524174a0be07beae0322f11ec09a062',
    '0x6ce6e32fcd75373fd59476f8b5122502144825e6',
    '0x94a3c225d8d469eb578a8a81a7301a357807d966',
    '0x706a39f86f174d26c0b5285721fbc48beaa192a0',
]



TOKEN_SYMBOL = "AMPL"
ACCOUNTS = TOP_AMPL_HOLDERS

def main():
    print("Scanning for Whales...")
    latest_block = get_latest_block() - 10
    while True:
        for i, account in enumerate(ACCOUNTS):
            get_internal_txs(i, account, latest_block)
            time.sleep(DELAY_SLEEP_SEC)
        latest_block = get_latest_block() - (
            DELAY_SLEEP_SEC * len(ACCOUNTS) / BLOCK_TIME
        )


def get_latest_block() -> int:
    url = f"{ETHERSCAN_API}?module=proxy&action=eth_blockNumber&apikey={API_KEY}"
    resp = requests.get(url)
    hex_block = json.loads(resp.text)["result"]
    return int(hex_block, 16)


def get_internal_txs(i: int, account: str, from_block: int):
    url = f"{ETHERSCAN_API}?module=account&action=tokentx&address={account}&startblock={from_block}&page=1&offset=50&sort=asc&apikey={API_KEY}"
    resp = requests.get(url)
    json_resp = json.loads(resp.text)
    try:
        ampl_results = [
            result
            for result in json_resp["result"]
            if result["tokenSymbol"] == TOKEN_SYMBOL
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
                    notify("Whale Detected", f"{value} {TOKEN_SYMBOL}")
                else:
                    print(stylize("TRANSFER IN <<<<<<<<<<<<<<", colored.fg("green")))
                date = datetime.datetime.fromtimestamp(
                    int(result["timeStamp"])
                ).strftime("%Y-%m-%d %H:%M:%S")
                print(f"Timestamp: {date}")
                print(f'Hash: https://etherscan.io/tx/{result["hash"]}')
                print(f"Value: {value} {TOKEN_SYMBOL} \n")

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
