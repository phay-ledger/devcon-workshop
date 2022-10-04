import requests

SPECULOS_URL="http://127.0.0.1:5042/apdu"


def format_for_nano(simulation: dict[str]) -> str:
    # TODO: parse simu answer and only extract balance or idk.  
    return b"salam khouya  <3\npredictive balance = 21 ETH\nj'ai d'autres trucs a dire!!!"

def build_apdu(msg: str) -> str:
    """
        Create apdu encoded string from a given message. 
        Prepend "oracle" to communicate with the ethereum-app loaded in speculos.

        @param msg: insightful message from the transaction simulation
    """
    msg = len(msg).to_bytes(1, "big") + msg
    raw_apdu     = bytes.fromhex(
        "058000002c8000003c800000000000000000000000eb808502faf0800082520894fe470ea311dbde1726f467081671e4410aa8952287038d7ea4c6800080018080"
    )
    payload = b"\x01oracle" + msg + raw_apdu
    apdu = bytes.fromhex("e0040000") + len(payload).to_bytes(1, "big") + payload
    return apdu.hex()



def send_to_speculos(simulation: dict):
    message = format_for_nano(simulation)
    encoded_message = build_apdu(message)
    payload = {"data": encoded_message}
    response = requests.post(SPECULOS_URL, json=payload)
    return response.text