from dotenv import load_dotenv
from utils.constants import ROOT_DIR

# loading env file
load_dotenv(dotenv_path=ROOT_DIR.joinpath(".env"))

import os
from web3 import Web3

from ethtx import EthTx, EthTxConfig
from ethtx.models.decoded_model import DecodedTransaction


web3 = Web3(Web3.HTTPProvider(os.getenv("ETH_NODE")))

ethtx_config = EthTxConfig(
    mongo_connection_string="mongomock://localhost/ethtx",  ##MongoDB connection string,
    etherscan_api_key="R48UWXJJ48F5VMKI6RXPMAMPMZU9UN9KJ3",  ##Etherscan API key,
    web3nodes={
        "mainnet": {
            "hook": os.getenv("ETH_NODE"),  # multiple nodes supported, separate them with comma
            "poa": False  # represented by bool value
        }
    },
    default_chain="mainnet",
    etherscan_urls={"mainnet": "https://api.etherscan.io/api", },
)

ethtx = EthTx.initialize(ethtx_config)


# w3transaction = web3.eth.get_transaction_receipt('0xecfa50cf0386a9a2494e68004059416898e4297c099086e8b3213f1178cc1695')
transaction: DecodedTransaction = ethtx.decoders.decode_transaction(
    '0xd9cadca34518c443b157ebee5fe4adbb8472646ff4ddd4660ffbbbcf6d9bfa9f')

balances = transaction.balances
print(f"Address {' '*38} NFT {' '*42} Token {' '*10} Balance")
for balance in balances:
    for token in balance.tokens:
        print(f"{balance.holder.address} {' '*2}  {token['token_address'].split('?')[0]} {' '*3} {token['token_symbol']} {' '*6} {token['balance']}")

transfers = transaction.transfers
print(f"Sender {' '*40} Token {' '*10} Amount {' '*10} Receiver")
for transfer in transfers:
    print(f"{transfer.from_address.address} {' '*2}  {transfer.token_symbol} {' '*6} {transfer.value} {' '*6} {transfer.to_address.address}")