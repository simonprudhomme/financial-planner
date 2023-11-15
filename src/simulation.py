import datetime as dt

import pandas as pd
from dateutil.relativedelta import relativedelta
from loguru import logger

from src.cashflow import CashFlow


class Simulation:
    def __init__(self, start_date, duration, cashflow: CashFlow):
        self.start_date = dt.date.fromisoformat(start_date)
        self.current_date = self.start_date
        self.duration = duration

        self.cashflow = cashflow
        self.simulation_result = {}

    def run(self):
        # Main loop for the simulation
        for month in range(self.duration):
            self.process_month()
            self.current_date = self.current_date + relativedelta(months=1)

    def process_month(self):
        # add the current cashflow to the simulation result
        current_date_ = self.current_date.isoformat()
        cashflow_ = self.cashflow.calculate_monthly_cash_flow(current_date_)
        self.simulation_result[current_date_] = {"cashflow": cashflow_}
        logger.info(f"{current_date_:10} cashflow $ {cashflow_:.2f}")

    def plot(self):
        # plot the simulation result
        df = pd.DataFrame.from_dict(self.simulation_result, orient="index")
        df.plot()
        return df
