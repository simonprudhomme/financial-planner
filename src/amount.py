import datetime as dt
import numpy_financial as npf
from dateutil.relativedelta import relativedelta


class Amount:
    def __init__(
        self, value:int, annual_inflation_rate:int, start_date=dt.date.today().isoformat()
    ):
        self.value = value
        self.monthly_inflation_rate = annual_inflation_rate / 1200
        self.start_date = start_date

    def calculate_future_value(self, date: str):
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.start_date)
        )
        total_months = difference.years * 12 + difference.months
        return npf.fv(rate=self.monthly_inflation_rate,
                      nper=total_months,
                      pmt=0,
                      pv=-self.value)
