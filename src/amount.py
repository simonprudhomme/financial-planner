import datetime as dt
from dataclasses import dataclass

import numpy_financial as npf
from dateutil.relativedelta import relativedelta
from loguru import logger


@dataclass
class Amount:
    value: int
    annual_inflation_rate: int
    start_date: str = dt.date.today().isoformat()
    end_date: str = "2999-12-31"

    @property
    def monthly_inflation_rate(self):
        return self.annual_inflation_rate / 1200

    def check_if_active(self, date: str):
        return (
            dt.date.fromisoformat(self.start_date)
            <= dt.date.fromisoformat(date)
            <= dt.date.fromisoformat(self.end_date)
        )

    def calculate_future_value(self, date: str):
        if self.check_if_active(date) is False:
            return 0
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.start_date)
        )
        total_months = difference.years * 12 + difference.months
        return npf.fv(
            rate=self.monthly_inflation_rate, nper=total_months, pmt=0, pv=-self.value
        )
