import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

from network import RailwayNetwork
from simulator import SimResult

class RailwayVisualizer:
    @staticmethod
    def plot_network(network: RailwayNetwork, title='Railway Network', save_path=None):
        plt.figure(figsize=(8, 4))
        pos = {'Station A': (0,1), 'Station B': (2,1), 'Station C': (4,1), 'Station D': (2,0)}
        
        for sec in network.sections.values():
            p1 = pos[sec.from_station]
            p2 = pos[sec.to_station]
            color = 'red' if sec.occupied_by else 'green'
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, linewidth=2)
            mid = ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)
            plt.text(mid[0], mid[1]+0.05, f"{sec.section_id}({sec.travel_time}m)", ha='center')

        for name, p in pos.items():
            plt.plot(p[0], p[1], 'bo', markersize=10)
            plt.text(p[0], p[1]-0.15, name, ha='center')
            
        plt.title(title)
        plt.axis('off')
        if save_path:
            plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_waiting_times(per_train_stats, save_path=None):
        plt.figure(figsize=(8, 4))
        names = [s['train_id'] for s in per_train_stats]
        waits = [s['waiting_time_total'] for s in per_train_stats]
        types = [s['type'] for s in per_train_stats]
        
        colors = []
        for t in types:
            if t == 'EXPRESS': colors.append('blue')
            elif t == 'PASSENGER': colors.append('green')
            else: colors.append('orange')
            
        bars = plt.bar(names, waits, color=colors)
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, f"{yval:.1f}", ha='center', va='bottom')
            
        plt.title('Waiting Time per Train')
        plt.ylabel('Time (min)')
        if save_path:
            plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_section_utilization(section_utilization, save_path=None):
        plt.figure(figsize=(6, 4))
        secs = list(section_utilization.keys())
        utils = [u * 100 for u in section_utilization.values()]
        
        plt.bar(secs, utils, color='purple')
        plt.axhline(y=100, color='r', linestyle='-')
        plt.title('Section Utilization (%)')
        plt.ylabel('Utilization %')
        if save_path:
            plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_timeline(timeline, save_path=None):
        plt.figure(figsize=(8, 4))
        times = [t['sim_time'] for t in timeline]
        moving = [t['moving'] for t in timeline]
        waiting = [t['waiting'] for t in timeline]
        
        plt.plot(times, moving, label='Moving', color='blue')
        plt.plot(times, waiting, label='Waiting', color='orange')
        plt.title('Train Status Over Simulation Time')
        plt.xlabel('Sim Time (min)')
        plt.ylabel('Count')
        plt.legend()
        if save_path:
            plt.savefig(save_path)
        plt.close()

    @staticmethod
    def plot_controller_comparison(results: dict, save_path=None):
        fig, axs = plt.subplots(2, 2, figsize=(10, 8))
        names = list(results.keys())
        
        thru = [r.throughput_per_hour for r in results.values()]
        wait = [r.avg_waiting_time for r in results.values()]
        dela = [r.avg_delay for r in results.values()]
        conf = [r.total_conflicts for r in results.values()]
        
        axs[0,0].bar(names, thru, color='blue')
        axs[0,0].set_title('Throughput')
        
        axs[0,1].bar(names, wait, color='orange')
        axs[0,1].set_title('Avg Wait Time')
        
        axs[1,0].bar(names, dela, color='green')
        axs[1,0].set_title('Avg Delay')
        
        axs[1,1].bar(names, conf, color='red')
        axs[1,1].set_title('Conflicts')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        plt.close()

    @staticmethod
    def save_all_plots(result: SimResult, per_train_stats, output_dir='output'):
        os.makedirs(output_dir, exist_ok=True)
        RailwayVisualizer.plot_waiting_times(per_train_stats, os.path.join(output_dir, 'waiting_times.png'))
        RailwayVisualizer.plot_section_utilization(result.section_utilization, os.path.join(output_dir, 'utilization.png'))
        RailwayVisualizer.plot_timeline(result.timeline, os.path.join(output_dir, 'timeline.png'))
        print(f"Plots saved to {output_dir}")
