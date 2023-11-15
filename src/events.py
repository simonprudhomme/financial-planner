from dataclasses import dataclass
from typing import Dict


@dataclass
class Event:
    name: str
    action: Dict[str, str]


class EventManager:
    def __init__(self):
        self.events = {}

    def add_event(self, event: Event):
        self.events[event.name] = event

    def update(self, event_name, **kwargs):
        self.events[event_name].action.update(kwargs)
