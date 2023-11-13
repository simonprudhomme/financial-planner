from typing import Optional, Union


class Budget:
    def __init__(self):
        self.monthly_income = {}
        self.monthly_expenses = {}

    def set_monthly_income(self, income_type: str, amount: int):
        self.monthly_income[income_type] = amount

    def get_income(self, income_type: Optional[str] = None):
        if income_type is None:
            return self.monthly_income
        else:
            return self.monthly_income[income_type]

    def set_monthly_expense(self, expense_type: str, amount: int):
        self.monthly_expenses[expense_type] = amount

    def get_expense(self, expense_type: Optional[str] = None):
        if expense_type is None:
            return self.monthly_expenses
        else:
            return self.monthly_expenses[expense_type]

    def calculate_monthly_cashflow(self):
        return sum(self.monthly_income.values()) - sum(self.monthly_expenses.values())
