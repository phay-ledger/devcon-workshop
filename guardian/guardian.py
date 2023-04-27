import os
import click
from rich import print_json

from transaction_simulation_service import (
    simulate_the_hard_way,
    simulate_with_call_tracer,
    simulate_like_a_boss,
)
from speculos_client import send_to_speculos
from transactions_sample import *


def print_with_delimiter(content, delimiter="*"):
    terminal_width = int(os.getenv("COLUMNS", 100))
    print_json(content)
    print(delimiter * terminal_width)


@click.command()
@click.option("--raw", is_flag=True, help="Run simulation and output raw EVM opcodes")
@click.option("--trace-call", is_flag=True, help="Run simulation and output the smart contracts call trace")
@click.option("--beautiful", is_flag=True, help="Run simulation and output activable insights")
@click.option("--speculos", is_flag=True, help="Print simulation result on the nano device emulator")
def main(raw, trace_call, beautiful, speculos):

    unsigned_transaction_payload = paraswap_thief
    
    if raw:
        # STEP 1: Hello World transaction simulation
        raw_op_codes = simulate_the_hard_way(unsigned_transaction_payload)
        print_with_delimiter(raw_op_codes)
       
    if trace_call:
        # STEP 2: WTF is tracing ?? 
        traced_simulation = simulate_with_call_tracer(unsigned_transaction_payload)
        print_with_delimiter(traced_simulation)

    if beautiful:
        # STEP 3: Activable insights from simulation
        smart_simulation = simulate_like_a_boss(unsigned_transaction_payload)
        print_with_delimiter(smart_simulation)

        if speculos:
            # STEP 4: Send simulation result to speculos
            send_to_speculos(smart_simulation)


if __name__ == "__main__":
    main()