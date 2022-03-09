from flask import Flask
from .decoders import Decoder

app = Flask(__name__)

@app.route("/decode/<tx_hash>", methods=["GET"])
def decode(tx_hash):
    decoder = Decoder()
    decoded_tx = decoder.decode_to_json(tx_hash)
    return decoded_tx