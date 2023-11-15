import datetime as dt
from typing import Optional, Union

import numpy_financial as npf
from dateutil.relativedelta import relativedelta
from loguru import logger

from src.amount import Amount
from src.entity import FinancialEntity
from src.loan import Loan


class BankAccount(FinancialEntity):
    def __init__(
        self, name, amount: Union[Amount, int], start_date=None, end_date=None
    ):
        super().__init__(name, start_date, end_date)
        self.amount = amount

    def check_if_active(self, date: str):
        return (
            dt.date.fromisoformat(self.start_date)
            <= dt.date.fromisoformat(date)
            <= dt.date.fromisoformat(self.end_date)
        )

    def calculate_future_value(self, date: str):
        if self.check_if_active(date) is False:
            return 0
        if isinstance(self.amount, Amount):
            return self.amount.calculate_future_value(date)
        return self.amount

    def calculate_monthly_cash_flow(self, date: str):
        return 0


class Stock(FinancialEntity):
    def __init__(
        self, name, value: int, expected_annual_return, start_date=None, end_date=None
    ):
        super().__init__(name, start_date, end_date)
        self.name = name
        self.value = value
        self.expected_monthly_return = expected_annual_return / 1200
        self.start_date = start_date

    def check_if_active(self, date: str):
        return (
            dt.date.fromisoformat(self.start_date)
            <= dt.date.fromisoformat(date)
            <= dt.date.fromisoformat(self.end_date)
        )

    def calculate_future_value(self, date: str):
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.start_date)
        )
        total_months = difference.years * 12 + difference.months
        return npf.fv(self.expected_monthly_return, total_months, 0, -self.value)

    def calculate_monthly_cash_flow(self, date: str):
        # return 0 as dividends/distribution are not implemented yet
        return 0

    def sell_stock(self, percentage: int, date: str):
        # TODO: need to implement the sell_stock method
        pass


class RealEstate(FinancialEntity):
    def __init__(
        self,
        name,
        value,
        cashdown,
        expected_annual_return,
        loan: Optional[Loan],
        start_date=None,
        end_date=None,
    ):
        super().__init__(name, start_date, end_date)
        self.name = name
        self.expected_monthly_return = expected_annual_return / 1200
        self.value = value
        self.cashdown = cashdown
        self.loan = Optional[Loan]
        self.monthly_expenses = {}
        self.monthly_incomes = {}
        if loan:
            self.set_monthly_expense("loan", loan)

    def check_if_active(self, date: str):
        return (
            dt.date.fromisoformat(self.start_date)
            <= dt.date.fromisoformat(date)
            <= dt.date.fromisoformat(self.end_date)
        )

    # Expenses
    def set_monthly_expense(
        self, expense_type: str, monthly_expense: Union[Amount, int]
    ):
        if expense_type in self.monthly_expenses.keys():
            logger.warning(f"Expense type {expense_type} already exists.")
            logger.info(f"Overwriting {expense_type} with {monthly_expense}")
            self.monthly_expenses[expense_type] = monthly_expense
        self.monthly_expenses[expense_type] = monthly_expense

    def calculate_total_monthly_expenses(self, date):
        total_expenses = 0
        for expense_type in self.monthly_expenses.keys():
            total_expenses += self.monthly_expenses[
                expense_type
            ].calculate_future_value(date)
        return total_expenses

    # Incomes
    def set_monthly_income(self, income_type: str, monthly_income: Union[Amount, int]):
        if income_type in self.monthly_incomes.keys():
            logger.warning(f"Income type {income_type} already exists.")
            logger.info(f"Overwriting {income_type} with {monthly_income}")
            self.monthly_incomes[income_type] = monthly_income
        self.monthly_incomes[income_type] = monthly_income

    def calculate_total_monthly_incomes(self, date):
        total_incomes = 0
        for income_type in self.monthly_incomes.keys():
            total_incomes += self.monthly_incomes[income_type].calculate_future_value(
                date
            )
        return total_incomes

    # Cashflow
    def calculate_monthly_cash_flow(self, date):
        return self.calculate_total_monthly_incomes(
            date
        ) - self.calculate_total_monthly_expenses(date)

    # Equity
    def calculate_equity(self, date):
        # cashdown + appreciation + loan principal paid
        equity = self.cashdown
        equity += self.calculate_future_value(date) - self.value
        if isinstance(self.loan, Loan):
            equity += self.loan.calculate_total_principal_paid_by_date(date)
        return equity

    # Future value
    def calculate_future_value(self, date):
        # TODO: need to improve, as this is the real value, but we also want to calculate the equity in the building
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.start_date)
        )
        total_months = difference.years * 12 + difference.months
        return npf.fv(self.expected_monthly_return, total_months, 0, -self.value)

    def sell_real_estate(self, date: str):
        # TODO: need to implement the sell_real_estate method
        pass
