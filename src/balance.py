import datetime as dt

from loguru import logger


class Balance:
    def __init__(self):
        self.entities = {}

    def add_entity(self, entity):
        self.entities[entity.name] = entity

    def calculate_net_worth(self, date: str):
        logger.debug(f"Calculate Net Worth for {date}")
        monthly_net_worth = 0
        results = {}
        for entity in self.entities.values():
            net_worth = entity.calculate_future_value(date)
            results[entity.name] = net_worth
            entity_name = entity.name
            logger.debug(f"{entity_name:15} : ${net_worth:,.0f}")
            monthly_net_worth += net_worth
        logger.info(f"Total net worth: $ {monthly_net_worth:,.0f} \n\n")
        return monthly_net_worth, results

    def update(self, *arg, **kwarg):
        pass
