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
