from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict

class EventType(Enum):
    TRAIN_SPAWNED = "TRAIN_SPAWNED"
    TRAIN_MOVED = "TRAIN_MOVED"
    SECTION_FREED = "SECTION_FREED"
    CONFLICT_DETECTED = "CONFLICT_DETECTED"
    DISPATCH_DECISION = "DISPATCH_DECISION"
    TRAIN_COMPLETED = "TRAIN_COMPLETED"
    TRAIN_WAITING = "TRAIN_WAITING"

@dataclass
class SimEvent:
    time: float
    event_type: EventType
    message: str
    train_id: str = ''
    section_id: str = ''
    metadata: Dict = field(default_factory=dict)

class SimLogger:
    def __init__(self):
        self.events: List[SimEvent] = []

    def log(self, time: float, event_type: EventType, message: str, train_id: str = '', section_id: str = '', **kwargs):
        self.events.append(SimEvent(time, event_type, message, train_id, section_id, kwargs))

    def get_events(self, event_type: EventType = None) -> List[SimEvent]:
        if event_type:
            return [e for e in self.events if e.event_type == event_type]
        return self.events

    def print_log(self, event_type: EventType = None):
        for e in self.get_events(event_type):
            print(f"[{e.time:06.1f}] [{e.event_type.name:18s}] {e.message}")

    def export_csv(self, path: str):
        import csv
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["time", "event_type", "message", "train_id", "section_id", "metadata"])
            for e in self.events:
                writer.writerow([e.time, e.event_type.name, e.message, e.train_id, e.section_id, str(e.metadata)])
