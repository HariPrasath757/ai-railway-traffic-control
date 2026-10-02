from simulator import SimResult
from train import Train, TrainType

def compute_jains_fairness(values: list) -> float:
    if not values: return 1.0
    n = len(values)
    s = sum(values)
    sq_sum = sum(x*x for x in values)
    if sq_sum == 0: return 1.0
    return (s * s) / (n * sq_sum)

class MetricsReport:
    def __init__(self):
        self.section_throughput_per_hour = 0.0
        self.avg_waiting_by_type = {}
        self.avg_delay_by_type = {}
        self.section_utilization = {}
        self.total_conflicts = 0
        self.conflict_rate = 0.0
        self.fairness_index = 1.0
        self.trains_completed = 0
        self.trains_total = 0

    @classmethod
    def from_result(cls, result: SimResult, trains: list):
        rep = cls()
        rep.section_throughput_per_hour = result.throughput_per_hour
        rep.section_utilization = result.section_utilization
        rep.total_conflicts = result.total_conflicts
        rep.trains_completed = result.trains_completed
        rep.trains_total = result.trains_total
        rep.conflict_rate = result.total_conflicts / result.trains_total if result.trains_total else 0

        wait_by_type = {}
        delay_by_type = {}
        count_by_type = {}
        for t in trains:
            tn = t.train_type.name
            wait_by_type[tn] = wait_by_type.get(tn, 0.0) + t.waiting_time_total
            delay_by_type[tn] = delay_by_type.get(tn, 0.0) + t.delay_total
            count_by_type[tn] = count_by_type.get(tn, 0) + 1

        for tn, count in count_by_type.items():
            rep.avg_waiting_by_type[tn] = wait_by_type[tn] / count
            rep.avg_delay_by_type[tn] = delay_by_type[tn] / count

        waits = [t.waiting_time_total for t in trains]
        rep.fairness_index = compute_jains_fairness(waits)
        
        return rep

    def print_report(self):
        print("\n--- Metrics Report ---")
        print(f"Trains Completed: {self.trains_completed}/{self.trains_total}")
        print(f"Throughput (trains/hr): {self.section_throughput_per_hour:.2f}")
        print(f"Total Conflicts: {self.total_conflicts}")
        print(f"Conflict Rate: {self.conflict_rate:.2f}")
        print(f"Jain's Fairness (Wait): {self.fairness_index:.2f}")
        print("Section Utilization:")
        for k, v in self.section_utilization.items():
            print(f"  {k}: {v*100:.1f}%")
        print("Average Waiting Time by Type:")
        for k, v in self.avg_waiting_by_type.items():
            print(f"  {k}: {v:.1f}")

    def to_dict(self) -> dict:
        return {
            "section_throughput_per_hour": self.section_throughput_per_hour,
            "avg_waiting_by_type": self.avg_waiting_by_type,
            "avg_delay_by_type": self.avg_delay_by_type,
            "section_utilization": self.section_utilization,
            "total_conflicts": self.total_conflicts,
            "conflict_rate": self.conflict_rate,
            "fairness_index": self.fairness_index,
            "trains_completed": self.trains_completed,
            "trains_total": self.trains_total
        }
