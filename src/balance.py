import datetime as dt


class Balance:
    def __init__(self):
        self.entities = {}

    def add_entity(self, entity):
        self.entities[entity.name] = entity

    def calculate_net_worth(self, date: str):
        return sum(
            entity.calculate_future_value(date) for entity in self.entities.values()
        )

    def update(self, *arg, **kwarg):
        pass
