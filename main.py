import sys

from loguru import logger

from src.balance import Balance
from src.cashflow import CashFlow
from src.simulation import Simulation
from src.variables import ASSETS, ENTITIES

# CASHFLOW
cashflow = CashFlow()
for entity in ENTITIES + ASSETS:
    cashflow.add_entity(entity)

# BALANCE
balance = Balance()

for entity in ASSETS:
    balance.add_entity(entity)


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")

    simulation = Simulation(
        start_date="2023-10-01", duration=12 * 10, cashflow=cashflow, balance=balance
    )
    simulation.run()
