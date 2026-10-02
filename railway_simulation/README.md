# AI-Based Multi-Objective Optimization for Real-Time Railway Traffic Control

Comprehensive Python-based railway traffic simulation system for section throughput maximization and conflict resolution.

## Network Topology
```
Station A ---- S1 ---- Station B ---- S2 ---- Station C
                            |
                            S3
                            |
                        Station D
```

## Installation
`pip install -r requirements.txt`

## Usage
- `python main.py` (default: normal scenario, heuristic controller)
- `python main.py --scenario congested --controller fcfs`
- `python main.py --compare`
- `python main.py --scenario high_priority --controller priority`

## Modules
| Module | Description |
|--------|-------------|
| network.py | Topology, stations, and section mutex tracking |
| train.py | Train classes, states, routing |
| simulator.py | Main loop and discrete-event engine |
| controller.py| FCFS, Priority, and Heuristic multi-objective dispatchers |
| metrics.py | Reporting and fairness index calc |

## Research Roadmap
- Phase 1: Simulation env and baseline
- Phase 2: RL integration
- Phase 3: Large-scale topology testing
