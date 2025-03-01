import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from scipy import stats
from typing import List
from request import Request
from lift import Lift

# Class to handle simulation analytics and graph generation
class SimulationAnalytics:
    def __init__(self):
        # Initialize lists to store lift positions, states, and timestamps
        self.lift_positions_history: List[List[float]] = []
        self.lift_states_history: List[List[str]] = []
        self.timestamps: List[float] = []
        
    # Method to record the state of lifts at a given time
    def record_state(self, time: float, lifts: List[Lift]):
        """Record lift states at each timestamp"""
        self.timestamps.append(time)
        self.lift_positions_history.append([lift.position for lift in lifts])
        self.lift_states_history.append([lift.state.name for lift in lifts])

    # Method to generate various analysis graphs
    def generate_graphs(self, completed_requests: List[Request], total_time: float):
        """Generate various analysis graphs"""
        # Clear any existing figures to avoid duplicates
        plt.close('all')
        
        # Create each plot with a specific figure number and name
        # create figure 1
        plt.figure(1, figsize=(10, 6))
        self._plot_waiting_times(completed_requests)
        
        # create figure 2
        plt.figure(2, figsize=(12, 6))
        self._plot_lift_positions()
        
        # create figure 3
        plt.figure(3, figsize=(10, 6))
        self._plot_turnaround_times(completed_requests)
        
        # Create figure 4
        plt.figure(4, figsize=(10, 6))
        self._plot_system_statistics(completed_requests, total_time)
        
        plt.show()

    # Method to plot waiting times for each request
    def _plot_waiting_times(self, completed_requests: List[Request]):
        """Plot waiting times for each request"""
        plt.clf()  
        # Extract waiting times
        waiting_times = [req.time_on_floor for req in completed_requests]  
        # Sort requests by creation time
        sorted_indices = sorted(range(len(completed_requests)), 
                              key=lambda k: completed_requests[k].time_created)
        # Sort waiting times
        sorted_times = [waiting_times[i] for i in sorted_indices]  
        
        plt.plot(range(len(sorted_times)), sorted_times, marker='o')  # Plot waiting times
        plt.title('Figure 1: Waiting Times Over Request Sequence')  # Set title
        plt.xlabel('Request Number')  # Set x-axis label
        plt.ylabel('Waiting Time (seconds)')  # Set y-axis label
        plt.grid(True, which='both', linestyle='-', alpha=0.5)  # Add grid
        plt.minorticks_on()  # Enable minor ticks
        plt.ylim(bottom=0)  # Set y-axis lower limit
        plt.xlim(left=0)  # Set x-axis lower limit
        ax = plt.gca()  # Get current axes
        ax.spines['left'].set_position('zero')  # Position left spine at zero
        ax.spines['bottom'].set_position('zero')  # Position bottom spine at zero
        # Hide the top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    # Method to plot lift positions over time
    def _plot_lift_positions(self):
        """Plot lift positions over time"""
        plt.clf()
        
        for lift_idx in range(len(self.lift_positions_history[0])):  # Iterate over each lift
            positions = [pos[lift_idx] for pos in self.lift_positions_history]  # Get positions for the lift
            plt.plot(self.timestamps, positions, label=f'Lift {lift_idx + 1}')  # Plot positions
        plt.title('Figure 2: Lift Positions Over Time')  # Set title
        plt.xlabel('Time (seconds)')  # Set x-axis label
        plt.ylabel('Floor')  # Set y-axis label
        plt.legend()  # Show legend
        plt.grid(True, which='both', linestyle='-', alpha=0.5)  # Add grid
        plt.minorticks_on()  # Enable minor ticks
        plt.xlim(left=0)  # Set x-axis lower limit
        plt.ylim(bottom=0)  # Set y-axis lower limit
        ax = plt.gca()  # Get current axes
        ax.spines['left'].set_position(('data', 0))  # Position left spine at zero
        ax.spines['bottom'].set_position(('data', 0))  # Position bottom spine at zero
        # Hide the top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    # Method to plot total turnaround times (waiting + travel)
    def _plot_turnaround_times(self, completed_requests: List[Request]):
        plt.clf()
        
        # Calculate turnaround times
        turnaround_times = [(req.time_in_lift + req.time_on_floor) for req in completed_requests] 

        # Sort requests by creation time
        sorted_indices = sorted(range(len(completed_requests)), 
                              key=lambda k: completed_requests[k].time_created)
        # Sort turnaround times
        sorted_times = [turnaround_times[i] for i in sorted_indices]  
        
        plt.plot(range(len(sorted_times)), sorted_times, marker='o')  # Plot turnaround times
        plt.title('Figure 3: Total Turnaround Times Over Request Sequence')  # Set title
        plt.xlabel('Request Number')  # Set x-axis label
        plt.ylabel('Turnaround Time (seconds)')  # Set y-axis label
        plt.grid(True, which='both', linestyle='-', alpha=0.5)  # Add grid
        plt.minorticks_on()  # Enable minor ticks
        plt.ylim(bottom=0)  # Set y-axis lower limit
        plt.xlim(left=0)  # Set x-axis lower limit
        ax = plt.gca()  # Get current axes
        ax.spines['left'].set_position('zero')  # Position left spine at zero
        ax.spines['bottom'].set_position('zero')  # Position bottom spine at zero
        # Hide the top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    # Method to plot overall system statistics
    def _plot_system_statistics(self, completed_requests: List[Request], total_time: float):
        plt.clf()  
        
        # Get current figure and create axes
        fig = plt.gcf()
        ax1 = fig.add_subplot(111)
        
        # Calculate key metrics
        avg_waiting_time = np.mean([req.time_on_floor for req in completed_requests])  # Average waiting time
        avg_travel_time = np.mean([req.time_in_lift for req in completed_requests])  # Average travel time
        avg_turnaround = np.mean([req.time_in_lift + req.time_on_floor for req in completed_requests])  # Average turnaround time
        throughput = len(completed_requests) / total_time  # Calculate throughput
        
        # Create two separate sets of metrics
        time_metrics = ['Avg Waiting Time', 'Avg Travel Time', 'Avg Turnaround']  # Metrics labels
        time_values = [avg_waiting_time, avg_travel_time, avg_turnaround]  # Metrics values
        
        # Plot time metrics on the left y-axis
        bars1 = ax1.bar(time_metrics, time_values, color='skyblue')  # Create bar chart for time metrics
        ax1.set_ylabel('Time (seconds)')  # Set y-axis label
        ax1.set_ylim(bottom=0)  # Set y-axis lower limit
        
        # Create a second y-axis for throughput
        ax2 = ax1.twinx()  # Create a twin y-axis
        bars2 = ax2.bar(['Throughput'], [throughput], color='orange')  # Create bar chart for throughput
        ax2.set_ylabel('Requests per second')  # Set y-axis label for throughput
        ax2.set_ylim(bottom=0)  # Set y-axis lower limit
        
        # Set title and grid
        ax1.set_title('Figure 4: System Performance Metrics')  # Set title
        ax1.grid(True, which='both', linestyle='-', alpha=0.5)  # Add grid
        ax1.minorticks_on()  # Enable minor ticks
        
        # Add value labels on top of each bar
        for bar in bars1:
            height = bar.get_height()  # Get height of the bar
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}',  # Format height value
                    ha='center', va='bottom')  # Position the text
        
        for bar in bars2:
            height = bar.get_height()  # Get height of the bar
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}',  # Format height value
                    ha='center', va='bottom')  # Position the text
            
        plt.tight_layout()  # Adjust layout to prevent overlap
