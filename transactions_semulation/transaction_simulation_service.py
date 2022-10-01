import os
import json
import requests
from typing import Optional
from web3 import Web3
from transactions import *


# STEP 0: setup workshop configuration

### NANO EMULATOR URL
SPECULOS_URL="http://127.0.0.1:5042/apdu"


### LEDGER ETH FULLNODE
LEDGER_ETH_ARCHIVE_NODE = os.getenv("NODE_URL")
if not LEDGER_ETH_ARCHIVE_NODE:
    raise Exception("Configuration missing: NODE_URL")
TOKEN = os.getenv("NODE_AUTH")
if not TOKEN:
    raise Exception("Configuration missing: NODE_AUTH")

### Web3 HTTP PROVIDER
HEADER={
    "Authorization": f"Basic {TOKEN}",
    "Content-Type": "application/json"
}
PROVIDER = Web3.HTTPProvider(LEDGER_ETH_ARCHIVE_NODE, request_kwargs={"headers": HEADER})


# STEP 1: Simulate a transaction
def simulate(transaction: dict, block: str = "latest", tracer: str = None) -> Optional[str]:
    """
        Run debug_traceCall EVM primitive to simulate a transaction on a block state trie.
        
        @param transaction: transaction JSON object to simulate. See samples in transaction.py.
        @param block: block number to simulate the transaction in. Default is latest.
        @param tracer: JS tracer to transalated the raw opcodes to intelligble infos. Default is no tracer.
    """

    ethereum_primitive_debug_call = "debug_traceCall"
    tracing_opt = {"tracer": tracer} if tracer else {}
    params = [transaction, block, tracing_opt]
    transaction_simulation = PROVIDER.make_request(ethereum_primitive_debug_call, params)
    return json.dumps(transaction_simulation, indent=1)


# STEP 2: Extract Valuable insight from simulation ouput
def decode_simulation_result(simulation: dict[str]) -> str:
    pass


# STEP 3: Buil APDU from Message to communicate with the Nano simulated with Speculos
def build_apdu(msg: str) -> str:
    """
        Create apdu encoded string from a given message. 
        Prepend "oracle" to communicate with the ethereum-app loaded in speculos.

        @param msg: insightful message from the transaction simulation
    """
    msg = len(msg).to_bytes(1, "big") + msg
    raw_apdu = bytes.fromhex(
        "058000002c8000003c800000000000000000000000eb808502faf0800082520894fe470ea311dbde1726f467081671e4410aa8952287038d7ea4c6800080018080"
    )
    payload = b"\x01oracle" + msg + raw_apdu
    apdu = bytes.fromhex("e0040000") + len(payload).to_bytes(1, "big") + payload
    return apdu


def main():
    raw_op_codes = simulate(aave_deposit)
    # print(raw_op_codes)
    informative_output = simulate(aave_deposit, tracer="callTracer")
    print(informative_output)
    simulation_result = decode_simulation_result(informative_output)
    # apdu_message = build_apdu(simulation_result)
    # requests.post("")


if __name__ == "__main__":
    main()