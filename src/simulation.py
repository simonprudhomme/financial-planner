import datetime as dt
from typing import List, Optional

import matplotlib.pyplot as plt
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
        if self.balance.entities["Bank Account"].amount < 0:
            logger.error(
                f"Bank Account has a negative balance. Date: {self.date}, Amount: {self.balance.entities['Bank Account'].amount}"
            )
            raise ValueError("Bank Account has a negative balance")

        net_worth, net_worth_results = self.balance.calculate_net_worth(self.date)

        self.simulation_result[self.date] = {
            "cashflow": cashflow_results,
            "net_worth": net_worth_results,
        }

    def get_results_json(self):
        return self.simulation_result

    def get_results_dataframe(self, save_to_excel=False):
        # Your JSON data
        data = self.get_results_json()

        # Convert to DataFrame
        cashflow_data = {}
        net_worth_data = {}

        for date, info in data.items():
            cashflow_data[date] = info["cashflow"]
            net_worth_data[date] = info["net_worth"]

        cashflow_df = pd.DataFrame(cashflow_data).T
        net_worth_df = pd.DataFrame(net_worth_data).T

        # Convert index to datetime
        cashflow_df.index.name = "Date"
        net_worth_df.index.name = "Date"

        if save_to_excel:
            # Save the DataFrames to an Excel files
            cashflow_output_file = "results/cashflow_results.xlsx"
            cashflow_df.to_excel(cashflow_output_file)
            print(f"Results saved to {cashflow_output_file}")

            net_worth_output_file = "results/networth_results.xlsx"
            net_worth_df.to_excel(net_worth_output_file)
            print(f"Results saved to {net_worth_output_file}")

        return cashflow_df, net_worth_df

    def plot_results(self):
        cashflow_df, net_worth_df = self.get_results_dataframe()

        cashflow_df["Total Cash Flow"] = cashflow_df.sum(axis=1)
        net_worth_df["Total Net Worth"] = net_worth_df.sum(axis=1)

        # Plot Cash Flow Data
        plt.figure(figsize=(15, 8))
        plt.plot(
            cashflow_df.index, cashflow_df["Total Cash Flow"], label="Total Cash Flow"
        )
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Cash Flow Over Time")

        # Plot Net Worth Data
        plt.figure(figsize=(15, 8))
        plt.plot(
            net_worth_df.index,
            net_worth_df["Total Net Worth"],
            label="Total Net Worth",
            color="green",
        )
        plt.ylim(bottom=0)
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Net Worth Over Time")
