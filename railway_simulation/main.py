import argparse
import os
import sys
from pathlib import Path

from network import RailwayNetwork
from simulator import RailwaySimulator
from metrics import MetricsReport
from visualizer import RailwayVisualizer
from scenarios import ScenarioBuilder

def print_header():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  AI-Based Railway Traffic Control Simulation               ║")
    print("║  Multi-Objective Optimization Framework                    ║")
    print("║  Phase 1: Simulation Environment & Baseline Controller     ║")
    print("╚══════════════════════════════════════════════════════════════╝")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scenario', default='normal')
    parser.add_argument('--controller', default='heuristic')
    parser.add_argument('--compare', action='store_true')
    parser.add_argument('--output', default='output')
    parser.add_argument('--verbose', action='store_true', default=True)
    args = parser.parse_args()

    print_header()
    
    scenarios = ScenarioBuilder.get_all()
    if args.scenario not in scenarios:
        print(f"Unknown scenario. Available: {list(scenarios.keys())}")
        sys.exit(1)

    if args.compare:
        print(f"\n--- Controller Comparison on Scenario: '{args.scenario}' ---")
        results = {}
        for ctrl in ['fcfs', 'priority', 'heuristic']:
            net, trains, config = scenarios[args.scenario]()
            config.controller_type = ctrl
            config.verbose = False
            sim = RailwaySimulator(net, trains, config)
            res = sim.run()
            results[ctrl] = res
            print(f"  [{ctrl.upper():10s}] Throughput={res.throughput_per_hour:.2f} t/hr | "
                  f"AvgWait={res.avg_waiting_time:.1f} min | "
                  f"AvgDelay={res.avg_delay:.1f} min | "
                  f"Conflicts={res.total_conflicts} | "
                  f"Completed={res.trains_completed}/{res.trains_total}")

        print("\n  Summary Table:")
        print(f"  {'Controller':<25} {'Throughput':>12} {'Avg Wait':>10} {'Avg Delay':>11} {'Conflicts':>11} {'Completed':>11}")
        print("  " + "-"*80)
        for ctrl, res in results.items():
            cname = res.controller_name
            print(f"  {cname:<25} {res.throughput_per_hour:>10.2f}   {res.avg_waiting_time:>9.1f}  "
                  f"{res.avg_delay:>10.1f}  {res.total_conflicts:>10}  "
                  f"{res.trains_completed}/{res.trains_total}")

        os.makedirs(args.output, exist_ok=True)
        RailwayVisualizer.plot_controller_comparison(results, os.path.join(args.output, 'comparison.png'))
        print(f"\n  Comparison plot saved to: {args.output}/comparison.png")
        return

    net, trains, config = scenarios[args.scenario]()
    config.controller_type = args.controller
    
    net.display_network()
    
    sim = RailwaySimulator(net, trains, config)
    result = sim.run()
    
    if args.verbose:
        sim.logger.print_log()
        
    rep = MetricsReport.from_result(result, trains)
    rep.print_report()
    
    RailwayVisualizer.save_all_plots(result, result.per_train_stats, args.output)
    RailwayVisualizer.plot_network(net, save_path=os.path.join(args.output, 'network.png'))

if __name__ == '__main__':
    main()
