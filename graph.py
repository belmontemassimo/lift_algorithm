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

# plot1
    def _plot_waiting_times(self, completed_requests: List[Request]):
        """Plot waiting times for each request"""
        plt.figure(figsize=(10, 6))
        waiting_times = [req.time_on_floor for req in completed_requests]
        # Sort requests by creation time
        sorted_indices = sorted(range(len(completed_requests)), 
                              key=lambda k: completed_requests[k].time_created)
        sorted_times = [waiting_times[i] for i in sorted_indices]
        
        plt.plot(range(len(sorted_times)), sorted_times, marker='o')
        plt.title('Waiting Times Over Request Sequence')
        plt.xlabel('Request Number')
        plt.ylabel('Waiting Time (seconds)')
        plt.grid(True, which='both', linestyle='-', alpha=0.5)
        plt.minorticks_on()
        plt.ylim(bottom=0)
        plt.xlim(left=0)
        ax = plt.gca()
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        # Hide the top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

# plot2
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
        plt.grid(True, which='both', linestyle='-', alpha=0.5)
        plt.minorticks_on()
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        ax = plt.gca()
        ax.spines['left'].set_position(('data', 0))
        ax.spines['bottom'].set_position(('data', 0))
        # Hide the top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

# plot3
    def _plot_turnaround_times(self, completed_requests: List[Request]):
        """Plot total turnaround times (waiting + travel)"""
        plt.figure(figsize=(10, 6))
        turnaround_times = [(req.time_in_lift + req.time_on_floor) for req in completed_requests]
        # Sort requests by creation time
        sorted_indices = sorted(range(len(completed_requests)), 
                              key=lambda k: completed_requests[k].time_created)
        sorted_times = [turnaround_times[i] for i in sorted_indices]
        
        plt.plot(range(len(sorted_times)), sorted_times, marker='o')
        plt.title('Total Turnaround Times Over Request Sequence')
        plt.xlabel('Request Number')
        plt.ylabel('Turnaround Time (seconds)')
        plt.grid(True, which='both', linestyle='-', alpha=0.5)
        plt.minorticks_on()
        plt.ylim(bottom=0)
        plt.xlim(left=0)
        ax = plt.gca()
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        # Hide the top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)


# plot4
    def _plot_system_statistics(self, completed_requests: List[Request], total_time: float):
        """Plot overall system statistics"""
        plt.figure(figsize=(10, 6))
        
        # Calculate key metrics
        avg_waiting_time = np.mean([req.time_on_floor for req in completed_requests])
        avg_travel_time = np.mean([req.time_in_lift for req in completed_requests])
        avg_turnaround = np.mean([req.time_in_lift + req.time_on_floor for req in completed_requests])
        throughput = len(completed_requests) / total_time
        
        # Create two separate sets of metrics
        time_metrics = ['Avg Waiting Time', 'Avg Travel Time', 'Avg Turnaround']
        time_values = [avg_waiting_time, avg_travel_time, avg_turnaround]
        
        # Create figure with two y-axes
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # Plot time metrics on the left y-axis
        bars1 = ax1.bar(time_metrics, time_values, color='skyblue')
        ax1.set_ylabel('Time (seconds)')
        ax1.set_ylim(bottom=0)
        
        # Create a second y-axis for throughput
        ax2 = ax1.twinx()
        bars2 = ax2.bar(['Throughput'], [throughput], color='orange')
        ax2.set_ylabel('Requests per second')
        ax2.set_ylim(bottom=0)
        
        # Set title and grid
        ax1.set_title('System Performance Metrics')
        ax1.grid(True, which='both', linestyle='-', alpha=0.5)
        ax1.minorticks_on()
        
        # Add value labels on top of each bar
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}',
                    ha='center', va='bottom')
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}',
                    ha='center', va='bottom')
            
        plt.tight_layout()