from typing import Optional, Union
import datetime as dt
import numpy_financial as npf
from dateutil.relativedelta import relativedelta
from src.loan import Loan
from src.amount import Amount
import logging

logger = logging.getLogger(__name__)


class Stock:
    def __init__(
        self,
        name,
        value:int,
        expected_annual_return,
        start_date=dt.date.today().isoformat(),
    ):
        self.name = name
        self.value = value
        self.expected_monthly_return = expected_annual_return / 1200
        self.start_date = start_date

    def calculate_future_value(self, date:str):
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.start_date)
        )
        total_months = difference.years * 12 + difference.months
        return npf.fv(
            self.expected_monthly_return, total_months, 0, -self.value
        )

    def sell_stock(self, percentage:int, date:str):
        current_value = self.calculate_future_value(date)
        if percentage == 100:
            self.value = 0
            self.start_date = date
            return current_value
        
        liquidation_value = current_value * percentage/100
        self.value = current_value - liquidation_value
        self.start_date = date
        return liquidation_value


class RealEstate:
    def __init__(
        self,
        name,
        value,
        cashdown, 
        expected_annual_return,
        loan: Loan,
        acquisition_date=dt.date.today().isoformat(),
    ):
        self.name = name
        self.expected_monthly_return = expected_annual_return / 1200
        self.value = value
        self.cashdown = cashdown
        self.loan = Optional[Loan]
        self.monthly_expenses = {}
        self.monthly_incomes = {}

        if loan:
            self.set_monthly_expense("loan", loan)
        self.acquisition_date = acquisition_date


    # Expenses
    def set_monthly_expense(self, expense_type: str, monthly_expense: Union[Amount, int]):
        if expense_type in self.monthly_expenses.keys():
            logger.warning(f"Expense type {expense_type} already exists.")
            overwritting = input("Do you want to overwrite? (y/n)")
            if overwritting == "n":
                return
            logger.info(f"Overwriting {expense_type} with {monthly_expense}")
            self.monthly_expenses[expense_type] = monthly_expense
        self.monthly_expenses[expense_type] = monthly_expense
    
    def calculate_total_monthly_expenses(self, date):
        total_expenses = 0
        for expense_type in self.monthly_expenses.keys():
            total_expenses += self.monthly_expenses[expense_type].calculate_future_value(date)
        return total_expenses
    
    # Incomes
    def set_monthly_income(self, income_type: str, monthly_income: Union[Amount, int]):
        if income_type in self.monthly_incomes.keys():
            logger.warning(f"Income type {income_type} already exists.")
            overwritting = input("Do you want to overwrite? (y/n)")
            if overwritting == "n":
                return
            logger.info(f"Overwriting {income_type} with {monthly_income}")
            self.monthly_incomes[income_type] = monthly_income
        self.monthly_incomes[income_type] = monthly_income
 
    def calculate_total_monthly_incomes(self, date):
        total_incomes = 0
        for income_type in self.monthly_incomes.keys():
            total_incomes += self.monthly_incomes[income_type].calculate_future_value(date)
        return total_incomes

    # Cashflow
    def calculate_monthly_cashflow(self, date):
        return self.calculate_total_monthly_incomes(date) - self.calculate_total_monthly_expenses(date)
    
    def calculate_future_value(self, date):
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.acquisition_date)
        )
        total_months = difference.years * 12 + difference.months
        return npf.fv(
            self.expected_monthly_return, total_months, 0, -self.value
        )
        
    def sell_real_estate(self, date:str):
        current_value = self.calculate_future_value(date)
        self.value = 0
        self.acquisition_date = date
        return current_value
