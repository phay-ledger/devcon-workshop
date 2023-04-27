import os
import json
from typing import Optional
from web3 import Web3
import requests



def _simulate(transaction: dict, block: str = "latest", tracer: str = None) -> Optional[str]:
    """
        Run debug_traceCall EVM primitive to simulate a transaction on a block.
        
        @param transaction: transaction JSON object to simulate. See transaction_samples.py.
        @param block: block number to simulate the transaction in. Default is latest.
        @param tracer: JS tracer to transalated the raw opcodes to intelligble infos. Default is no tracer.
    """

    # get node access from env
    ledger_eth_archive_node = os.getenv("NODE_URL")
    if not ledger_eth_archive_node:
        raise Exception("Configuration missing: NODE_URL")
    token = os.getenv("NODE_AUTH")
    if not token:
        raise Exception("Configuration missing: NODE_AUTH")

    # build web3 provider
    header={
      "Authorization": f"Basic {token}",
      "Content-Type": "application/json"
    }
    provider = Web3.HTTPProvider(ledger_eth_archive_node, request_kwargs={"headers": header})

    # launch the simulation
    ethereum_primitive_debug_call = "debug_traceCall"
    tracing_opt = {"tracer": tracer} if tracer else {}
    params = [transaction, block, tracing_opt]
    transaction_simulation = provider.make_request(ethereum_primitive_debug_call, params)

    return json.dumps(transaction_simulation, indent=1)


def simulate_the_hard_way(transaction, block="latest") -> str:
    return _simulate(transaction, block)

def simulate_with_call_tracer(transaction, block="latest") -> str:
    return _simulate(transaction, block, tracer="callTracer")

def simulate_like_a_boss(transaction: dict, chain_id=1) -> str:
    web3_insight_url = os.getenv("WEB3_INSIGHT_URL", default="http://localhost:3000")
    simulation_endpoint = f"{web3_insight_url}/api/check/transaction"
    transaction["chainId"] = chain_id
    payload = {
	    "includeEvents": True,
	    "includeContracts": True,
	    "transaction": transaction,
	}
    simulation_response = requests.post(simulation_endpoint, json=payload)
    return simulation_response.text


    
