import datetime as dt

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

    def calculate_monthly_cash_flow(self, date):
        total_inflows = sum(
            entity.calculate_monthly_cash_flow(date) for entity in self.inflows.values()
        )
        total_outflows = sum(
            entity.calculate_monthly_cash_flow(date)
            for entity in self.outflows.values()
        )
        return total_inflows + total_outflows
