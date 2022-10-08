from transaction_simulation_service import (
    simulate_the_hard_way,
    simulate_with_call_tracer,
    simulate_like_a_boss,
)
from speculos_client import send_to_speculos
from transactions_sample import *



def main():

    unsigned_transaction_payload = ens_transfer

    # STEP 1: Hello World transaction simulation
    raw_op_codes = simulate_the_hard_way(unsigned_transaction_payload)
    print(raw_op_codes)

    # STEP 2: WTF is tracing ??
    print("*" * 50)
    traced_simulation = simulate_with_call_tracer(unsigned_transaction_payload)
    print(traced_simulation)

    # STEP 3: Activable insights from simulation
    print("*" * 50)
    smart_simulation = simulate_like_a_boss(unsigned_transaction_payload)
    print(smart_simulation)

    # STEP 4: Send simulation resut to device emulator
    send_to_speculos(smart_simulation)

    return 0


if __name__ == "__main__":
    main()