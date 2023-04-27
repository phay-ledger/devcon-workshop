import requests

SPECULOS_URL="http://127.0.0.1:5042/apdu"


def format_for_nano(simulation: dict[str]) -> str:
    # TODO: parse simulation answer
    return b"(ENS) from maninthecenter.eth\n(ENS) to rektverse.eth"

def build_apdu(msg: str) -> str:
    """ 
        Create apdu encoded string from a given message. 
        Prepend "oracle" to communicate with the ethereum-app loaded in speculos.

        @param msg: insightful message from the transaction simulation
    """

    raw_apdu = bytes.fromhex(
        "058000002c8000003c800000000000000000000000eb808502faf0800082520894fe470ea311dbde1726f467081671e4410aa8952287038d7ea4c6800080018080"
    )

    payload = b"\x01oracle" + len(msg).to_bytes(1, "big") + msg + raw_apdu
    # 4 bytes APDU HEADER
    # CLA (1 byte - E0): Class of instruction, which specifies the type of command and the card type.
    # INS (1 byte - 04): Instruction code, which specifies the operation to be performed.
    # P1 (1 byte - 00): Parameter 1, which is used to provide additional information about the operation.
    # P2 (1 byte - 00): Parameter 2, which is also used to provide additional information about the operation.
    header = "e0040000"
    apdu = bytes.fromhex(header) + len(payload).to_bytes(1, "big") + payload
    return apdu.hex()



def send_to_speculos(simulation: dict):
    message = format_for_nano(simulation)
    encoded_message = build_apdu(message)
    payload = {"data": encoded_message}
    response = requests.post(SPECULOS_URL, json=payload)
    return response.text