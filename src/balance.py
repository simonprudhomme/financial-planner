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

    def calculate_total_assets(self, current_date):
        total = 0
        for asset in self.assets.values():
            if hasattr(asset, "calculate_future_value"):
                print(f"{asset.name} is a {asset.calculate_future_value(current_date)}")
                total += asset.calculate_future_value(current_date)
            else:
                total += asset
        return total

    # def calculate_total_liabilities(self, current_date):
    #     total = 0
    #     for liability in self.liabilities.values():
    #         if hasattr(liability, 'calculate_remaining_balance'):
    #             total += liability.calculate_remaining_balance(current_date)
    #         else:
    #             total += liability
    #     return total

    # def calculate_net_worth(self, current_date):
    #     return self.calculate_total_assets(current_date) - self.calculate_total_liabilities(current_date)
