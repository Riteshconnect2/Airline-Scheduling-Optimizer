
import pandas as pd
import random


def to_minutes(value):
    parts = str(value).strip().split(":")
    if len(parts) != 2:
        raise ValueError("Time must use HH:MM format")

    h, m = map(int, parts)
    if not (0 <= h <= 23 and 0 <= m <= 59):
        raise ValueError("Invalid time")

    return h * 60 + m


def duration_hours(departure, arrival):
    start = to_minutes(departure)
    end = to_minutes(arrival)

    if end < start:
        end += 1440

    return (end - start) / 60.0


def in_window(start_text, end_text, flight_start, flight_end):
    start = to_minutes(start_text)
    end = to_minutes(end_text)

    if end < start:
        end += 1440

    for shift in (0, 1440):
        fs = flight_start + shift
        fe = flight_end + shift

        if fs >= start and fe <= end:
            return True

    return False


def qualification_matches(resource_qualification, aircraft):
    return (
        str(resource_qualification).strip().casefold()
        == str(aircraft).strip().casefold()
    )


def _can_assign(resource, key, worklog, aircraft,
                flight_start, flight_end, duration):

    if not qualification_matches(
        resource["qualification"], aircraft
    ):
        return False

    if not in_window(
        resource["available_from"],
        resource["available_to"],
        flight_start,
        flight_end
    ):
        return False

    max_hours = float(resource["max_work_hours"])

    if duration > max_hours:
        return False

    history = worklog.get(str(resource[key]), [])

    if sum(item["duration"] for item in history) + duration > max_hours:
        return False

    rest_hours = float(resource["min_rest_hours"])

    for item in history:
        prev_start = item["start"]
        prev_end = item["end"]

        if not (
            flight_end <= prev_start
            or flight_start >= prev_end
        ):
            return False

        if (
            flight_start >= prev_end
            and (flight_start - prev_end) / 60 < rest_hours
        ):
            return False

        if (
            prev_start >= flight_end
            and (prev_start - flight_end) / 60 < rest_hours
        ):
            return False

    return True


def _candidate_resources(resources, key, worklog, aircraft,
                         flight_start, flight_end, duration):

    candidates = []

    for _, row in resources.iterrows():
        resource = row.to_dict()

        if _can_assign(
            resource, key, worklog, aircraft,
            flight_start, flight_end, duration
        ):
            candidates.append(resource)

    return candidates


def _run(flights, pilots, crew, strategy="lowest_cost", seed=42):
    flights = pd.DataFrame(flights).copy()
    pilots = pd.DataFrame(pilots).copy()
    crew = pd.DataFrame(crew).copy()

    output = []
    conflicts = []
    pilot_work = {}
    crew_work = {}

    required_flights = {
        "flight_id", "origin", "destination",
        "departure", "arrival", "aircraft", "priority"
    }

    required_resource = {
        "qualification", "available_from", "available_to",
        "cost_per_hour", "max_work_hours", "min_rest_hours"
    }

    if not required_flights.issubset(flights.columns):
        raise ValueError(
            f"Flight data missing columns: "
            f"{sorted(required_flights - set(flights.columns))}"
        )

    if not ({"pilot_id"} | required_resource).issubset(pilots.columns):
        raise ValueError(
            f"Pilot data missing columns: "
            f"{sorted(({'pilot_id'} | required_resource) - set(pilots.columns))}"
        )

    if not ({"crew_id"} | required_resource).issubset(crew.columns):
        raise ValueError(
            f"Crew data missing columns: "
            f"{sorted(({'crew_id'} | required_resource) - set(crew.columns))}"
        )

    # Backward compatibility for existing flight data.
    if "required_crew" not in flights.columns:
        flights["required_crew"] = 1

    flights["_priority"] = (
        flights["priority"].astype(str).str.casefold()
        .map({"high": 0, "normal": 1, "low": 2})
        .fillna(1)
    )

    if strategy == "priority_first":
        flights = flights.sort_values(["_priority", "departure"])

    elif strategy == "shortest_first":
        flights["_duration"] = flights.apply(
            lambda f: duration_hours(f["departure"], f["arrival"]),
            axis=1
        )
        flights = flights.sort_values(["_duration", "_priority"])

    elif strategy == "longest_first":
        flights["_duration"] = flights.apply(
            lambda f: duration_hours(f["departure"], f["arrival"]),
            axis=1
        )
        flights = flights.sort_values(
            ["_duration", "_priority"],
            ascending=[False, True]
        )

    else:
        flights = flights.sort_values(["_priority", "departure"])

    rng = random.Random(seed)

    for _, f in flights.iterrows():
        flight_id = f["flight_id"]

        # Read required crew count for this flight.
        try:
            required_value = float(f["required_crew"])
            required_crew = int(required_value)

            if required_value != required_crew or required_crew < 1:
                raise ValueError

        except (TypeError, ValueError, OverflowError):
            conflicts.append({
                "Flight ID": flight_id,
                "Reason": "Required crew must be a positive whole number"
            })
            continue

        # Validate flight times.
        try:
            start = to_minutes(f["departure"])
            duration = duration_hours(f["departure"], f["arrival"])
            end = start + duration * 60

        except (ValueError, TypeError, AttributeError, KeyError):
            conflicts.append({
                "Flight ID": flight_id,
                "Reason": "Invalid departure/arrival time. Use HH:MM."
            })
            continue

        if duration <= 0:
            conflicts.append({
                "Flight ID": flight_id,
                "Reason": "Flight duration must be positive"
            })
            continue

        # Find all eligible pilots and cabin crew.
        pc = _candidate_resources(
            pilots, "pilot_id", pilot_work,
            f["aircraft"], start, end, duration
        )

        cc = _candidate_resources(
            crew, "crew_id", crew_work,
            f["aircraft"], start, end, duration
        )

        # Apply assignment strategy.
        if strategy == "randomized":
            rng.shuffle(pc)
            rng.shuffle(cc)

        elif strategy == "balanced":
            pc.sort(key=lambda r: (
                len(pilot_work.get(str(r["pilot_id"]), [])),
                float(r["cost_per_hour"])
            ))

            cc.sort(key=lambda r: (
                len(crew_work.get(str(r["crew_id"]), [])),
                float(r["cost_per_hour"])
            ))

        else:
            pc.sort(key=lambda r: (
                float(r["cost_per_hour"]),
                str(r["pilot_id"])
            ))

            cc.sort(key=lambda r: (
                float(r["cost_per_hour"]),
                str(r["crew_id"])
            ))

        # IMPORTANT: require the full cabin crew complement.
        if not pc or len(cc) < required_crew:
            missing = []

            if not pc:
                missing.append("eligible pilot")

            if len(cc) < required_crew:
                missing.append(
                    f"{required_crew} cabin crew required, "
                    f"only {len(cc)} eligible"
                )

            reason = (
                "Insufficient resources: "
                + "; ".join(missing)
                + ". Check qualifications, availability, "
                  "overlapping duties, rest and work limits."
            )

            output.append({
                "Flight ID": flight_id,
                "Route": f'{f["origin"]} → {f["destination"]}',
                "Departure": f["departure"],
                "Arrival": f["arrival"],
                "Aircraft": f["aircraft"],
                "Required Crew": required_crew,
                "Pilot ID": "—",
                "Cabin Crew ID": "—",
                "Duration (hrs)": round(duration, 2),
                "Pilot Cost (₹)": 0.0,
                "Cabin Crew Cost (₹)": 0.0,
                "Cost (₹)": 0.0,
                "Status": "UNASSIGNED"
            })

            conflicts.append({
                "Flight ID": flight_id,
                "Reason": reason
            })
            continue

        # Select one pilot and the required number of crew members.
        pilot = pc[0]
        selected_crew = cc[:required_crew]

        pilot_id = str(pilot["pilot_id"])
        crew_ids = [
            str(member["crew_id"])
            for member in selected_crew
        ]

        pilot_cost = float(pilot["cost_per_hour"]) * duration

        # Cost includes every assigned cabin crew member.
        crew_cost = sum(
            float(member["cost_per_hour"]) * duration
            for member in selected_crew
        )

        total_cost = pilot_cost + crew_cost

        output.append({
            "Flight ID": flight_id,
            "Route": f'{f["origin"]} → {f["destination"]}',
            "Departure": f["departure"],
            "Arrival": f["arrival"],
            "Aircraft": f["aircraft"],
            "Required Crew": required_crew,
            "Pilot ID": pilot_id,
            "Cabin Crew ID": ", ".join(crew_ids),
            "Duration (hrs)": round(duration, 2),
            "Pilot Cost (₹)": round(pilot_cost, 2),
            "Cabin Crew Cost (₹)": round(crew_cost, 2),
            "Cost (₹)": round(total_cost, 2),
            "Status": "ASSIGNED"
        })

        # Record duties for every assigned resource.
        pilot_work.setdefault(pilot_id, []).append({
            "start": start,
            "end": end,
            "duration": duration
        })

        for member in selected_crew:
            crew_id = str(member["crew_id"])

            crew_work.setdefault(crew_id, []).append({
                "start": start,
                "end": end,
                "duration": duration
            })

    columns = [
        "Flight ID", "Route", "Departure", "Arrival", "Aircraft",
        "Required Crew", "Pilot ID", "Cabin Crew ID",
        "Duration (hrs)", "Pilot Cost (₹)",
        "Cabin Crew Cost (₹)", "Cost (₹)", "Status"
    ]

    return pd.DataFrame(output, columns=columns), conflicts


ALGORITHMS = {
    "Lowest-cost greedy": "lowest_cost",
    "Priority-first greedy": "priority_first",
    "Shortest-flight-first": "shortest_first",
    "Longest-flight-first": "longest_first",
    "Randomized feasible assignment": "randomized",
    "Balanced cost/workload": "balanced",
}


def optimize_schedule(flights, pilots, crew, strategy="lowest_cost"):
    if strategy not in set(ALGORITHMS.values()):
        strategy = "lowest_cost"

    return _run(flights, pilots, crew, strategy=strategy)


def compare_algorithms(flights, pilots, crew):
    rows = []
    schedules = {}

    for name, strategy in ALGORITHMS.items():
        schedule, conflicts = optimize_schedule(
            flights, pilots, crew, strategy
        )

        assigned = schedule[schedule["Status"] == "ASSIGNED"]
        total_cost = float(assigned["Cost (₹)"].sum())

        rows.append({
            "Algorithm": name,
            "Assigned Flights": int(len(assigned)),
            "Unassigned Flights": int(
                (schedule["Status"] == "UNASSIGNED").sum()
            ),
            "Total Cost (₹)": round(total_cost, 2),
            "Conflicts": len(conflicts),
            "Cost per Assigned Flight (₹)": (
                round(total_cost / len(assigned), 2)
                if len(assigned) else 0.0
            )
        })

        schedules[name] = schedule

    comparison = pd.DataFrame(rows).sort_values(
        ["Unassigned Flights", "Total Cost (₹)", "Conflicts"],
        ascending=[True, True, True]
    ).reset_index(drop=True)

    best = (
        comparison.iloc[0]["Algorithm"]
        if not comparison.empty else None
    )

    return comparison, schedules, best
