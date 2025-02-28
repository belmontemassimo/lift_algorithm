The Lift Simulation System is a Python-based project designed to simulate elevator operations in a multi-lift building environment. It models passenger requests, lift movements, and scheduling algorithms, providing real-time visualization and performance analytics. This project is ideal for studying elevator system efficiency, testing scheduling algorithms, or educational purposes.

**Features:**
- Multi-Lift Management: Simulate multiple lifts with configurable speed, acceleration, and capacity.
- Request Handling: Generate and process passenger requests with realistic weight modeling.
- Scheduling Algorithms: Includes FCFS, SCAN, LOOK, MYLIFT, and a custom OtherLift algorithm, with extensibility for new strategies.
- Graphical User Interface (GUI): Visualize lift movements and floor requests using Tkinter.
- Monitoring Panel: Real-time stats display via wxPython (position, speed, state, weight).
- Analytics: Generate graphs for waiting times, turnaround times, lift positions, and system performance using Matplotlib.
- Modular Design: Cleanly separated components for easy modification and expansion.

**Project Structure:**

lift-simulation/  
├── `gui.py`              # Tkinter-based GUI for visualizing lift movements  
├── `lift.py`             # Core Lift class with movement and state logic  
├── `liftmanager.py`      # Manages multiple lifts and their updates  
├── `main.py`             # Main simulation runner  
├── `monitoring.py`       # wxPython-based monitoring interface  
├── `request.py`          # Request class for passenger trip modeling  
├── `algorithms.py`       # Scheduling algorithms (FCFS, SCAN, LOOK, MYLIFT, PATHFINDER)  
├── `graph.py`            # Analytics and graphing with Matplotlib  
├── `extenders.py`        # Utility functions (DeltaTime, weight distribution)  
├── `generator.py`        # Generates samples of requests  
└── `README.md`           # This file  

**Prerequisites:**
- Python 3.9+

- Dependencies:
    - matplotlib (for analytics graphs)
    - numpy (for statistical computations)
    - wxPython (for monitoring GUI)
    - tkinter (for visualization GUI, typically included with Python)

**Installation:**
1. Clone the repository:
```sh
git clone https://github.com/belmontemassimo/lift_algorithm.git; cd lift_algorithm
```
3. Install required packages:
```sh
pip install wxPython, matplotlib, numpy, scipy
```
5. Run the simulation:
```sh
python simulation.py
```


**Usage:**
Run simulation.py to start the simulation with default settings:
python simulation.py

- GUI: A Tkinter window shows lift positions and floor requests.
- Monitoring: A wxPython window displays real-time lift stats (position, speed, state, etc.).
- Analytics: After completion, Matplotlib plots performance metrics.


**Configuration:**
Modify simulation.py to adjust:
- Lift Parameters: `MAX_SPEED`, `ACCELERATION`, `CAPACITY`, `WAITING_TIME`.
- GUI Toggle: Set isGUI=False in run_simulation() to disable visualization.
- monitoring Interface
- Set number of lifts, floors, simulation speed, and algorithm before clicking "Start".
- Displays live updates every 40ms.

**Algorithms:**
The system supports multiple scheduling strategies in algorithms.py:
- FCFS (First Come, First Served): Processes requests in order of arrival.
- SCAN: Moves lifts in one direction, servicing requests until the end, then reverses.
- LOOK: Similar to SCAN but reverses direction when no requests remain in the current direction.
- MYLIFT: Batches requests with weight-based prioritization.
- PATHFINDER: Custom algorithm optimizing multi-request fulfillment:
Assigns requests to all lifts, prioritizing batch efficiency.
Lifts maintain direction mid-trip, changing only when idle or waiting.
Idle lifts take the closest request; moving lifts batch requests along their path.
To switch algorithms, adjust the monitoring UI or modify algorithm.set_algorithm() in main.py.

**Analytics:**
Post-simulation graphs (via `graph.py`):

- Waiting Times: Time from request creation to lift pickup.
- Lift Positions: Tracks each lift’s floor over time.
- Turnaround Times: Total time from request creation to completion.
- System Statistics: Average waiting time, travel time, turnaround time, and throughput.

**Extending the Project:**
- New Algorithms: Add classes to `algorithms.py` and register them in `get_algorithms()`.
- Custom Requests: Use request.py’s `double_normal_distribution` for realistic weights or modify request generation.
- UI Enhancements: Expand gui.py or `monitoring.py` for additional features.


**Contributing:**
Contributions are welcome! Fork the repo, make changes, and submit a pull request. Focus areas:
- Bug fixes
- New algorithms
- UI improvements
- Performance optimization

**License**
This project is licensed under the MIT License. See LICENSE for details.
