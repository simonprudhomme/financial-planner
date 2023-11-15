#### notebooks/financial-planner.ipynb 
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sys\n",
    "from loguru import logger\n",
    "\n",
    "from src.entity import Entity, EntityFactory, Loan, BankAccount, Stock, RealEstate\n",
    "from src.cashflow import CashFlow\n",
    "from src.balance import Balance\n",
    "from src.simulation import Simulation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "%reload_ext autoreload\n",
    "%autoreload 2"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Assets\n",
    "bank_account = BankAccount(name='Bank Account', amount=10_000, annual_inflation_rate=0)\n",
    "stock = Stock(name='Stocks', amount=450_000, annual_expected_return=7)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Liabilities\n",
    "triplex = RealEstate(name='Triplex', \n",
    "                     amount=500_000, \n",
    "                     cashdown=200_000, \n",
    "                     annual_expected_return=0.05, \n",
    "                     loan=Loan(name='Triplex Loan', amount=300_000, annual_interest_rate=0.03, term_in_year=25, annual_inflation_rate=0))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Budget\n",
    "\n",
    "# Income\n",
    "salary = Entity(name='Salary', amount=10_000, annual_inflation_rate=4)\n",
    "\n",
    "# Expenses\n",
    "rent = Entity(name='Rent', amount=-1200, annual_inflation_rate=4)\n",
    "food = Entity(name='Food', amount=-500, annual_inflation_rate=4)\n",
    "transport = Entity(name='Transport', amount=-200, annual_inflation_rate=4)\n",
    "entertainment = Entity(name='Entertainment', amount=-300, annual_inflation_rate=4)\n",
    "\n",
    "entities = [salary, rent, food, transport, entertainment, bank_account, stock]#, triplex]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Cashflow\n",
    "cashflow = CashFlow()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "for entity in entities:\n",
    "    cashflow.add_entity(entity)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "7800.0"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cashflow.calculate_monthly_cash_flow('2023-12-01')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "({'Salary': <src.entity.Entity at 0x127d1fa00>,\n",
       "  'Bank Account': <src.entity.BankAccount at 0x127cfccd0>,\n",
       "  'Stocks': <src.entity.Stock at 0x127cfc490>},\n",
       " {'Rent': <src.entity.Entity at 0x127d1fd60>,\n",
       "  'Food': <src.entity.Entity at 0x127d1f9d0>,\n",
       "  'Transport': <src.entity.Entity at 0x127d1fd30>,\n",
       "  'Entertainment': <src.entity.Entity at 0x127d1f280>})"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cashflow.inflows, cashflow.outflows"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Balance\n",
    "balance = Balance()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "for entity in entities:\n",
    "    balance.add_entity(entity)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "2129064.768748231"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "balance.calculate_net_worth('2045-11-15')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "10407.415429197907"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "balance.assets['Stocks'].calculate_future_value('2024-11-15')\n",
    "balance.assets['Bank Account'].calculate_future_value('2024-11-15')\n",
    "balance.assets['Salary'].calculate_future_value('2024-11-15')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [],
   "source": [
    "#balance.liabilities['Triplex'].calculate_future_value('2024-11-15')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "505227.5832089276"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "balance.calculate_net_worth('2024-11-15')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "simulation = Simulation(start_date='2024-11-15', duration=12, cashflow=cashflow, balance=balance)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 52,
   "metadata": {},
   "outputs": [],
   "source": [
    "# create entity\n",
    "House = EntityFactory.create_entity('RealEstate', \n",
    "                                   name='House', \n",
    "                                   amount=1_000_000,\n",
    "                                   cashdown= 200_000,\n",
    "                                   annual_expected_return=0,\n",
    "                                   loan=Loan('house_loan',\n",
    "                                             800_000,\n",
    "                                             6,\n",
    "                                             25))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 53,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<src.entity.Entity at 0x163555490>"
      ]
     },
     "execution_count": 53,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "EntityFactory.create_entity(entity_type='Entity',name='house_rent',amount=-100)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 54,
   "metadata": {},
   "outputs": [],
   "source": [
    "House.add_entity(entity=EntityFactory.create_entity(entity_type='Entity',name='house_rent',amount=-100))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 61,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "242599.70447592417"
      ]
     },
     "execution_count": 61,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# update entity\n",
    "House.loan.calculate_principal_paid_by(date='2035-11-15')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'name': 'Stock',\n",
       " 'amount': 131072.0744067345,\n",
       " 'annual_inflation_rate': 0,\n",
       " 'start_date': '2035-11-15',\n",
       " 'end_date': '2999-12-31',\n",
       " 'annual_expected_return': 0.005833333333333334}"
      ]
     },
     "execution_count": 22,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "stock.__dict__"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Actions\n",
    "    - create Entity (using factory)\n",
    "    - update Entity (using entity.update())\n",
    "    - delete Entity (using entity.delete())\n",
    "\n",
    "    - create BankAccount (using factory)\n",
    "    - update BankAccount (using entity.update())\n",
    "    - delete BankAccount (using entity.delete())\n",
    "    - withdraw from BankAccount (using entity.withdraw())\n",
    "    - deposit to BankAccount (using entity.deposit())\n",
    "\n",
    "    - create Stock (using factory)\n",
    "    - update Stock (using entity.update())\n",
    "    - delete Stock (using entity.delete())\n",
    "    - buy Stock (using entity.buy())\n",
    "    - sell Stock (using entity.sell())\n",
    "\n",
    "    - create RealEstate (using factory)\n",
    "    - update RealEstate (using entity.update())\n",
    "    - delete RealEstate (using entity.delete())\n",
    "    - sell RealEstate (using entity.sell())\n",
    "\n",
    "    - invest (excess cashflow in stock) \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "venv",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}


#### notebooks/code-to-text.ipynb 
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import glob"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "# get src file\n",
    "src_files_path = glob.glob(\"notebooks/*.ipynb\") +  glob.glob(\"src/*.py\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "# read src file\n",
    "text = \"\"\n",
    "for file_path in src_files_path:\n",
    "    text += f\"#### {file_path} \\n\"\n",
    "    with open(file_path) as f:\n",
    "        text += f.read()\n",
    "    text += \"\\n\\n\"\n",
    "    \n",
    "# write to OPENAI.md\n",
    "with open(\"OPENAI.md\", \"w\") as f:\n",
    "    f.write(text)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "venv",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}


#### src/simulation.py 
import datetime as dt

import pandas as pd
from dateutil.relativedelta import relativedelta
from loguru import logger

from src.cashflow import CashFlow
from src.balance import Balance


class Simulation:
    def __init__(self, start_date, duration, cashflow: CashFlow, balance: Balance):
        self.start_date = dt.date.fromisoformat(start_date)
        self.current_date = self.start_date
        self.duration = duration

        self.cashflow = cashflow
        self.balance = balance
        self.simulation_result = {}

    def run(self):
        # Main loop for the simulation
        for _ in range(self.duration):
            self.process_month()
            self.current_date = self.current_date + relativedelta(months=1)

    def process_month(self):
        # add the current cashflow to the simulation result
        current_date_ = self.current_date.isoformat()
        cashflow_ = self.cashflow.calculate_monthly_cash_flow(current_date_)
        self.balance.assets['Bank Account'].update(cashflow_)
        balance_ = self.balance.calculate_net_worth(current_date_)
        self.simulation_result[current_date_] = {"cashflow": cashflow_,
                                                 "balance": balance_}

    def plot(self, columns=["cashflow", "balance"]):
        df = pd.DataFrame.from_dict(self.simulation_result, orient="index")
        df[columns].plot()
        return df


#### src/events.py 
from datetime import date
from src.entity import EntityFactory
from typing import Callable


class FinancialEvent:
    def __init__(self, name: str, event_date: date, action: Callable):
        self.name = name
        self.event_date = event_date
        self.action = action

    def execute(self, context):
        self.action(context)
        
    def create_entity(self, **kwargs):
        return EntityFactory.create_entity(entity_type='Entity',**kwargs)


#### src/utils.py 
import datetime as dt

from dateutil.relativedelta import relativedelta

def relativedelta_in_months(date1, date2):
    difference = relativedelta(
        dt.date.fromisoformat(date1), dt.date.fromisoformat(date2)
    )
    return difference.years * 12 + difference.months


#### src/entity.py 
import datetime as dt
from typing import Optional
from abc import ABC, abstractmethod

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
        self.annual_inflation_rate = 0 if annual_inflation_rate is None else annual_inflation_rate
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
        return -self.calculate_remaining_balance_by(date)

    def calculate_monthly_cash_flow(self, date):
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

    def update(self, **kwargs):
        name = self.name
        super().__init__(name, **kwargs)
        
    def deposit(self, amount: int, start_date: str):
        amount = self.calculate_future_value(start_date) + amount
        self.update(amount=amount)

    def withdraw(self, amount: int, start_date: str):
        amount = self.calculate_future_value(start_date) - amount
        if amount < 0:
            logger.error(f"Bank account {self.name} has a negative balance.")
            raise ValueError
        self.update(amount=amount)


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
        if self.annual_expected_return == 0:
            return self.amount
        total_months = relativedelta_in_months(date, self.start_date)
        return npf.fv(self.annual_expected_return, total_months, 0, -self.amount)

    def update(self, **kwargs):
        if 'annual_expected_return' in kwargs:
            self.annual_expected_return = kwargs['annual_expected_return'] / 1200
            kwargs.pop('annual_expected_return')
        if 'cashdown' in kwargs:
            self.cashdown = kwargs['cashdown']
            kwargs.pop('cashflow')
        if 'loan' in kwargs:
            self.loan = kwargs['loan']
            kwargs.pop('loan')
        name = self.name
        super().__init__(name, **kwargs)
        
    def sell(self, date):
        loan_balance = 0
        if self.loan:
            loan_balance = self.loan.calculate_future_value(date)
        return self.calculate_future_value(date) + loan_balance
        

#### src/cashflow.py 
import datetime as dt


class CashFlow:
    def __init__(self):
        self.inflows = {}
        self.outflows = {}

    def add_entity(self, entity):
        if entity.calculate_monthly_cash_flow(dt.date.today().isoformat()) >= 0:
            self.inflows[entity.name] = entity
        else:
            self.outflows[entity.name] = entity

    def calculate_monthly_cash_flow(self, date):
        total_inflows = sum(
            entity.calculate_monthly_cash_flow(date) for entity in self.inflows.values()
        )
        total_outflows = sum(
            entity.calculate_monthly_cash_flow(date)
            for entity in self.outflows.values()
        )
        return total_inflows + total_outflows

    def update(self, *arg, **kwarg):
        pass

    def delete(self, entity_name):
        if entity_name in self.inflows:
            del self.inflows[entity_name]
        elif entity_name in self.outflows:
            del self.outflows[entity_name]
        else:
            raise ValueError("Entity not found")


#### src/balance.py 
import datetime as dt


class Balance:
    def __init__(self):
        self.assets = {}
        self.liabilities = {}

    def add_entity(self, entity):
        if entity.calculate_monthly_cash_flow(dt.date.today().isoformat()) < 0:
            self.liabilities[entity.name] = entity
        else:
            self.assets[entity.name] = entity

    def calculate_net_worth(self, date: str):
        net_worth = 0
        for asset in self.assets.values():
            net_worth += asset.calculate_future_value(date)
        for liability in self.liabilities.values():
            net_worth -= liability.calculate_future_value(date)
        return net_worth

    def update(self, *arg, **kwarg):
        pass


