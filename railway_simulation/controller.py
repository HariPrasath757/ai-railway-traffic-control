from abc import ABC, abstractmethod
from typing import List, Dict
from train import Train

class BaseController(ABC):
    name: str = "Base"
    
    @abstractmethod
    def resolve(self, waiting_trains: List[Train], section_id: str, sim_time: float) -> Train:
        pass

class FCFSController(BaseController):
    name = 'FCFS'
    def resolve(self, waiting_trains: List[Train], section_id: str, sim_time: float) -> Train:
        return min(waiting_trains, key=lambda t: t.arrival_time if t.arrival_time is not None else float('inf'))

class PriorityController(BaseController):
    name = 'Priority'
    def resolve(self, waiting_trains: List[Train], section_id: str, sim_time: float) -> Train:
        return max(waiting_trains, key=lambda t: (t.priority, -t.arrival_time if t.arrival_time is not None else -float('inf')))

class HeuristicController(BaseController):
    name = 'Heuristic (Multi-Objective)'
    
    def __init__(self):
        self.last_scores: Dict[str, float] = {}

    def score(self, train: Train, sim_time: float) -> float:
        return 10 * train.priority + 2 * train.waiting_time_current(sim_time) + 1 * train.delay_total

    def resolve(self, waiting_trains: List[Train], section_id: str, sim_time: float) -> Train:
        self.last_scores = {t.train_id: self.score(t, sim_time) for t in waiting_trains}
        winner = max(waiting_trains, key=lambda t: self.last_scores[t.train_id])
        return winner

class ControllerFactory:
    @staticmethod
    def create(name: str) -> BaseController:
        n = name.lower()
        if n == 'fcfs':
            return FCFSController()
        elif n == 'priority':
            return PriorityController()
        elif n in ['heuristic', 'heuristic (multi-objective)']:
            return HeuristicController()
        else:
            raise ValueError(f"Unknown controller: {name}")
