#### File Path: src/simulation.py
 ###import pandas as pd
import datetime as dt
from loguru import logger
from dateutil.relativedelta import relativedelta
from src.cashflow import CashFlow

class Simulation:
    def __init__(self, start_date, duration, cashflow:CashFlow):
        self.start_date = dt.date.fromisoformat(start_date)
        self.current_date = self.start_date
        self.duration = duration
        
        self.cashflow = cashflow
        self.simulation_result = {}
        
        
    def run(self):
        # Main loop for the simulation
        for month in range(self.duration):
            self.process_month()
            self.current_date = self.current_date + relativedelta(months=1)

    def process_month(self):
        # add the current cashflow to the simulation result
        self.simulation_result[self.current_date.isoformat()] = {'cashflow': self.cashflow.calculate_monthly_cash_flow(self.current_date.isoformat())}
        logger.info(f'{self.current_date.isoformat():10} cashflow $ {self.cashflow.calculate_monthly_cash_flow(self.current_date.isoformat()):.2f}')

    def plot(self):
        # plot the simulation result
        df = pd.DataFrame.from_dict(self.simulation_result, orient='index')
        df.plot()
        return df

#### File Path: src/amount.py
 ###from dataclasses import dataclass
import datetime as dt
from dateutil.relativedelta import relativedelta
import numpy_financial as npf
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
        return dt.date.fromisoformat(self.start_date) <= dt.date.fromisoformat(date) <= dt.date.fromisoformat(self.end_date)

    def calculate_future_value(self, date:str):
        if self.check_if_active(date) is False:
            return 0
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.start_date)
        )
        total_months = difference.years * 12 + difference.months
        return npf.fv(
            rate=self.monthly_inflation_rate, nper=total_months, pmt=0, pv=-self.value
        )


#### File Path: src/budget.py
 ###import logging
from typing import Union
import datetime as dt
from src.entity import FinancialEntity
from src.amount import Amount

logger = logging.getLogger(__name__)


class Income(FinancialEntity):
    def __init__(self, name, amount: Union[Amount, int], start_date=None, end_date=None):
        super().__init__(name, start_date, end_date)
        self.amount = amount
        
    def check_if_active(self, date: str):
        return dt.date.fromisoformat(self.start_date) <= dt.date.fromisoformat(date) <= dt.date.fromisoformat(self.end_date)

    def calculate_future_value(self, date: str):
        if self.check_if_active(date) is False:
            return 0
        if isinstance(self.amount, Amount):
            return self.amount.calculate_future_value(date)
        return self.amount

    def calculate_monthly_cash_flow(self, date: str):
        return self.calculate_future_value(date)
    
class Expense(FinancialEntity):
    def __init__(self, name, amount: Union[Amount, int], start_date=None, end_date=None):
        super().__init__(name, start_date, end_date)
        self.amount = amount

    def check_if_active(self, date: str):
        return dt.date.fromisoformat(self.start_date) <= dt.date.fromisoformat(date) <= dt.date.fromisoformat(self.end_date)

    def calculate_future_value(self, date: str):
        if self.check_if_active(date) is False:
            return 0
        if isinstance(self.amount, Amount):
            return self.amount.calculate_future_value(date) * -1
        return self.amount * -1

    def calculate_monthly_cash_flow(self, date: str):
        return self.calculate_future_value(date)

#### File Path: src/loan.py
 ###import datetime as dt

import numpy_financial as npf
from dateutil.relativedelta import relativedelta


class Loan:
    def __init__(
        self,
        name,
        loan_amount,
        annual_rate,
        term_in_year,
        start_date=dt.date.today().isoformat(),
    ):
        self.name = name
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

    def calculate_monthly_cash_flow(self, date: str):
        return -self.calculate_monthly_payment()

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


#### File Path: src/assets.py
 ###import datetime as dt
from loguru import logger
from typing import Optional, Union

import numpy_financial as npf
from dateutil.relativedelta import relativedelta

from src.amount import Amount
from src.loan import Loan
from src.entity import FinancialEntity

class BankAccount(FinancialEntity):
    def __init__(self, name, amount:Union[Amount, int], start_date=None, end_date=None):
        super().__init__(name, start_date, end_date)
        self.amount = amount

    def check_if_active(self, date: str):
        return dt.date.fromisoformat(self.start_date) <= dt.date.fromisoformat(date) <= dt.date.fromisoformat(self.end_date)

    def calculate_future_value(self, date: str):
        if self.check_if_active(date) is False:
            return 0
        if isinstance(self.amount, Amount):
            return self.amount.calculate_future_value(date)
        return self.amount

    def calculate_monthly_cash_flow(self, date: str):
        return 0


class Stock:
    def __init__(
        self,
        name,
        value: int,
        expected_annual_return,
        start_date=dt.date.today().isoformat(),
    ):
        self.name = name
        self.value = value
        self.expected_monthly_return = expected_annual_return / 1200
        self.start_date = start_date

    def calculate_future_value(self, date: str):
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.start_date)
        )
        total_months = difference.years * 12 + difference.months
        return npf.fv(self.expected_monthly_return, total_months, 0, -self.value)

    def calculate_monthly_cash_flow(self, date: str):
        # return 0 as dividends/distribution are not implemented yet
        return 0

    def sell_stock(self, percentage: int, date: str):
        current_value = self.calculate_future_value(date)
        if percentage == 100:
            self.value = 0
            self.start_date = date
            return current_value

        liquidation_value = current_value * percentage / 100
        self.value = current_value - liquidation_value
        self.start_date = date
        return liquidation_value


class RealEstate:
    def __init__(
        self,
        name,
        value,
        cashdown,
        expected_annual_return,
        loan: Loan,
        acquisition_date=dt.date.today().isoformat(),
    ):
        self.name = name
        self.expected_monthly_return = expected_annual_return / 1200
        self.value = value
        self.cashdown = cashdown
        self.loan = Optional[Loan]
        self.monthly_expenses = {}
        self.monthly_incomes = {}

        if loan:
            self.set_monthly_expense("loan", loan)
        self.acquisition_date = acquisition_date

    # Expenses
    def set_monthly_expense(
        self, expense_type: str, monthly_expense: Union[Amount, int]
    ):
        if expense_type in self.monthly_expenses.keys():
            logger.warning(f"Expense type {expense_type} already exists.")
            overwritting = input(
                f"Do you want to overwrite {expense_type} with {monthly_expense}? (y/n)"
            )
            if overwritting == "n":
                return
            logger.info(f"Overwriting {expense_type} with {monthly_expense}")
            self.monthly_expenses[expense_type] = monthly_expense
        self.monthly_expenses[expense_type] = monthly_expense

    def calculate_total_monthly_expenses(self, date):
        total_expenses = 0
        for expense_type in self.monthly_expenses.keys():
            total_expenses += self.monthly_expenses[
                expense_type
            ].calculate_future_value(date)
        return total_expenses

    # Incomes
    def set_monthly_income(self, income_type: str, monthly_income: Union[Amount, int]):
        if income_type in self.monthly_incomes.keys():
            logger.warning(f"Income type {income_type} already exists.")
            overwritting = input(
                f"Do you want to overwrite {income_type} with {monthly_income}? (y/n)"
            )
            if overwritting == "n":
                return
            logger.info(f"Overwriting {income_type} with {monthly_income}")
            self.monthly_incomes[income_type] = monthly_income
        self.monthly_incomes[income_type] = monthly_income

    def calculate_total_monthly_incomes(self, date):
        total_incomes = 0
        for income_type in self.monthly_incomes.keys():
            total_incomes += self.monthly_incomes[income_type].calculate_future_value(
                date
            )
        return total_incomes

    # Cashflow
    def calculate_monthly_cash_flow(self, date):
        return self.calculate_total_monthly_incomes(
            date
        ) - self.calculate_total_monthly_expenses(date)

    def calculate_future_value(
        self, date
    ):  # TODO: need to improve, as this is the real value, but we also want to calculate the equity in the building
        difference = relativedelta(
            dt.date.fromisoformat(date), dt.date.fromisoformat(self.acquisition_date)
        )
        total_months = difference.years * 12 + difference.months
        return npf.fv(self.expected_monthly_return, total_months, 0, -self.value)

    def sell_real_estate(self, date: str):
        current_value = self.calculate_future_value(date)
        self.value = 0
        self.acquisition_date = date
        return current_value


#### File Path: src/entity.py
 ###from abc import ABC, abstractmethod
import datetime as dt

class FinancialEntity(ABC):
    def __init__(self, name, start_date=None, end_date=None):
        self.name = name
        self.start_date = start_date if start_date is not None else dt.date.today().isoformat()
        self.end_date = end_date if end_date is not None else '2999-12-31'

    @abstractmethod
    def calculate_future_value(self, date:str):
        pass

    @abstractmethod
    def calculate_monthly_cash_flow(self, date:str):
        pass


#### File Path: src/cashflow.py
 ###import datetime as dt
from loguru import logger

class CashFlow:
    def __init__(self):
        self.inflows = {}
        self.outflows = {}

    def add_entity(self, entity):
        if entity.calculate_monthly_cash_flow(dt.date.today().isoformat()) > 0:
            self.inflows[entity.name] = entity
        else:
            self.outflows[entity.name] = entity

    def calculate_monthly_cash_flow(self, date: str):
        inflows = 0
        outflows = 0
        for entity in self.inflows.values():
            inflows += entity.calculate_monthly_cash_flow(date)

        for entity in self.outflows.values():
            outflows += entity.calculate_monthly_cash_flow(date)

        return inflows + outflows


#### File Path: src/balance.py
 ###import datetime as dt
from loguru import logger


class Balance:
    def __init__(self):
        self.assets = {}
        self.liabilities = {}

    def add_entity(self, entity):
        if entity.calculate_monthly_cash_flow(dt.date.today().isoformat()) < 0:
            self.liabilities[entity.name] = entity
        else:
            self.assets[entity.name] = entity

