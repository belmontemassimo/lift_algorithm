import matplotlib.pyplot as plt
import numpy as np
from typing import List
from request import Request
from lift import Lift

class SimulationAnalytics:
    def __init__(self):
        self.lift_positions_history: List[List[float]] = []
        self.lift_states_history: List[List[str]] = []
        self.timestamps: List[float] = []
        
    def record_state(self, time: float, lifts: List[Lift]):
        """Record lift states at each timestamp"""
        self.timestamps.append(time)
        self.lift_positions_history.append([lift.position for lift in lifts])
        self.lift_states_history.append([lift.state.name for lift in lifts])

    def generate_graphs(self, completed_requests: List[Request], total_time: float):
        """Generate various analysis graphs"""
        self._plot_waiting_times(completed_requests)
        self._plot_lift_positions()
        self._plot_turnaround_times(completed_requests)
        self._plot_system_statistics(completed_requests, total_time)
        plt.show()

    def _plot_waiting_times(self, completed_requests: List[Request]):
        """Plot waiting times for each request"""
        plt.figure(figsize=(10, 6))
        waiting_times = [req.time_on_floor - req.time_created for req in completed_requests]
        plt.hist(waiting_times, bins=20)
        plt.title('Distribution of Waiting Times')
        plt.xlabel('Waiting Time (seconds)')
        plt.ylabel('Number of Requests')

    def _plot_lift_positions(self):
        """Plot lift positions over time"""
        plt.figure(figsize=(12, 6))
        for lift_idx in range(len(self.lift_positions_history[0])):
            positions = [pos[lift_idx] for pos in self.lift_positions_history]
            plt.plot(self.timestamps, positions, label=f'Lift {lift_idx + 1}')
        plt.title('Lift Positions Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Floor')
        plt.legend()

    def _plot_turnaround_times(self, completed_requests: List[Request]):
        """Plot total turnaround times (waiting + travel)"""
        plt.figure(figsize=(10, 6))
        turnaround_times = [(req.time_in_lift + req.time_on_floor) for req in completed_requests]
        plt.hist(turnaround_times, bins=20)
        plt.title('Distribution of Total Turnaround Times')
        plt.xlabel('Turnaround Time (seconds)')
        plt.ylabel('Number of Requests')

    def _plot_system_statistics(self, completed_requests: List[Request], total_time: float):
        """Plot overall system statistics"""
        plt.figure(figsize=(10, 6))
        
        # Calculate key metrics
        avg_waiting_time = np.mean([req.time_on_floor - req.time_created for req in completed_requests])
        avg_travel_time = np.mean([req.time_in_lift for req in completed_requests])
        avg_turnaround = np.mean([req.time_in_lift + req.time_on_floor for req in completed_requests])
        throughput = len(completed_requests) / total_time

        metrics = ['Avg Waiting Time', 'Avg Travel Time', 'Avg Turnaround', 'Throughput']
        values = [avg_waiting_time, avg_travel_time, avg_turnaround, throughput]

        plt.bar(metrics, values)
        plt.title('System Performance Metrics')
        plt.xticks(rotation=45)
        plt.tight_layout() 