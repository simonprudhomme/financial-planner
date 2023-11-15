from datetime import date
from typing import Callable

from src.entity import EntityFactory


class FinancialEvent:
    def __init__(self, name: str, event_date: date, action: Callable):
        self.name = name
        self.event_date = event_date
        self.action = action

    def execute(self, context):
        self.action(context)

    def create_entity(self, **kwargs):
        return EntityFactory.create_entity(entity_type="Entity", **kwargs)
