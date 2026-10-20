# ✈️ Airline Scheduling Optimizer

A Python-based application that assigns pilots and cabin crew to flights while estimating personnel costs and comparing six scheduling algorithms. It checks crew availability and scheduling constraints, displays optimized schedules, and supports CSV downloads for further analysis.

### 1. Operations Overview

Displays total flights, assigned flights, unassigned flights, total assigned cost, and the optimized flight schedule.

![Operations Overview](screenshots/operations-overview.png)

### 2. Optimized Flight Schedule

Shows flight routes, departure and arrival times, aircraft, required crew, assigned pilot and cabin crew, flight duration, cost breakdown, and assignment status.

![Optimized Flight Schedule](screenshots/optimized-flight-schedule.png)

### 3. Algorithm Performance Comparison

Compares six scheduling algorithms based on assigned flights, unassigned flights, total cost, conflicts, and cost per assigned flight.

![Algorithm Comparison](screenshots/algorithm-comparison.png)

## 🚀 Features

- Generate schedules using six different scheduling algorithms.
- Assign pilots and cabin crew based on availability and qualifications.
- Check overlapping flights, minimum rest periods, and maximum work hours.
- Calculate pilot cost, cabin crew cost, and total personnel cost.
- Display assigned and unassigned flights.
- Compare algorithm performance using a common set of metrics.
- Export schedules and reports as CSV files.
- Identify scheduling conflicts and evaluate assignment results.

## 🧠 Scheduling Algorithms

1. **Lowest-Cost Greedy** — prioritizes lower-cost feasible assignments.
2. **Priority-First Greedy** — prioritizes flights according to their priority.
3. **Shortest-Flight-First** — schedules shorter-duration flights first.
4. **Longest-Flight-First** — schedules longer-duration flights first.
5. **Randomized Feasible Assignment** — explores feasible assignments using random selection.
6. **Balanced Cost/Workload** — considers both assignment cost and workload balance.

The optimizer ranks results by the number of flights assigned, followed by total cost and reported conflicts.

## 🛠️ Tech Stack

- **Language:** Python
- **Application Interface:** Streamlit
- **Data Export:** CSV
- **Environment:** Python virtual environment

## 📂 Project Structure

```text
Airline-Scheduling-Optimizer/
├── app.py
├── data.py
├── optimizer.py
├── requirements.txt
├── README.md
└── screenshots/
    ├── operations-overview.png
    ├── optimized-flight-schedule.png
    └── algorithm-comparison.png
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Riteshconnect2/Airline-Scheduling-Optimizer.git
cd Airline-Scheduling-Optimizer
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the environment

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Run the application

```powershell
streamlit run app.py
```

Open the local URL displayed in your terminal to access the application.

## 📊 Algorithm Evaluation

The following results are from the displayed sample run.

| Algorithm | Assigned Flights | Unassigned Flights | Total Cost (₹) | Conflicts | Cost per Assigned Flight (₹) |
|---|---:|---:|---:|---:|---:|
| Shortest-Flight-First | 11 | 9 | 391,945.83 | 9 | 35,631.44 |
| Longest-Flight-First | 11 | 9 | 502,400.00 | 9 | 45,672.73 |
| Lowest-Cost Greedy | 11 | 9 | 508,158.33 | 9 | 46,196.21 |
| Priority-First Greedy | 11 | 9 | 508,158.33 | 9 | 46,196.21 |
| Balanced Cost/Workload | 11 | 9 | 508,658.33 | 9 | 46,241.67 |
| Randomized Feasible Assignment | 11 | 9 | 510,870.83 | 9 | 46,442.80 |

**Observation:** In this sample run, Shortest-Flight-First has the lowest reported total cost. All six strategies assign 11 flights and leave 9 unassigned. The results may change when the input data or randomized assignments change.

## ⚠️ Limitations

This project is an educational prototype, not a certified airline dispatch system. It currently models one pilot and one cabin crew member per flight and matches qualifications to aircraft codes exactly.

Real airline scheduling may require multiple pilots and cabin crew, detailed regulatory duty-time limits, time-zone handling, overnight and multi-day scheduling, aircraft assignment, and additional operational checks.

## 🔮 Future Enhancements

- Implement linear programming and genetic algorithms.
- Add real-time disruption handling and schedule re-optimization.
- Support multiple pilots and cabin crew per flight.
- Improve regulatory and duty-time validation.
- Integrate a database for persistent storage.
- Test with larger and more realistic airline datasets.

## 📌 Disclaimer

This project is intended for educational and demonstration purposes only. Its output must not be used for real airline operations without extensive validation, expert review, and regulatory compliance checks.
