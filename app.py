
import streamlit as st
import pandas as pd

from optimizer import optimize_schedule, compare_algorithms, ALGORITHMS
from data import default_flights, default_pilots, default_crew


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Airline Scheduling Optimizer",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# BLUE & WHITE UI THEME
# --------------------------------------------------
st.markdown("""
<style>
/* Main application */
.stApp {
    background: linear-gradient(180deg, #f3f8ff 0%, #ffffff 48%);
    color: #172b4d;
}

[data-testid="stHeader"] {
    background: rgba(243, 248, 255, 0.95);
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2.5rem;
    max-width: 1600px;
}

/* Text visibility */
 h2, h3, h4 {
    color: #123b70 !important;
    font-weight: 750 !important;
}
 

 label, li, .stMarkdown, .stCaption {
    color: #334966;
}

[data-testid="stCaptionContainer"] p {
    color: #536b87 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #123b70 0%, #0757a6 100%);
}

[data-testid="stSidebar"] * {
    color: #ffffff;
}

[data-testid="stSidebar"] [data-baseweb="select"] *,
[data-testid="stSidebar"] input {
    color: #172b4d !important;
    background-color: #ffffff;
}

[data-testid="stSidebar"] [data-baseweb="select"] {
    background-color: #ffffff;
    border-radius: 9px;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #e1edff !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #d5e5fa;
    border-top: 4px solid #1672ce;
    padding: 18px 20px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(24, 74, 130, 0.07);
}

[data-testid="stMetricLabel"] {
    color: #536b87 !important;
    font-weight: 650;
}

[data-testid="stMetricValue"] {
    color: #123b70 !important;
    font-weight: 800;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    border-radius: 9px;
    font-weight: 650;
    min-height: 42px;
    transition: all 0.2s ease;
}

.stButton > button[kind="secondary"] {
    background: #1266b5;
    color: #ffffff;
    border: 1px solid #1266b5;
}

.stButton > button[kind="primary"]:hover {
    background: #084a8c;
    border-color: #084a8c;
    color: #ffffff;
}

.stDownloadButton > button {
    background: #e8f2ff;
    color: #104f91;
    border: 1px solid #bdd7f5;
}

.stDownloadButton > button:hover {
    background: #d4e8ff;
    color: #103c70;
    border-color: #7eb2ed;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 2px solid #d8e7f8;
}

.stTabs [data-baseweb="tab"] {
    background: #eaf2fc;
    border-radius: 9px 9px 0 0;
    color: #ffffff !important;
    padding: 12px 18px;
    font-weight: 650;
}

.stTabs [aria-selected="true"] {
    background: #1266b5 !important;
    color: #ffffff !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: #1266b5;
}

/* Dataframes and editable tables */
[data-testid="stDataFrame"],
[data-testid="stDataEditor"] {
    border: 1px solid #d5e3f4;
    border-radius: 11px;
    overflow: hidden;
    background: #ffffff;
}

[data-testid="stDataFrame"] [role="columnheader"],
[data-testid="stDataEditor"] [role="columnheader"] {
    background: #dcecff !important;
    color: #123b70 !important;
    font-weight: 750 !important;
}

[data-testid="stDataFrame"] [role="gridcell"],
[data-testid="stDataEditor"] [role="gridcell"] {
    color: #263c56 !important;
}

[data-testid="stDataFrame"] [role="row"]:nth-child(even) [role="gridcell"] {
    background: #f2f7fd;
}

/* Inputs */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTimeInput input,
.stTextArea textarea {
    color: #172b4d !important;
    background: #ffffff !important;
    border: 1px solid #c7d8ec;
    border-radius: 8px;
}

[data-baseweb="select"] > div {
    background-color: #ffffff;
    border-color: #c7d8ec;
}

[data-baseweb="select"] * {
    color: #172b4d;
}

/* Messages */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Section separators */
hr {
    border-color: #d9e7f7;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div style="
    background: linear-gradient(115deg, #103b70, #1672ce);
    padding: 28px 30px;
    border-radius: 18px;
    margin-bottom: 22px;
    box-shadow: 0 8px 24px rgba(18, 59, 112, 0.16);
">
    <div style="font-size: 13px; color: #d7eaff;
                letter-spacing: 2px; font-weight: 700;">
        FLIGHT OPERATIONS MANAGEMENT
    </div>
    <h1 style="
        margin: 8px 0 0 0;
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        line-height: 1.4;
    ">
        ✈️ Airline Scheduling Optimizer
    </h1>
     
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DATA INITIALIZATION
# --------------------------------------------------
if "flights" not in st.session_state:
    st.session_state.flights = default_flights()

if "pilots" not in st.session_state:
    st.session_state.pilots = default_pilots()

if "crew" not in st.session_state:
    st.session_state.crew = default_crew()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Control Center")
    st.caption("Configure and run your scheduling engine.")

    selected_name = st.selectbox(
        "Optimization Algorithm",
        list(ALGORITHMS.keys()),
        index=0,
    )

    selected_strategy = ALGORITHMS[selected_name]

    st.markdown("---")
    st.markdown("### Scheduling rules")
    st.caption(
        "The optimizer should respect resource availability, "
        "flight overlaps, qualifications and required rest "
        "according to your implementation."
    )

    run = st.button(
        "🚀 Generate Schedule",
        type="primary",
        use_container_width=True,
    )

    compare = st.button(
        "📊 Compare Algorithms",
        use_container_width=True,
    )

    st.markdown("---")
    st.caption("Airline Scheduling Optimizer | Dashboard")


# --------------------------------------------------
# NAVIGATION TABS
# --------------------------------------------------
tabs = st.tabs([
    "📊 Operations",
    "✈️ Flights",
    "👨‍✈️ Pilots",
    "🧑‍✈️ Cabin Crew",
    "📈 Algorithm Comparison",
])


# --------------------------------------------------
# FLIGHT REGISTER
# --------------------------------------------------
with tabs[1]:
    st.subheader("✈️ Flight Register")
    st.caption("Add, edit or remove flights before generating a schedule.")

    st.session_state.flights = st.data_editor(
        st.session_state.flights,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="flight_editor",
    )


# --------------------------------------------------
# PILOT REGISTER
# --------------------------------------------------
with tabs[2]:
    st.subheader("👨‍✈️ Pilot Resource Register")
    st.caption("Manage pilot qualifications, availability and work limits.")

    st.session_state.pilots = st.data_editor(
        st.session_state.pilots,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="pilot_editor",
    )


# --------------------------------------------------
# CABIN CREW REGISTER
# --------------------------------------------------
with tabs[3]:
    st.subheader("🧑‍✈️ Cabin Crew Register")
    st.caption("Manage crew availability, qualifications and duty limits.")

    st.session_state.crew = st.data_editor(
        st.session_state.crew,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="crew_editor",
    )


# --------------------------------------------------
# TABLE STYLING HELPER
# --------------------------------------------------
def style_table(df):
    """Return a readable, blue-themed pandas table style."""

    styler = (
        df.style
        .set_properties(**{
            "color": "#263c56",
            "background-color": "#ffffff",
            "border-color": "#dce7f5",
            "text-align": "left",
        })
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("background-color", "#dcecff"),
                    ("color", "#123b70"),
                    ("font-weight", "bold"),
                    ("padding", "10px"),
                    ("border", "1px solid #c7d9ef"),
                ],
            },
            {
                "selector": "td",
                "props": [
                    ("padding", "8px"),
                    ("border-bottom", "1px solid #e4edf8"),
                ],
            },
            {
                "selector": "table",
                "props": [
                    ("border-collapse", "collapse"),
                    ("width", "100%"),
                ],
            },
        ])
    )

    if "Status" in df.columns:
        def color_status(value):
            if value == "ASSIGNED":
                return "color: #087443; font-weight: bold;"
            if value == "UNASSIGNED":
                return "color: #b42318; font-weight: bold;"
            return "color: #263c56;"

        styler = styler.map(color_status, subset=["Status"])

    return styler


# --------------------------------------------------
# OPTIMIZATION
# --------------------------------------------------
if run or "schedule" not in st.session_state:
    schedule, conflicts = optimize_schedule(
        st.session_state.flights,
        st.session_state.pilots,
        st.session_state.crew,
        selected_strategy,
    )

    st.session_state.schedule = schedule
    st.session_state.conflicts = conflicts
    st.session_state.selected_algorithm_name = selected_name

if compare or "comparison" not in st.session_state:
    comparison, schedules, best = compare_algorithms(
        st.session_state.flights,
        st.session_state.pilots,
        st.session_state.crew,
    )

    st.session_state.comparison = comparison
    st.session_state.algorithm_schedules = schedules
    st.session_state.best_algorithm = best


# --------------------------------------------------
# OPERATIONS DASHBOARD
# --------------------------------------------------
schedule = st.session_state.schedule
conflicts = st.session_state.conflicts

with tabs[0]:
    st.subheader("📊 Operations Overview")
    st.caption(
        f"Active algorithm: "
        f"{st.session_state.get('selected_algorithm_name', selected_name)}"
    )

    total_flights = len(st.session_state.flights)

    assigned = (
        int(schedule["Status"].eq("ASSIGNED").sum())
        if not schedule.empty and "Status" in schedule.columns
        else 0
    )

    unassigned = (
        int(schedule["Status"].eq("UNASSIGNED").sum())
        if not schedule.empty and "Status" in schedule.columns
        else 0
    )

    total_cost = (
        schedule.loc[
            schedule["Status"].eq("ASSIGNED"), "Cost (₹)"
        ].sum()
        if not schedule.empty
        and {"Status", "Cost (₹)"}.issubset(schedule.columns)
        else 0
    )

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Total Flights", f"{total_flights:,}")
    m2.metric("Assigned Flights", f"{assigned:,}")
    m3.metric("Unassigned Flights", f"{unassigned:,}")
    m4.metric("Total Assigned Cost", f"₹{total_cost:,.2f}")

    st.markdown("---")
    st.subheader("🗓️ Optimized Flight Schedule")

    if schedule.empty:
        st.info("No schedule data available. Check your input data and optimizer.")
    else:
        st.dataframe(
            style_table(schedule),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Download Schedule CSV",
            data=schedule.to_csv(index=False).encode("utf-8-sig"),
            file_name="optimized_schedule.csv",
            mime="text/csv",
        )

    if conflicts:
        st.warning(
            "Some flights could not be assigned. Review the details below."
        )
        conflict_df = pd.DataFrame(conflicts)

        st.dataframe(
            style_table(conflict_df),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.success("No conflicts were reported by the optimizer.")


# --------------------------------------------------
# ALGORITHM COMPARISON
# --------------------------------------------------
with tabs[4]:
    st.subheader("📈 Algorithm Performance Comparison")

    st.markdown("""
    Compare scheduling methods using the current flight and resource data.
    The ranking prioritizes fewer unassigned flights, lower assigned cost,
    and fewer reported conflicts.
    """)

    comparison = st.session_state.comparison

    if comparison is None or comparison.empty:
        st.info("No comparison results are available yet.")
    else:
        st.dataframe(
            style_table(comparison),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Download Comparison CSV",
            data=comparison.to_csv(index=False).encode("utf-8-sig"),
            file_name="algorithm_comparison.csv",
            mime="text/csv",
        )

    best = st.session_state.best_algorithm

    if best:
        st.markdown("---")
        st.subheader("🏆 Best Performing Algorithm")
        st.success(f"Best result for the current data: {best}")

        best_schedule = st.session_state.algorithm_schedules[best]

        st.dataframe(
            style_table(best_schedule),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Download Best Schedule",
            data=best_schedule.to_csv(index=False).encode("utf-8-sig"),
            file_name="best_algorithm_schedule.csv",
            mime="text/csv",
        )

    st.caption(
        "Results depend on your input data, constraints and algorithm "
        "implementation. The best-performing algorithm may change."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#60758f; padding:10px;">
        ✈️ <b>Airline Scheduling Optimizer</b><br>
        <small>Intelligent scheduling • Efficient resource utilization • Cost optimization</small>
    </div>
    """,
    unsafe_allow_html=True,
)
