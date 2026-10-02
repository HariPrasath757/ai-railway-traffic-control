from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ConflictEvent:
    timestamp: float
    section_id: str
    requesting_trains: List[str]
    winner_train: str
    loser_trains: List[str]
    scores: Optional[Dict[str, float]] = None

class ConflictDetector:
    def __init__(self):
        self.conflicts: List[ConflictEvent] = []

    def log_conflict(self, event: ConflictEvent):
        self.conflicts.append(event)

    def detect_and_log(self, timestamp: float, section_id: str, requesting_trains: List[str], winner: str, loser_trains: List[str], scores: Optional[Dict[str, float]] = None) -> ConflictEvent:
        event = ConflictEvent(timestamp, section_id, requesting_trains, winner, loser_trains, scores)
        self.log_conflict(event)
        return event

    def get_summary(self) -> dict:
        by_sec = {}
        for c in self.conflicts:
            by_sec[c.section_id] = by_sec.get(c.section_id, 0) + 1
        
        sorted_secs = sorted(by_sec.items(), key=lambda x: x[1], reverse=True)
        return {
            "total_conflicts": len(self.conflicts),
            "most_contested_sections": [s[0] for s in sorted_secs],
            "conflicts_by_section": by_sec
        }

    def print_conflict(self, event: ConflictEvent):
        print(f"[{event.timestamp}] CONFLICT at {event.section_id}: {event.requesting_trains} -> Winner: {event.winner_train}")
