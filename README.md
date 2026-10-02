# 🚆 AI-Based Railway Traffic Control Simulation

> **Multi-Objective Optimization for Real-Time Railway Traffic Control and Section Throughput Maximization**
> An advanced research prototype and interactive evaluation testbed comparing Traditional / Greedy controllers with a Multi-Objective Optimization framework.

---

## 📌 Project Overview

This project implements a real-time railway traffic control simulation designed to resolve traffic bottlenecks, track conflicts, and propagation delays across complex bidirectional railway networks.

It features:
1. **Interactive Research Web Dashboard (`railway_simulation/app.html`)**:
   - Live visual simulation of trains, station queues, track occupancy, and section bottlenecks.
   - Comprehensive fleet-wide metrics: Section Throughput, Active Delay, Fleet Progress Fraction, Punctuality Rate, Jain's Fairness Index, and Resource Utilization.
   - Live Head-to-Head Comparison: Greedy (FCFS/Priority) vs. Proposed Multi-Objective Controller under identical seeds, topologies, and disruption schedules.
   - Real-time time-distance string charts, interactive train telemetry, and conflict resolution logs.

2. **Python Discrete-Event Simulation Suite (`railway_simulation/`)**:
   - Discrete-event simulator modeling track mutexes, bidirectional headway, and dynamic priority dispatching.
   - Configurable scenarios: Normal, Congested, Disrupted, and High-Priority bottlenecks.
   - Matplotlib visualization module generating publication-ready charts.

---

## 🚀 Quick Start

### Option 1: Interactive Web Simulation (No Installation Required!)
Simply open `railway_simulation/app.html` in any modern web browser (Google Chrome, Microsoft Edge, Firefox):
```bash
# On Windows (PowerShell):
Start-Process railway_simulation/app.html
```
Or double-click `app.html` directly from your file explorer.

### Option 2: Python Simulation Suite
Ensure you have Python 3.8+ installed:
```bash
cd railway_simulation
pip install -r requirements.txt

# Run standard simulation with heuristic multi-objective controller
python main.py

# Run head-to-head controller comparison across all metrics
python main.py --compare

# Run congested scenario with FCFS controller
python main.py --scenario congested --controller fcfs
```

---

## 🏛️ Railway Network Topology

```
Station A ---- S1 ---- Station B ---- S2 ---- Station C
                            |
                            S3
                            |
                        Station D
```
- **S1 (A ↔ B)**: Bidirectional, travel time = 15 min
- **S2 (B ↔ C)**: Bidirectional, travel time = 20 min
- **S3 (B ↔ D)**: Bidirectional, travel time = 12 min

---

## 🧠 Evaluated Controllers

1. **Traditional Greedy / FCFS**:
   - First-Come, First-Served or basic static priority. Dispatches the first arrived train without looking ahead at bottleneck congestion or downstream starvation.
2. **Proposed Multi-Objective Controller**:
   - Real-time scoring function evaluating:
     - Train priority (Express > Passenger > Freight)
     - Accumulated waiting time & delay
     - Downstream section congestion & starvation prevention
     - Network fairness (Jain's Fairness Index) and fleet progress fraction

---

## 📂 Repository Structure

```
.
├── .gitignore
├── README.md
└── railway_simulation/
    ├── app.html              # Full interactive Research Web Application
    ├── main.py               # Main CLI simulation entry point
    ├── simulator.py          # Core discrete-event simulation engine
    ├── controller.py         # Baseline & Multi-Objective dispatch controllers
    ├── network.py            # Railway network graph and block section logic
    ├── train.py              # Train state machines, routes, and priorities
    ├── conflict.py           # Conflict detection and arbitration logger
    ├── metrics.py            # Fleet metrics, throughput, delay & fairness calculations
    ├── scenarios.py          # Pre-built benchmark scenarios and disruption patterns
    ├── visualizer.py         # Matplotlib chart generators
    ├── setup_and_run.ps1     # Automated setup script for Windows
    └── requirements.txt      # Python dependencies
```
