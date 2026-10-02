from network import RailwayNetwork
from train import Train, TrainType
from simulator import SimConfig

class ScenarioBuilder:
    @staticmethod
    def build_network() -> RailwayNetwork:
        net = RailwayNetwork()
        net.add_station("Station A", is_terminus=True)
        net.add_station("Station B")
        net.add_station("Station C", is_terminus=True)
        net.add_station("Station D", is_terminus=True)
        
        net.add_section("S1", "Station A", "Station B", 15.0)
        net.add_section("S2", "Station B", "Station C", 20.0)
        net.add_section("S3", "Station B", "Station D", 12.0)
        return net

    @staticmethod
    def normal_traffic():
        net = ScenarioBuilder.build_network()
        trains = [
            Train("EXP101", TrainType.EXPRESS, ["Station A", "Station B", "Station C"], 0),
            Train("PAS201", TrainType.PASSENGER, ["Station C", "Station B", "Station A"], 5),
            Train("EXP102", TrainType.EXPRESS, ["Station D", "Station B", "Station C"], 2),
            Train("FRT301", TrainType.FREIGHT, ["Station A", "Station B", "Station D"], 8)
        ]
        return net, trains, SimConfig(duration=120)

    @staticmethod
    def congested_traffic():
        net, trains, _ = ScenarioBuilder.normal_traffic()
        trains.extend([
            Train("EXP103", TrainType.EXPRESS, ["Station A", "Station B", "Station C"], 1),
            Train("PAS202", TrainType.PASSENGER, ["Station D", "Station B", "Station A"], 3)
        ])
        return net, trains, SimConfig(duration=150)

    @staticmethod
    def delayed_train():
        net, trains, _ = ScenarioBuilder.normal_traffic()
        trains[0].start_time = 20
        return net, trains, SimConfig(duration=140)

    @staticmethod
    def high_priority_conflict():
        net = ScenarioBuilder.build_network()
        trains = [
            Train("FRT401", TrainType.FREIGHT, ["Station A", "Station B", "Station C"], 0),
            Train("EXP104", TrainType.EXPRESS, ["Station A", "Station B", "Station C"], 0),
            Train("PAS203", TrainType.PASSENGER, ["Station A", "Station B", "Station C"], 1)
        ]
        return net, trains, SimConfig(duration=100)

    @staticmethod
    def get_all():
        return {
            'normal': ScenarioBuilder.normal_traffic,
            'congested': ScenarioBuilder.congested_traffic,
            'delayed': ScenarioBuilder.delayed_train,
            'high_priority': ScenarioBuilder.high_priority_conflict
        }
