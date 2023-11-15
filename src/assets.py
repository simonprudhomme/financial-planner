import datetime as dt
from typing import Optional

import numpy_financial as npf
from dateutil.relativedelta import relativedelta
from loguru import logger

from src.entity import Entity, FinancialEntity
from src.loan import Loan
from src.utils import relativedelta_in_months


class BankAccount(FinancialEntity):
    def __init__(
        self,
        name,
        amount: int,
        annual_inflation_rate: int = 0,
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
        total_months = relativedelta_in_months(date, self.start_date)
        return npf.fv(
            rate=self.monthly_inflation_rate, nper=total_months, pmt=0, pv=-self.amount
        )

    def calculate_monthly_cash_flow(self, date: str):
        return 0

    def update(
        self, amount, annual_inflation_rate=None, start_date=None, end_date=None
    ):
        name = self.name
        annual_inflation_rate = (
            self.annual_inflation_rate
            if annual_inflation_rate is None
            else annual_inflation_rate
        )
        start_date = self.start_date if start_date is None else self.start_date
        amount = self.calculate_future_value(start_date) + amount
        if amount < 0:
            logger.error(f"Bank account {self.name} has a negative balance.")
            raise ValueError
        super().__init__(name, amount, annual_inflation_rate, start_date, end_date)


class Stock(FinancialEntity):
    def __init__(
        self,
        name,
        amount: int,
        annual_expected_return: int,
        start_date=None,
        end_date=None,
    ):
        super().__init__(name, amount, annual_expected_return, start_date, end_date)

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
        total_months = relativedelta_in_months(date, self.start_date)
        return npf.fv(
            rate=self.monthly_inflation_rate, nper=total_months, pmt=0, pv=-self.amount
        )

    def calculate_monthly_cash_flow(self, date: str):
        return 0

    def update(
        self, amount, annual_expected_return=None, start_date=None, end_date=None
    ):
        name = self.name
        annual_inflation_rate = (
            self.annual_inflation_rate
            if annual_expected_return is None
            else annual_expected_return
        )
        start_date = self.start_date if start_date is None else self.start_date
        amount = self.calculate_future_value(start_date) + amount
        if amount < 0:
            logger.error(f"Stock {self.name} has a negative balance.")
            raise ValueError
        super().__init__(name, amount, annual_inflation_rate, start_date, end_date)


class RealEstate(FinancialEntity):
    def __init__(
        self,
        name,
        amount: int,
        cashdown: int,
        annual_expected_return: int,
        loan: Optional[Loan],
        start_date=None,
        end_date=None,
    ):
        super().__init__(name, amount, annual_expected_return, start_date, end_date)
        self.cashdown = cashdown
        self.loan = loan
        self.entities = {}
        if loan:
            self.add_entity(loan)

    @property
    def monthly_inflation_rate(self):
        if self.annual_inflation_rate == 0:
            return 0
        return self.annual_inflation_rate / 1200

    def is_active_on(self, date: str):
        return self.start_date <= date <= self.end_date

    def add_entity(self, entity: Entity):
        self.entities[entity.name] = entity

    # Cashflow
    def calculate_monthly_cash_flow(self, date):
        return sum(
            entity.calculate_monthly_cash_flow(date)
            for entity in self.entities.values()
        )

    # Future value
    def calculate_future_value(self, date):
        total_months = relativedelta_in_months(date, self.start_date)
        return npf.fv(self.monthly_inflation_rate, total_months, 0, -self.amount)

    def update(self):
        pass
