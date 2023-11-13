import datetime as dt
import logging

logger = logging.getLogger(__name__)


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
            logger.info(f"{entity.name:15} ${entity.calculate_monthly_cash_flow(date)}")
            inflows += entity.calculate_monthly_cash_flow(date)

        for entity in self.outflows.values():
            logger.info(f"{entity.name:15} ${entity.calculate_monthly_cash_flow(date)}")
            outflows += entity.calculate_monthly_cash_flow(date)

        return inflows + outflows
