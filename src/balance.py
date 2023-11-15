import datetime as dt

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
