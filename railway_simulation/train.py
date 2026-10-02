from enum import Enum
from typing import List, Optional, Dict

class TrainType(Enum):
    EXPRESS = 3
    PASSENGER = 2
    FREIGHT = 1

class TrainStatus(Enum):
    SCHEDULED = "SCHEDULED"
    WAITING = "WAITING"
    MOVING = "MOVING"
    COMPLETED = "COMPLETED"

class Train:
    def __init__(self, train_id: str, train_type: TrainType, route: List[str], start_time: float = 0, scheduled_times: Optional[Dict[str, float]] = None):
        self.train_id = train_id
        self.train_type = train_type
        self.route = route
        self.start_time = start_time
        self.scheduled_times = scheduled_times or {}
        
        self.current_station_idx = 0
        self.current_section: Optional[str] = None
        self.status = TrainStatus.SCHEDULED
        
        self.arrival_time: Optional[float] = None
        self.entry_time: Optional[float] = None
        self.waiting_time_total = 0.0
        self.delay_total = 0.0
        self.sections_completed = 0

    @property
    def current_station(self) -> str:
        return self.route[self.current_station_idx]

    @property
    def next_station(self) -> Optional[str]:
        if self.current_station_idx + 1 < len(self.route):
            return self.route[self.current_station_idx + 1]
        return None

    @property
    def priority(self) -> int:
        return self.train_type.value

    @property
    def is_completed(self) -> bool:
        return self.status == TrainStatus.COMPLETED

    def waiting_time_current(self, sim_time: float) -> float:
        if self.status == TrainStatus.WAITING and self.arrival_time is not None:
            return sim_time - self.arrival_time
        return 0.0

    def get_next_section_needed(self, network) -> Optional[str]:
        nxt = self.next_station
        if not nxt:
            return None
        sec = network.get_section_between(self.current_station, nxt)
        return sec.section_id if sec else None

    def start_moving(self, section_id: str, sim_time: float):
        self.current_section = section_id
        self.entry_time = sim_time
        if self.status == TrainStatus.WAITING and self.arrival_time is not None:
            self.waiting_time_total += (sim_time - self.arrival_time)
        self.status = TrainStatus.MOVING

    def complete_section(self, sim_time: float):
        self.current_station_idx += 1
        self.sections_completed += 1
        if self.scheduled_times and self.current_station in self.scheduled_times:
            expected = self.scheduled_times[self.current_station]
            if sim_time > expected:
                self.delay_total += (sim_time - expected)
        self.current_section = None
        self.entry_time = None
        self.arrival_time = sim_time

    def spawn(self, sim_time: float):
        self.status = TrainStatus.WAITING
        self.arrival_time = sim_time

    def __repr__(self):
        return f"<Train {self.train_id} ({self.train_type.name}) {self.status.name}>"
