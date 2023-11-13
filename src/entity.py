import datetime as dt
from typing import Union

from src.amount import Amount


class FinancialEntity:
    def __init__(
        self,
        name: str,
        amount: Union[Amount, int],
        start_date=dt.date.today().isoformat(),
    ):
        self.name = name
        self.amount = amount
        self.start_date = start_date

    def calculate_monthly_cash_flow(self, current_date):
        if isinstance(self.amount, Amount):
            return self.amount.calculate_future_value(current_date)
        else:
            return self.amount
