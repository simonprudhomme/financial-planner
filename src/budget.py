import datetime as dt
import logging
from typing import Union

from src.amount import Amount
from src.entity import FinancialEntity

logger = logging.getLogger(__name__)


class Income(FinancialEntity):
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
        return self.calculate_future_value(date)


class Expense(FinancialEntity):
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
            return self.amount.calculate_future_value(date) * -1
        return self.amount * -1

    def calculate_monthly_cash_flow(self, date: str):
        return self.calculate_future_value(date)
