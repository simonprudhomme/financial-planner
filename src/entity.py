import datetime as dt
from abc import ABC, abstractmethod


class FinancialEntity(ABC):
    def __init__(self, name, start_date=None, end_date=None):
        self.name = name
        self.start_date = (
            start_date if start_date is not None else dt.date.today().isoformat()
        )
        self.end_date = end_date if end_date is not None else "2999-12-31"

    @abstractmethod
    def check_if_active(self, date: str):
        pass

    @abstractmethod
    def calculate_future_value(self, date: str):
        pass

    @abstractmethod
    def calculate_monthly_cash_flow(self, date: str):
        pass
