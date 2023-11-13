import numpy_financial as npf
import datetime as dt
from dateutil.relativedelta import relativedelta


class Loan:
    def __init__(
        self,
        loan_amount,
        annual_rate,
        term_in_year,
        start_date=dt.date.today().isoformat(),
    ):
        self.loan_amount = loan_amount
        self.monthly_rate = annual_rate / 1200
        self.periods_in_month = term_in_year * 12
        self.start_date = start_date

        self.monthly_loan_payment = npf.pmt(
            self.monthly_rate, self.periods_in_month, -self.loan_amount
        )
        self.monthly_loan_payment_str = f"$ {self.monthly_loan_payment:.2f}"
        
    def calculate_future_value(self, date):
        return npf.pmt(self.monthly_rate, self.periods_in_month, -self.loan_amount)

    def calculate_monthly_payment(self):
        return npf.pmt(self.monthly_rate, self.periods_in_month, -self.loan_amount)

    def calculate_monthly_payment_interest_by_date(self, date):
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.start_date)
        )
        total_months = difference.years * 12 + difference.months
        return npf.ipmt(
            self.monthly_rate, total_months, self.periods_in_month, -self.loan_amount
        )

    def calculate_monthly_payment_principal_by_date(self, date):
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.start_date)
        )
        total_months = difference.years * 12 + difference.months
        return npf.ppmt(
            self.monthly_rate, total_months, self.periods_in_month, -self.loan_amount
        )

    def calculate_total_interest_paid_by_date(self, date):
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.start_date)
        )
        total_months = difference.years * 12 + difference.months
        interest = 0
        for month in range(1, total_months + 1):
            interest += self.calculate_monthly_payment_interest_by_date(month)
        return interest

    def calculate_total_principal_paid_by_date(self, date):
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.start_date)
        )
        total_months = difference.years * 12 + difference.months
        principal = 0
        for month in range(1, total_months + 1):
            principal += self.calculate_monthly_payment_principal_by_date(month)
        return principal

    def calculate_remaining_loan_balance_by_date(self, date):
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.start_date)
        )
        total_months = difference.years * 12 + difference.months
        return npf.fv(
            self.monthly_rate,
            total_months,
            self.monthly_loan_payment,
            -self.loan_amount,
        )
