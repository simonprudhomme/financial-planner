import sys

from loguru import logger

from src.balance import Balance
from src.cashflow import CashFlow
from src.simulation import Simulation
from src.variables import ASSETS_LIAIBILITIES, ENTITIES

import os 

# CASHFLOW
cashflow = CashFlow()
for entity in ENTITIES + ASSETS_LIAIBILITIES:
    cashflow.add_entity(entity)

# BALANCE
balance = Balance()

for entity in ASSETS_LIAIBILITIES:
    balance.add_entity(entity)


if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")

    simulation = Simulation(
        start_date="2023-10-01", duration=12 * 10, cashflow=cashflow, balance=balance
    )
    simulation.run()
    simulation.get_results_dataframe(save_to_excel=True)
