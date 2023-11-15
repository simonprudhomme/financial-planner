import numpy_financial as npf

from src.entity import FinancialEntity
from src.utils import relativedelta_in_months


class Loan(FinancialEntity):
    def __init__(
        self,
        name,
        principal: int,
        annual_interest_rate: int,
        term_in_year: int,
        annual_inflation_rate: int,
        start_date=None,
        end_date=None,
    ):
        super().__init__(name, principal, annual_inflation_rate, start_date, end_date)

        self.monthly_rate = annual_interest_rate / 1200
        self.periods_in_month = term_in_year * 12
        self.monthly_loan_payment = npf.pmt(
            self.monthly_rate, self.periods_in_month, -self.amount
        )

    @property
    def monthly_inflation_rate(self):
        if self.annual_inflation_rate == 0:
            return 0
        return self.annual_inflation_rate / 1200

    def is_active_on(self, date: str):
        return self.start_date <= date <= self.end_date

    def calculate_future_value(self, date):
        return -self.calculate_remaining_balance_by(date)

    def calculate_monthly_cash_flow(self, date):
        return -self.monthly_loan_payment

    def calculate_interest_paid_by(self, date):
        total_months = relativedelta_in_months(date, self.start_date)
        interest = 0
        for month in range(1, total_months + 1):
            interest += npf.ipmt(
                self.monthly_rate, month, self.periods_in_month, -self.amount
            )
        return interest

    def calculate_principal_paid_by(self, date):
        total_months = relativedelta_in_months(date, self.start_date)
        principal = 0
        for month in range(1, total_months + 1):
            principal += npf.ppmt(
                self.monthly_rate, month, self.periods_in_month, -self.amount
            )
        if principal > self.amount:
            return self.amount
        return principal

    def calculate_remaining_balance_by(self, date):
        total_months = relativedelta_in_months(date, self.start_date)
        remaining_balance = npf.fv(
            self.monthly_rate,
            total_months,
            self.monthly_loan_payment,
            -self.amount,
        )
        if remaining_balance < 0:
            return 0
        return remaining_balance

    def update(self, *arg, **kwarg):
        # return super().update(*arg, **kwarg)
        pass
