import os
import traceback
import time

from dotenv import load_dotenv
from .utils.constants import ROOT_DIR

# loading env file if exists
env = ROOT_DIR.joinpath(".env")
if os.path.isfile(env):
    load_dotenv(dotenv_path=env)
else:
    print("No .env file found")

from ethtx import EthTx, EthTxConfig
from ethtx.models.decoded_model import DecodedTransaction


class Decoder:
    def __init__(self) -> None:
        ethtx_config = EthTxConfig(
            mongo_connection_string="mongomock://localhost/ethtx",  ##MongoDB connection string,
            etherscan_api_key=os.getenv("ETHERSCAN_KEY"),  ##Etherscan API key,
            web3nodes={
                "mainnet": {
                    "hook": os.getenv("GETH_ARCHIVE_NODE"),  # multiple nodes supported, separate them with comma
                    "poa": False  # represented by bool value
                }
            },
            default_chain="mainnet",
            etherscan_urls={"mainnet": "https://api.etherscan.io/api", },
        )

        self.ethtx = EthTx.initialize(ethtx_config)

    def _decode(self, tx_hash: str) -> DecodedTransaction:
        try:
            transaction: DecodedTransaction = self.ethtx.decoders.decode_transaction(tx_hash)
            return transaction
        except Exception:
            return {
                "code": "INTERNAL_SERVER_ERROR",
                "status": False,
                "error": "Internal server error",
                "msg": traceback.format_exc()
            }

    def _parse_address(self, addressInfo):
        return {
            "address": addressInfo.address,
            "name": addressInfo.name,
        }

    def _to_json(self, decodedTransaction: DecodedTransaction):
        if "code" in decodedTransaction and decodedTransaction["code"] == "INTERNAL_SERVER_ERROR":
            return decodedTransaction

        if not decodedTransaction.status:
            return {
                "code": "TRANSACTION_NOT_FOUND",
                "status": decodedTransaction.status,
                "error": "Transaction could not be decoded"
            }
        
        if not decodedTransaction.metadata.success:
            return {
                "code": "TRANSACTION_FAILED",
                "status": decodedTransaction.status,
                "tx_status": decodedTransaction.metadata.success,
                "tx_cost": decodedTransaction.metadata.gas_price * decodedTransaction.metadata.gas_used / pow(10, 9),
                "error": "Transaction failed"
            }

        return {
            "code": "OK",
            "status": decodedTransaction.status,
            "metadata": {
                "block_number": decodedTransaction.metadata.block_number,
                "time_stamp": time.mktime(decodedTransaction.metadata.timestamp.timetuple()),
                "tx_hash": decodedTransaction.metadata.tx_hash,
                "sender": self._parse_address(decodedTransaction.metadata.sender),
                "receiver": self._parse_address(decodedTransaction.metadata.receiver),
                "eth_value": decodedTransaction.metadata.tx_value / pow(10, 18),
                "gas_used": decodedTransaction.metadata.gas_used,
                "gas_price": decodedTransaction.metadata.gas_price,
                "tx_cost": decodedTransaction.metadata.gas_price * decodedTransaction.metadata.gas_used / pow(10, 9),
            },
            "transfers": [
                {
                    "from_address": self._parse_address(o.from_address),
                    "to_address": self._parse_address(o.to_address),
                    "token": 
                    {
                        "token_address": o.token_address.split('?')[0],
                        "token_symbol": o.token_symbol,
                        "token_standard": o.token_standard,
                        "value": o.value
                    }
                }
                for o in decodedTransaction.transfers
            ],
            "balances": [
                {
                    "holder": self._parse_address(o.holder),
                    "tokens": [
                        {
                            "token_address": t["token_address"].split('?')[0],
                            "token_symbol": t["token_symbol"],
                            "token_standard": t["token_standard"],
                            "balance": t["balance"],
                        }
                        for t in o.tokens
                    ]
                }
                for o in decodedTransaction.balances
            ]
        }

    def decode_to_json(self, tx_hash: str):
        decodedTransaction: DecodedTransaction = self._decode(tx_hash)
        return self._to_json(decodedTransaction)