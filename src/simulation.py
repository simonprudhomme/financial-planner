import datetime as dt
from typing import List, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta
from loguru import logger

from src.balance import Balance
from src.cashflow import CashFlow


class Simulation:
    def __init__(self, start_date, duration, cashflow: CashFlow, balance: Balance):
        self.start_date = start_date
        self.date = self.start_date
        self.duration = duration

        self.cashflow = cashflow
        self.balance = balance
        self.simulation_result = {}

    def run(self):
        # Main loop for the simulation
        for _ in range(self.duration):
            self.process_month()
            date = dt.date.fromisoformat(self.date) + relativedelta(months=1)
            self.date = date.isoformat()

    def process_month(self):
        cashflow, cashflow_results = self.cashflow.calculate_monthly_cash_flow(
            self.date
        )
        self.balance.entities["Bank Account"].update(
            start_date=self.date, amount=cashflow
        )

        net_worth, net_worth_results = self.balance.calculate_net_worth(self.date)

        self.simulation_result[self.date] = {
            "cashflow": cashflow_results,
            "net_worth": net_worth_results,
        }

    def get_results(self):
        return self.simulation_result
