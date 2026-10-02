from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass
class Station:
    name: str
    capacity: int = 5
    is_terminus: bool = False

@dataclass
class Section:
    section_id: str
    from_station: str
    to_station: str
    travel_time: float
    capacity: int = 1
    bidirectional: bool = True
    occupied_by: Optional[str] = None

class RailwayNetwork:
    def __init__(self):
        self.stations: Dict[str, Station] = {}
        self.sections: Dict[str, Section] = {}

    def add_station(self, name: str, capacity: int = 5, is_terminus: bool = False):
        self.stations[name] = Station(name, capacity, is_terminus)

    def add_section(self, section_id: str, from_st: str, to_st: str, travel_time: float, capacity: int = 1, bidirectional: bool = True):
        self.sections[section_id] = Section(section_id, from_st, to_st, travel_time, capacity, bidirectional, None)

    def get_section_between(self, a: str, b: str) -> Optional[Section]:
        for sec in self.sections.values():
            if sec.from_station == a and sec.to_station == b:
                return sec
            if sec.bidirectional and sec.from_station == b and sec.to_station == a:
                return sec
        return None

    def get_adjacent_sections(self, station_name: str) -> List[Section]:
        adj = []
        for sec in self.sections.values():
            if sec.from_station == station_name or (sec.bidirectional and sec.to_station == station_name):
                adj.append(sec)
        return adj

    def is_section_free(self, section_id: str) -> bool:
        return self.sections[section_id].occupied_by is None

    def occupy_section(self, section_id: str, train_id: str):
        self.sections[section_id].occupied_by = train_id

    def free_section(self, section_id: str):
        self.sections[section_id].occupied_by = None

    def display_network(self):
        print("Network Topology:")
        print("Station A ---- S1 ---- Station B ---- S2 ---- Station C")
        print("                            |")
        print("                            S3")
        print("                            |")
        print("                        Station D")

    def get_network_stats(self) -> dict:
        return {
            "num_stations": len(self.stations),
            "num_sections": len(self.sections)
        }
