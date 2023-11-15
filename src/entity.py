import datetime as dt
from abc import ABC, abstractmethod
from typing import List, Optional

import numpy_financial as npf
from loguru import logger

from src.utils import relativedelta_in_months


class FinancialEntity(ABC):
    def __init__(
        self,
        name,
        amount: int,
        annual_inflation_rate=None,
        start_date=None,
        end_date=None,
    ):
        self.name = name
        self.amount = amount
        self.annual_inflation_rate = (
            0 if annual_inflation_rate is None else annual_inflation_rate
        )
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
    def update(self, **kwarg):
        pass


class EntityFactory:
    @staticmethod
    def create_entity(entity_type, **kwargs):
        if entity_type == "BankAccount":
            return BankAccount(**kwargs)
        elif entity_type == "Stock":
            return Stock(**kwargs)
        elif entity_type == "RealEstate":
            return RealEstate(**kwargs)
        elif entity_type == "Loan":
            return Loan(**kwargs)
        elif entity_type == "Entity":
            return Entity(**kwargs)
        else:
            raise ValueError(f"Entity type {entity_type} is not supported.")


class Entity(FinancialEntity):
    def __init__(
        self,
        name,
        amount: int,
        annual_inflation_rate=None,
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
        if self.is_active_on(date) is False:
            return 0
        return self.calculate_future_value(date)

    def update(self, **kwargs):
        name = self.name
        super().__init__(name, **kwargs)


class Loan(FinancialEntity):
    def __init__(
        self,
        name,
        amount: int,
        annual_interest_rate: int,
        term_in_year: int,
        annual_inflation_rate=None,
        start_date=None,
        end_date=None,
    ):
        super().__init__(name, amount, annual_inflation_rate, start_date, end_date)

        self.monthly_rate = annual_interest_rate / 1200
        self.periods_in_month = term_in_year * 12

    @property
    def calculate_monthly_payment(self):
        return npf.pmt(self.monthly_rate, self.periods_in_month, -self.amount)

    @property
    def monthly_inflation_rate(self):
        if self.annual_inflation_rate == 0:
            return 0
        return self.annual_inflation_rate / 1200

    def is_active_on(self, date: str):
        return self.start_date <= date <= self.end_date

    def calculate_future_value(self, date):
        if self.is_active_on(date) is False:
            return 0
        return -self.calculate_remaining_balance_by(date)

    def calculate_monthly_cash_flow(self, date):
        if self.is_active_on(date) is False:
            return 0
        return -self.calculate_monthly_payment

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
            self.calculate_monthly_payment,
            -self.amount,
        )
        if remaining_balance < 0:
            return 0
        return remaining_balance

    def update(self, **kwargs):
        name = self.name
        if "annual_interest_rate" in kwargs:
            self.monthly_rate = kwargs["annual_interest_rate"] / 1200
        if "term_in_year" in kwargs:
            self.periods_in_month = kwargs["term_in_year"] * 12
        super().__init__(name, **kwargs)


class BankAccount(FinancialEntity):
    def __init__(
        self,
        name,
        amount: int,
        annual_inflation_rate=None,
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

    def update(self, start_date, **kwargs):
        name = self.name
        amount = self.calculate_future_value(start_date)
        if "amount" in kwargs:
            print(kwargs["amount"])
            amount = self.calculate_future_value(start_date) + kwargs["amount"]
            kwargs.pop("amount")
        super().__init__(name, amount, **kwargs)


class Stock(FinancialEntity):
    def __init__(
        self,
        name,
        amount: int,
        annual_expected_return: int,
        annual_inflation_rate=None,
        start_date=None,
        end_date=None,
    ):
        super().__init__(name, amount, annual_inflation_rate, start_date, end_date)
        self.annual_expected_return = annual_expected_return / 1200

    @property
    def monthly_inflation_rate(self):
        if self.annual_expected_return == 0:
            return 0
        return self.annual_expected_return

    def is_active_on(self, date: str):
        return self.start_date <= date <= self.end_date

    def calculate_future_value(self, date: str):
        if self.is_active_on(date) is False:
            return 0
        if self.annual_expected_return == 0:
            return self.amount
        total_months = relativedelta_in_months(date, self.start_date)
        return npf.fv(
            rate=self.monthly_inflation_rate, nper=total_months, pmt=0, pv=-self.amount
        )

    def calculate_monthly_cash_flow(self, date: str):
        return 0

    def update(self, **kwargs):
        name = self.name
        super().__init__(name, **kwargs)

    def buy(self, amount: int, start_date: str):
        amount = self.calculate_future_value(start_date) + amount
        self.update(amount=amount, start_date=start_date)

    def sell(self, amount: int, start_date: str):
        amount = self.calculate_future_value(start_date) - amount
        if amount < 0:
            logger.error(f"Stock {self.name} has a negative balance.")
            raise ValueError
        self.update(amount=amount, start_date=start_date)


class RealEstate(FinancialEntity):
    def __init__(
        self,
        name,
        amount: int,
        cashdown: int,
        annual_expected_return: int,
        acquisition_costs: Optional[List[Entity]],
        loan: Optional[Loan],
        annual_inflation_rate=None,
        start_date=None,
        end_date=None,
    ):
        super().__init__(name, amount, annual_inflation_rate, start_date, end_date)
        self.cashdown = cashdown
        self.annual_expected_return = annual_expected_return / 1200
        self.loan = loan
        self.entities = {}
        if loan:
            self.add_entity(loan)
        if acquisition_costs:
            for entity in acquisition_costs:
                self.add_entity(entity)

    @property
    def monthly_inflation_rate(self):
        if self.annual_inflation_rate == 0:
            return 0
        return self.annual_inflation_rate

    def is_active_on(self, date: str):
        return self.start_date <= date <= self.end_date

    def add_entity(self, entity: Entity):
        self.entities[entity.name] = entity

    def remove_entity(self, entity: Entity):
        self.entities.pop(entity.name)

    # Cashflow
    def calculate_monthly_cash_flow(self, date):
        return sum(
            entity.calculate_monthly_cash_flow(date)
            for entity in self.entities.values()
        )

    # Future value
    def calculate_future_value(self, date):
        if self.is_active_on(date) is False:
            return 0
        gain = 0
        if self.annual_expected_return != 0:
            total_months = relativedelta_in_months(date, self.start_date)
            gain = npf.fv(self.annual_expected_return, total_months, 0, -self.amount)
        remaining_loan = 0
        if self.loan:
            remaining_loan = self.loan.calculate_future_value(date)
        return gain + remaining_loan

    def update(self, **kwargs):
        if "annual_expected_return" in kwargs:
            self.annual_expected_return = kwargs["annual_expected_return"] / 1200
            kwargs.pop("annual_expected_return")
        if "cashdown" in kwargs:
            self.cashdown = kwargs["cashdown"]
            kwargs.pop("cashflow")
        if "loan" in kwargs:
            self.loan = kwargs["loan"]
            kwargs.pop("loan")
        name = self.name
        super().__init__(name, **kwargs)

    def sell(self, date):
        loan_balance = 0
        if self.loan:
            loan_balance = self.loan.calculate_future_value(date)
        return self.calculate_future_value(date) + loan_balance
