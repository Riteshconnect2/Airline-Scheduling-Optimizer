# Airline Scheduling Optimizer — improved starter

## Run
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Fixes/features
- A resource cannot be assigned to overlapping flights.
- Minimum rest time and max work hours are checked between assignments.
- Per-flight pilot cost, cabin crew cost, and total cost are shown.
- Six heuristics can be compared: lowest-cost greedy, priority-first, shortest-flight-first, longest-flight-first, randomized feasible assignment, and balanced cost/workload.
- Best result is selected by: (1) most flights assigned, (2) lowest total cost, (3) fewest conflicts.

## Important
This is a demo/starter optimizer, not a certified airline dispatch system. It currently models one pilot and one cabin crew member per flight and matches qualifications to aircraft codes exactly. Real airline rules may require multiple pilots/cabin crew, duty-time rules, time zones, overnight/multi-day handling, aircraft assignment, and regulatory checks. Validate these before real use.
