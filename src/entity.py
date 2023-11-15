import datetime as dt
from abc import ABC, abstractmethod

import numpy_financial as npf
from dateutil.relativedelta import relativedelta


class FinancialEntity(ABC):
    def __init__(
        self,
        name,
        amount: int,
        annual_inflation_rate: int,
        start_date=None,
        end_date=None,
    ):
        self.name = name
        self.amount = amount
        self.annual_inflation_rate = annual_inflation_rate
        self.start_date = (
            start_date if start_date is not None else dt.date.today().isoformat()
        )
        self.end_date = end_date if end_date is not None else "2999-12-31"

    @abstractmethod
    def is_active_on(self, date: str):
        pass

    @abstractmethod
    def calculate_future_value(self, date: str):
        pass

    @abstractmethod
    def calculate_monthly_cash_flow(self, date: str):
        pass

    @abstractmethod
    def update(self, *arg, **kwarg):
        pass


class Entity(FinancialEntity):
    def __init__(
        self,
        name,
        amount: int,
        annual_inflation_rate: int,
        start_date=None,
        end_date=None,
    ):
        super().__init__(name, amount, annual_inflation_rate, start_date, end_date)

    @property
    def monthly_inflation_rate(self):
        if self.annual_inflation_rate == 0:
            return 0
        return self.annual_inflation_rate / 1200

    def is_active_on(self, date: str):
        return self.start_date <= date <= self.end_date

    def calculate_future_value(self, date: str):
        if self.is_active_on(date) is False:
            return 0
        if self.annual_inflation_rate == 0:
            return self.amount
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.start_date)
        )
        total_months = difference.years * 12 + difference.months
        return npf.fv(
            rate=self.monthly_inflation_rate, nper=total_months, pmt=0, pv=-self.amount
        )

    def calculate_monthly_cash_flow(self, date: str):
        if self.is_active_on(date) is False:
            return 0
        return self.calculate_future_value(date)

    def update(self, amount, annual_inflation_rate, start_date=None, end_date=None):
        name = self.name
        super().__init__(name, amount, annual_inflation_rate, start_date, end_date)
