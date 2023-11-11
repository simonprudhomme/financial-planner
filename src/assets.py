import datetime as dt
from src.loan import Loan
import numpy_financial as npf
from dateutil import relativedelta


class Stock:
    def __init__(
        self,
        name,
        acquisition_value,
        expected_annual_return,
        acquisition_date=dt.date.today().isoformat(),
    ):
        self.name = name
        self.present_value = acquisition_value
        self.acquisition_date = acquisition_date
        self.expected_annual_return = expected_annual_return
        self.expected_monthly_return = (1 + self.expected_annual_return / 100) ** (
            1 / 12
        ) - 1

        self.liquidation_value = None

    def set_present_value(self, present_value: int):
        self.present_value = present_value

    def get_holding_period_in_month(self, date: dt.date):
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.acquisition_date)
        )
        total_months = difference.years * 12 + difference.months
        return total_months

    def calculate_present_value(self, date: dt.date):
        holding_period = self.get_holding_period_in_month(date)
        return npf.fv(
            self.expected_monthly_return, holding_period, 0, -self.present_value
        )

    def liquidate(self, date: dt.date):
        self.liquidation_value = self.calculate_present_value(date)
        return self.liquidation_value


class RealEstate:
    def __init__(
        self,
        name,
        expected_annual_return,
        acquisition_value,
        cashdown,
        loan: Loan,
        acquisition_date=dt.date.today().isoformat(),
    ):
        self.name = name
        self.expected_annual_return = expected_annual_return
        self.expected_monthly_return = (1 + self.expected_annual_return / 100) ** (
            1 / 12
        ) - 1
        self.present_value = acquisition_value
        self.cashdown = cashdown
        self.loan = loan
        self.acquisition_date = acquisition_date
        self.monthly_expense = {}
        self.monthly_income = {}

    def set_monthly_expense(self, expense_type: str, monthly_expense: int):
        self.monthly_expense[expense_type] = monthly_expense

    def get_monthly_expense(self, expense_type: str):
        return self.monthly_expense[expense_type]

    def get_total_monthly_expense(self):
        return sum(self.monthly_expense.values())

    def set_monthly_income(self, income_type: str, monthly_income: int):
        self.monthly_income[income_type] = monthly_income

    def calculate_monthly_cashflow(self):
        return sum(self.monthly_income.values()) - sum(self.monthly_expense.values())

    def get_holding_period_in_month(self, date):
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.acquisition_date)
        )
        total_months = difference.years * 12 + difference.months
        return total_months

    def calculate_appreciation(self, date):
        holding_period = self.get_holding_period_in_month(date)
        return npf.fv(
            self.expected_monthly_return, holding_period, 0, -self.present_value
        )

    def liquidate(self, date):
        return self.calculate_appreciation(
            date
        ) - self.loan.get_loan_remaining_balance_by_date(date)

    def calculate_equity(self, date):
        return (
            self.loan.calculate_total_principal_paid_by_date(date)
            + self.calculate_appreciation(date)
            - self.loan.get_loan_remaining_balance_by_date(date)
        )
