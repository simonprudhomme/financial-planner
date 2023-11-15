import datetime as dt


class CashFlow:
    def __init__(self):
        self.entities = {}

    def add_entity(self, entity):
        self.entities[entity.name] = entity

    def calculate_monthly_cash_flow(self, date):
        return sum(
            entity.calculate_monthly_cash_flow(date)
            for entity in self.entities.values()
        )

    def update(self, *arg, **kwarg):
        pass
