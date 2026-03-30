# app_streamlit.py

import streamlit as st
import matplotlib.pyplot as plt
import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: 
        return None

from core_of_cpuShedular import (
    Process,
    simulate_fcfs,
    simulate_sjf,
    simulate_priority,
    simulate_rr,
    simulate_energy_efficient,
)

st.set_page_config(page_title="Energy-Efficient CPU Scheduling Simulator", layout="wide", page_icon="⚡")

# --- CUSTOM ANIMATIONS AND STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1b2a 0%, #1b263b 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    p, label, .stMarkdown, .stSelectbox label, .stMarkdown li {
        color: #e0f2f1 !important;
    }
    /* Fix dropdown option text mixing with background */
    ul[role="listbox"] li, div[data-baseweb="select"] span {
        color: #0d1b2a !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    .stButton>button {
        background: linear-gradient(45deg, #ff416c, #ff4b2b);
        color: white;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        padding: 0.5rem 1rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(255, 65, 108, 0.5);
        color: white;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    .stMetric label {
        display: block !important;
        text-align: center !important;
    }
    [data-testid="stMetricValue"] {
        color: #00e676 !important;
        text-align: center;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    .animated-title {
        animation: pulse 2.5s infinite;
        background: -webkit-linear-gradient(#f12711, #f5af19);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 2.8rem;
        margin-bottom: 0px;
        padding-bottom: 10px;
    }
    hr {
        border-top: 2px solid rgba(255,255,255,0.1) !important;
    }

    /* Hide Streamlit Default Header and Footer */
    header[data-testid="stHeader"] {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Custom Header Styles */
    .custom-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: rgba(15, 32, 39, 0.95);
        backdrop-filter: blur(10px);
        z-index: 99999;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 35px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border-bottom: 2px solid #ff4b2b;
    }
    .header-logo {
        color: #e0f2f1;
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .header-logo span {
        color: #ff4b2b;
    }
    .header-nav a {
        color: #a8dadc;
        text-decoration: none;
        margin-left: 25px;
        font-weight: 600;
        transition: color 0.3s;
    }
    .header-nav a:hover {
        color: #ff416c;
    }
    
    /* Make space for fixed header and footer */
    .block-container {
        padding-top: 80px !important;
        padding-bottom: 90px !important;
    }

    /* Custom Footer Styles */
    .custom-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(13, 27, 42, 0.95);
        color: #a8dadc;
        text-align: center;
        padding: 15px 0;
        font-size: 0.95rem;
        z-index: 99999;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    .custom-footer a {
        color: #00e676;
        text-decoration: none;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Inject Custom Header Navbar
st.markdown("""
<div class="custom-header">
    <div class="header-logo">⚙️ CPU<span>Scheduler</span></div>
    <div class="header-nav">
        <a href="." target="_self">Home</a>
        <a href="https://en.wikipedia.org/wiki/Scheduling_(computing)" target="_blank">Documentation</a>
        <a href="https://github.com" target="_blank">GitHub</a>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])
with col1:
    # URL for an awesome server/tech processor Lottie animation
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_tno6cg06.json"
    lottie_cpu = load_lottieurl(lottie_url)
    if lottie_cpu:
        st_lottie(lottie_cpu, height=130, key="cpu_animation")
    else:
        st.markdown("<h1 style='text-align:center;font-size:60px;'>⚡</h1>", unsafe_allow_html=True)
with col2:
    st.markdown("<h1 class='animated-title'>Energy-Efficient CPU<br>Scheduling Simulator</h1>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:left; font-size: 1.1rem; color: #a8dadc; margin-top: -15px; margin-bottom: 25px;">
This tool simulates classic CPU scheduling algorithms and a proposed <b>Energy-Efficient</b> scheduler.<br>
Compare performance using <b>waiting time, turnaround time, response time, CPU utilization & energy</b>.
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Simulation Settings")

algo = st.sidebar.selectbox(
    "Select Algorithm (for individual run)",
    [
        "FCFS",
        "SJF (Non-preemptive)",
        "Priority (Non-preemptive)",
        "Round Robin",
        "Energy-Efficient RR",
    ],
)

quantum = st.sidebar.number_input("Time Quantum (used in RR / EE-RR)", min_value=1, max_value=10, value=2)

st.sidebar.subheader("Process Input")

arrivals_str = st.sidebar.text_input("Arrival times", "0,2,4,5")
bursts_str = st.sidebar.text_input("Burst times", "7,4,1,4")
priorities_str = st.sidebar.text_input("Priorities", "2,1,3,2")

run_button = st.sidebar.button("Run Selected Algorithm")
compare_button = st.sidebar.button("Compare All Algorithms")

def parse_list(text):
    return [int(x.strip()) for x in text.split(",")]

# Process parsing
if run_button or compare_button:
    arrivals = parse_list(arrivals_str)
    bursts = parse_list(bursts_str)
    priorities = parse_list(priorities_str)

    if len(arrivals) != len(bursts):
        st.error("Arrival and Burst count must match!")
        st.stop()

    if len(priorities) != len(arrivals):
        priorities = [1] * len(arrivals)

    processes = [
        Process(f"P{i+1}", arrivals[i], bursts[i], priorities[i])
        for i in range(len(arrivals))
    ]

# --------------------------
# INDIVIDUAL RUN
# --------------------------
if run_button:
    if algo == "FCFS":
        result = simulate_fcfs(processes)
    elif algo == "SJF (Non-preemptive)":
        result = simulate_sjf(processes)
    elif algo == "Priority (Non-preemptive)":
        result = simulate_priority(processes)
    elif algo == "Round Robin":
        result = simulate_rr(processes, quantum=quantum)
    elif algo == "Energy-Efficient RR":
        result = simulate_energy_efficient(processes, quantum=quantum)

    st.subheader(f"🔧 Results for {result.algorithm}")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Avg Waiting Time", f"{result.avg_waiting_time:.2f}")
    col2.metric("Avg Turnaround Time", f"{result.avg_turnaround_time:.2f}")
    col3.metric("Avg Response Time", f"{result.avg_response_time:.2f}")
    col4.metric("CPU Utilization", f"{result.cpu_utilization:.2f}%")
    col5.metric("Total Energy", f"{result.total_energy:.2f} units")

    st.subheader("📍 Gantt Chart")

    fig, ax = plt.subplots(figsize=(10, 3))
    # Make plot background transparent with white text for dark mode
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.title.set_color('white')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    pids = sorted({e.pid for e in result.gantt if e.pid})
    pid_map = {p: i for i, p in enumerate(pids)}

    # Modern bar colors
    colors = ['#ff416c', '#f5af19', '#00e676', '#00bcd4', '#9c27b0']

    for entry in result.gantt:
        if entry.pid:
            c = colors[pid_map[entry.pid] % len(colors)]
            ax.barh(pid_map[entry.pid], entry.end - entry.start, left=entry.start, color=c, edgecolor='white', alpha=0.9)
            ax.text((entry.start + entry.end) / 2, pid_map[entry.pid], entry.pid, ha='center', va='center', color='black', fontweight='bold')

    ax.set_yticks(list(pid_map.values()))
    ax.set_yticklabels(pids)
    ax.set_xlabel("Time")
    ax.grid(True, alpha=0.2)
    st.pyplot(fig)

# --------------------------
# COMPARISON MODE
# --------------------------
if compare_button:
    results = [
        simulate_fcfs(processes),
        simulate_sjf(processes),
        simulate_priority(processes),
        simulate_rr(processes, quantum=quantum),
        simulate_energy_efficient(processes, quantum=quantum),
    ]

    st.subheader("📊 Algorithm Performance Comparison")

    data = {
        "Algorithm": [r.algorithm for r in results],
        "Avg Waiting Time": [round(r.avg_waiting_time, 2) for r in results],
        "Avg Turnaround Time": [round(r.avg_turnaround_time, 2) for r in results],
        "Avg Response Time": [round(r.avg_response_time, 2) for r in results],
        "CPU Utilization (%)": [round(r.cpu_utilization, 2) for r in results],
        "Total Energy": [round(r.total_energy, 2) for r in results],
    }

    st.table(data)

    best_turn = min(results, key=lambda r: r.avg_turnaround_time)
    best_energy = min(results, key=lambda r: r.total_energy)

    st.success(f"🏆 Fastest Algorithm (Min Turnaround Time): **{best_turn.algorithm}**")
    st.success(f"⚡ Most Energy Efficient Algorithm: **{best_energy.algorithm}**")

    st.subheader("⚡ Energy Usage Comparison")

    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    algos = [r.algorithm for r in results]
    energy = [r.total_energy for r in results]

    # Gradient-like color mapped list
    bar_colors = ['#ff4b2b', '#f5af19', '#00e676', '#00bcd4', '#9c27b0']
    bars = ax.bar(algos, energy, color=bar_colors[:len(algos)], edgecolor='white', alpha=0.9)
    ax.set_ylabel("Energy (units)")
    ax.set_xlabel("Algorithm")
    ax.set_title("Energy Consumption Comparison")

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 1, round(yval,1), ha='center', va='bottom', color='white', fontweight='bold')

    plt.xticks(rotation=30, ha='right')
    ax.grid(True, axis='y', alpha=0.2)
    fig.tight_layout()

    st.pyplot(fig)

# Inject Custom Footer
st.markdown("""
<div class="custom-footer">
    © 2026 Energy-Efficient CPU Scheduling Research. All Rights Reserved. &nbsp;|&nbsp; 
    Empowering Innovative Operating Systems Architecture &nbsp;|&nbsp; 
    <a href="." target="_self">Back to Top</a>
</div>
""", unsafe_allow_html=True)
