from dataclasses import dataclass, field
from typing import List, Dict, Optional
import random

from network import RailwayNetwork
from train import Train, TrainStatus
from conflict import ConflictDetector
from controller import BaseController, ControllerFactory, HeuristicController
from logger import SimLogger, EventType

@dataclass
class SimConfig:
    duration: float = 120.0
    time_step: float = 1.0
    controller_type: str = 'heuristic'
    random_seed: int = 42
    verbose: bool = True

@dataclass
class SimResult:
    trains: List[Train]
    conflict_summary: dict
    section_utilization: dict
    trains_completed: int
    trains_total: int
    simulation_duration: float
    throughput_per_hour: float
    avg_waiting_time: float
    avg_delay: float
    total_conflicts: int
    per_train_stats: List[dict]
    timeline: List[dict]
    controller_name: str

class RailwaySimulator:
    def __init__(self, network: RailwayNetwork, trains: List[Train], config: SimConfig):
        self.network = network
        self.trains = list(trains)
        self.config = config
        
        random.seed(config.random_seed)
        self.section_queue: Dict[str, List[Train]] = {}
        self.section_occupied_until: Dict[str, float] = {}
        self.conflict_detector = ConflictDetector()
        self.controller = ControllerFactory.create(config.controller_type)
        self.logger = SimLogger()
        self.section_busy_time: Dict[str, float] = {s: 0.0 for s in self.network.sections}
        self.timeline: List[dict] = []

    def run(self) -> SimResult:
        duration = self.config.duration
        time_step = self.config.time_step
        steps = int(duration / time_step)
        
        for step in range(steps + 1):
            sim_time = step * time_step
            
            self._spawn_trains(sim_time)
            self._update_moving_trains(sim_time)
            self._resolve_queues(sim_time)
            self._update_waiting_times(sim_time)
            
            if step % 10 == 0:
                num_moving = sum(1 for t in self.trains if t.status == TrainStatus.MOVING)
                num_waiting = sum(1 for t in self.trains if t.status == TrainStatus.WAITING)
                num_completed = sum(1 for t in self.trains if t.status == TrainStatus.COMPLETED)
                self.timeline.append({
                    "sim_time": sim_time,
                    "moving": num_moving,
                    "waiting": num_waiting,
                    "completed": num_completed
                })
                
        return self._build_result()

    def _spawn_trains(self, sim_time: float):
        for t in self.trains:
            if t.status == TrainStatus.SCHEDULED and t.start_time <= sim_time:
                t.spawn(sim_time)
                self.logger.log(sim_time, EventType.TRAIN_SPAWNED, f"Train {t.train_id} spawned at {t.current_station}", train_id=t.train_id)
                self._enqueue_train(t)

    def _enqueue_train(self, train: Train):
        sec_id = train.get_next_section_needed(self.network)
        if sec_id:
            if sec_id not in self.section_queue:
                self.section_queue[sec_id] = []
            if train not in self.section_queue[sec_id]:
                self.section_queue[sec_id].append(train)

    def _update_moving_trains(self, sim_time: float):
        for t in self.trains:
            if t.status == TrainStatus.MOVING:
                expected_exit = t.entry_time + self._get_section_travel_time(t.current_section)
                if sim_time >= expected_exit:
                    sec_id = t.current_section
                    self.network.free_section(sec_id)
                    t.complete_section(sim_time)
                    self.logger.log(sim_time, EventType.SECTION_FREED, f"Train {t.train_id} freed section {sec_id}", train_id=t.train_id, section_id=sec_id)
                    
                    if not t.next_station:
                        t.status = TrainStatus.COMPLETED
                        self.logger.log(sim_time, EventType.TRAIN_COMPLETED, f"Train {t.train_id} completed route at {t.current_station}", train_id=t.train_id)
                    else:
                        t.spawn(sim_time)
                        self._enqueue_train(t)

    def _resolve_queues(self, sim_time: float):
        for sec_id, queue in list(self.section_queue.items()):
            if not queue:
                continue
            if not self.network.is_section_free(sec_id):
                continue
            
            if len(queue) == 1:
                winner = queue.pop(0)
            else:
                winner = self.controller.resolve(queue, sec_id, sim_time)
                req_trains = [t.train_id for t in queue]
                losers = [t.train_id for t in queue if t.train_id != winner.train_id]
                scores = getattr(self.controller, 'last_scores', None)
                self.conflict_detector.detect_and_log(sim_time, sec_id, req_trains, winner.train_id, losers, scores)
                self.logger.log(sim_time, EventType.CONFLICT_DETECTED, f"Conflict at {sec_id} among {req_trains}", section_id=sec_id)
                self.logger.log(sim_time, EventType.DISPATCH_DECISION, f"{self.controller.name} dispatched {winner.train_id} to {sec_id}", train_id=winner.train_id, section_id=sec_id)
                queue.remove(winner)
            
            self.network.occupy_section(sec_id, winner.train_id)
            winner.start_moving(sec_id, sim_time)
            travel_t = self._get_section_travel_time(sec_id)
            self.section_busy_time[sec_id] += travel_t
            self.logger.log(sim_time, EventType.TRAIN_MOVED, f"Train {winner.train_id} entered {sec_id}", train_id=winner.train_id, section_id=sec_id)

    def _update_waiting_times(self, sim_time: float):
        pass # Not dynamically updating here since it's computed on demand

    def _get_section_travel_time(self, section_id: str) -> float:
        return self.network.sections[section_id].travel_time

    def _compute_section_utilization(self):
        return {s: min(1.0, self.section_busy_time[s] / self.config.duration) for s in self.network.sections}

    def _compute_per_train_stats(self):
        stats = []
        for t in self.trains:
            stats.append({
                "train_id": t.train_id,
                "type": t.train_type.name,
                "waiting_time_total": t.waiting_time_total,
                "delay_total": t.delay_total,
                "sections_completed": t.sections_completed,
                "status": t.status.name
            })
        return stats

    def _compute_avg_waiting(self):
        spawned = [t for t in self.trains if t.status != TrainStatus.SCHEDULED]
        if not spawned: return 0.0
        return sum(t.waiting_time_total for t in spawned) / len(spawned)

    def _compute_avg_delay(self):
        spawned = [t for t in self.trains if t.status != TrainStatus.SCHEDULED]
        if not spawned: return 0.0
        return sum(t.delay_total for t in spawned) / len(spawned)

    def _build_result(self) -> SimResult:
        comps = sum(1 for t in self.trains if t.status == TrainStatus.COMPLETED)
        hr = self.config.duration / 60.0
        thru = comps / hr if hr > 0 else 0
        
        return SimResult(
            trains=self.trains,
            conflict_summary=self.conflict_detector.get_summary(),
            section_utilization=self._compute_section_utilization(),
            trains_completed=comps,
            trains_total=len(self.trains),
            simulation_duration=self.config.duration,
            throughput_per_hour=thru,
            avg_waiting_time=self._compute_avg_waiting(),
            avg_delay=self._compute_avg_delay(),
            total_conflicts=len(self.conflict_detector.conflicts),
            per_train_stats=self._compute_per_train_stats(),
            timeline=self.timeline,
            controller_name=self.controller.name
        )
