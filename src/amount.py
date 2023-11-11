import datetime as dt
import numpy_financial as npf
from dateutils import month_start, relativedelta


class Amount:
    def __init__(
        self, value, annual_inflation_rate=0, start_date=dt.date.today().isoformat()
    ):
        self.value = value
        self.value_str = f"$ {self.value:.2f}"
        self.annual_inflation_rate = annual_inflation_rate / 1200
        self.monthly_inflation_rate = (1 + self.annual_inflation_rate) ** (1 / 12) - 1
        self.start_date = start_date

    def calculate_present_value(self, date):
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.start_date)
        )
        total_months = difference.years * 12 + difference.months
        return npf.fv(self.monthly_inflation_rate, total_months, self.value, self.value)
