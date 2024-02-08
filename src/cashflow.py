import datetime as dt

import pandas as pd
from loguru import logger


class CashFlow:
    def __init__(self):
        self.entities = {}

    def add_entity(self, entity):
        self.entities[entity.name] = entity

    def calculate_monthly_cash_flow(self, date):
        logger.debug(f"Cashflow for: {date}")
        results = {}
        monthly_cashflow = 0
        for entity in self.entities.values():
            cashflow = entity.calculate_monthly_cash_flow(date)
            results[entity.name] = cashflow
            entity_name = entity.name
            logger.debug(f"{entity_name:15} : ${cashflow:,.0f}")
            monthly_cashflow += cashflow
        logger.info(f"Total cashflow: ${monthly_cashflow:,.0f} \n\n")
        return monthly_cashflow, results

    def update(self, *arg, **kwarg):
        pass
