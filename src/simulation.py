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
            print(self.date)
            self.process_month()
            date = dt.date.fromisoformat(self.date) + relativedelta(months=1)
            self.date = date.isoformat()

    def process_month(self):
        # add the current cashflow to the simulation result
        cashflow_ = self.cashflow.calculate_monthly_cash_flow(self.date)
        print(cashflow_)
        print(self.balance.entities["Bank Account"].amount)
        self.balance.entities["Bank Account"].update(
            start_date=self.date, amount=cashflow_
        )

        net_worth = self.balance.calculate_net_worth(self.date)

        self.simulation_result[self.date] = {
            "cashflow": cashflow_,
            "net_worth": net_worth,
        }

    def plot(self, columns=["cashflow", "net_worth"]):
        df = pd.DataFrame.from_dict(self.simulation_result, orient="index")
        df[columns].plot()
        return df
