import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from scipy import stats
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
        # Clear any existing figures to avoid duplicates
        plt.close('all')
        
        # Create each plot with a specific figure number and name
        plt.figure(1, figsize=(10, 6))
        self._plot_waiting_times(completed_requests)
        
        plt.figure(2, figsize=(12, 6))
        self._plot_lift_positions()
        
        plt.figure(3, figsize=(10, 6))
        self._plot_turnaround_times(completed_requests)
        
        # Create figure for system statistics (figure 4)
        plt.figure(4, figsize=(10, 6))
        self._plot_system_statistics(completed_requests, total_time)
        
        # Create figure for waiting time vs distance (figure 5)
        plt.figure(5, figsize=(12, 10))
        self._plot_waiting_time_vs_distance(completed_requests)
        
        plt.show()

# plot1
    def _plot_waiting_times(self, completed_requests: List[Request]):
        """Plot waiting times for each request"""
        # Use current figure
        plt.clf()  # Clear the current figure
        
        waiting_times = [req.time_on_floor for req in completed_requests]
        # Sort requests by creation time
        sorted_indices = sorted(range(len(completed_requests)), 
                              key=lambda k: completed_requests[k].time_created)
        sorted_times = [waiting_times[i] for i in sorted_indices]
        
        plt.plot(range(len(sorted_times)), sorted_times, marker='o')
        plt.title('Figure 1: Waiting Times Over Request Sequence')
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
        # Use current figure
        plt.clf()  # Clear the current figure
        
        for lift_idx in range(len(self.lift_positions_history[0])):
            positions = [pos[lift_idx] for pos in self.lift_positions_history]
            plt.plot(self.timestamps, positions, label=f'Lift {lift_idx + 1}')
        plt.title('Figure 2: Lift Positions Over Time')
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
        # Use current figure
        plt.clf()  # Clear the current figure
        
        turnaround_times = [(req.time_in_lift + req.time_on_floor) for req in completed_requests]
        # Sort requests by creation time
        sorted_indices = sorted(range(len(completed_requests)), 
                              key=lambda k: completed_requests[k].time_created)
        sorted_times = [turnaround_times[i] for i in sorted_indices]
        
        plt.plot(range(len(sorted_times)), sorted_times, marker='o')
        plt.title('Figure 3: Total Turnaround Times Over Request Sequence')
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
        # Use current figure
        plt.clf()  # Clear the current figure
        
        # Get current figure and create axes
        fig = plt.gcf()
        ax1 = fig.add_subplot(111)
        
        # Calculate key metrics
        avg_waiting_time = np.mean([req.time_on_floor for req in completed_requests])
        avg_travel_time = np.mean([req.time_in_lift for req in completed_requests])
        avg_turnaround = np.mean([req.time_in_lift + req.time_on_floor for req in completed_requests])
        throughput = len(completed_requests) / total_time
        
        # Create two separate sets of metrics
        time_metrics = ['Avg Waiting Time', 'Avg Travel Time', 'Avg Turnaround']
        time_values = [avg_waiting_time, avg_travel_time, avg_turnaround]
        
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
        ax1.set_title('Figure 4: System Performance Metrics')
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

# plot5 - Simple plot to show correlation between waiting time and distance
    def _plot_waiting_time_vs_distance(self, completed_requests: List[Request]):
        """Plot distance vs waiting time to visualize correlation"""
        # Use current figure
        plt.clf()  # Clear the current figure
        
        # Filter requests that have lift position recorded
        valid_requests = [req for req in completed_requests if req.lift_position_on_request is not None]
        
        if not valid_requests:
            print("No requests with lift position data available")
            return
            
        # Calculate distances and get waiting times
        distances = []
        waiting_times = []
        request_ids = []  # To use request creation time as identifier
        
        for i, req in enumerate(valid_requests):
            if req.lift_position_on_request is not None:  # Extra check to satisfy type checker
                distances.append(abs(req.request_floor - req.lift_position_on_request))
                waiting_times.append(req.time_on_floor)
                # Use request index as an identifier
                request_ids.append(i + 1)  # Start from 1 instead of 0 for clearer labeling
        
        # Convert to numpy arrays for better compatibility
        distances_array = np.array(distances)
        waiting_times_array = np.array(waiting_times)
        
        # Create a scatter plot with waiting times on x-axis and distances on y-axis
        plt.scatter(waiting_times_array, distances_array, alpha=0.7, s=50, c='skyblue', edgecolors='blue')
        
        # Annotate each point with request ID
        for i, req_id in enumerate(request_ids):
            plt.annotate(str(req_id), 
                        (waiting_times_array[i], distances_array[i]),
                        xytext=(5, 5),  # Small offset to make labels readable
                        textcoords='offset points',
                        fontsize=8)
        
        # Add a trend line using linear regression
        if len(distances_array) > 1:
            # Calculate regression line
            z = np.polyfit(waiting_times_array, distances_array, 1)
            p = np.poly1d(z)
            
            # Create x values for the line
            x_trend = np.linspace(np.min(waiting_times_array) * 0.9, np.max(waiting_times_array) * 1.1, 100)
            
            # Plot the trend line
            plt.plot(x_trend, p(x_trend), 'r-', linewidth=2)
            
            # Calculate correlation coefficient
            correlation = np.corrcoef(waiting_times_array, distances_array)[0, 1]
            r_squared = correlation ** 2
            
            # Annotate with statistics
            plt.annotate(f"Slope: {z[0]:.4f}\nIntercept: {z[1]:.4f}\nR²: {r_squared:.4f}",
                        xy=(0.05, 0.95), xycoords='axes fraction',
                        bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.8),
                        fontsize=10)
            
            # Add title based on correlation strength
            if r_squared > 0.8:
                correlation_strength = "Strong"
                color = "green"
            elif r_squared > 0.5:
                correlation_strength = "Moderate"
                color = "orange"
            else:
                correlation_strength = "Weak"
                color = "red"
                
            plt.title(f"Figure 5: Waiting Time vs Distance Correlation ({correlation_strength})", color=color, fontsize=14)
        else:
            plt.title("Figure 5: Waiting Time vs Distance (Insufficient data)", fontsize=14)
        
        # Add labels
        plt.xlabel("Waiting Time (seconds)", fontsize=12)
        plt.ylabel("Distance (floors)", fontsize=12)
        
        # Add grid
        plt.grid(True, alpha=0.3)
        
        # Set axes to start from origin if possible
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        
        # Add a reference line if there's a theoretical relationship
        if len(distances_array) > 1:
            # Calculate average speed (distance/time) to see if it matches expectations
            avg_speed = np.mean(distances_array / waiting_times_array)
            ideal_line_x = np.linspace(0, np.max(waiting_times_array) * 1.1, 10)
            ideal_line_y = ideal_line_x * avg_speed
            plt.plot(ideal_line_x, ideal_line_y, 'g--', linewidth=1, alpha=0.5, 
                    label=f"Expected (v={avg_speed:.2f} floors/s)")
            plt.legend(loc='lower right')
            
        # Add a legend explaining the point labels
        plt.figtext(0.02, 0.02, "Note: Points are labeled with request number (1-indexed)", 
                  fontsize=8, bbox=dict(facecolor='white', alpha=0.8))
