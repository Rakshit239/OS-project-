# app_streamlit.py

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'
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

# --- COMPLETE UI OVERHAUL: WHITE & GOLD LUXURY THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ===== ANIMATED BACKGROUND ===== */
    .stApp {
        background: #faf9f6;
        background-attachment: fixed;
        overflow-x: hidden;
    }

    /* ===== MESH GRADIENT BLOBS ===== */
    .mesh-bg {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .blob {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.5;
        mix-blend-mode: multiply;
    }
    .blob-1 {
        width: 600px; height: 600px;
        background: radial-gradient(circle, rgba(212,175,55,0.45), transparent 70%);
        top: -10%; left: -5%;
        animation: blobMove1 18s ease-in-out infinite alternate;
    }
    .blob-2 {
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(255,248,220,0.6), transparent 70%);
        top: 30%; right: -10%;
        animation: blobMove2 22s ease-in-out infinite alternate;
    }
    .blob-3 {
        width: 450px; height: 450px;
        background: radial-gradient(circle, rgba(245,208,96,0.35), transparent 70%);
        bottom: -5%; left: 30%;
        animation: blobMove3 20s ease-in-out infinite alternate;
    }
    .blob-4 {
        width: 350px; height: 350px;
        background: radial-gradient(circle, rgba(255,255,255,0.8), transparent 70%);
        top: 50%; left: 10%;
        animation: blobMove4 25s ease-in-out infinite alternate;
    }
    .blob-5 {
        width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(184,134,11,0.2), transparent 70%);
        top: 10%; right: 20%;
        animation: blobMove5 16s ease-in-out infinite alternate;
    }
    @keyframes blobMove1 {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(120px, 80px) scale(1.15); }
    }
    @keyframes blobMove2 {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(-100px, 60px) scale(1.1); }
    }
    @keyframes blobMove3 {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(80px, -70px) scale(1.2); }
    }
    @keyframes blobMove4 {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(-60px, -90px) scale(0.9); }
    }
    @keyframes blobMove5 {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(70px, 100px) scale(1.1); }
    }

    /* ===== NOISE TEXTURE OVERLAY ===== */
    .noise-overlay {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        z-index: 1;
        opacity: 0.03;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
        background-repeat: repeat;
        background-size: 256px 256px;
    }

    /* ===== SIDEBAR: FROSTED GLASS ===== */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.55) !important;
        backdrop-filter: blur(25px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(25px) saturate(180%) !important;
        border-right: 1px solid rgba(212, 175, 55, 0.2);
        box-shadow: 4px 0 30px rgba(0,0,0,0.04);
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #1a1a2e !important;
        text-shadow: none !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: #333 !important;
        text-shadow: none !important;
    }

    /* ===== TYPOGRAPHY ===== */
    p, label, .stMarkdown, .stSelectbox label, .stMarkdown li {
        color: #2d2d3a !important;
        text-shadow: none;
    }
    ul[role="listbox"] li, div[data-baseweb="select"] span {
        color: #2d2d3a !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a2e !important;
        text-shadow: none;
    }

    /* ===== BUTTONS: GOLD LIQUID ===== */
    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #f5d060 50%, #d4af37 100%);
        background-size: 200% 200%;
        animation: buttonShimmer 3s ease infinite;
        color: #1a1a2e !important;
        border-radius: 14px;
        border: 1px solid rgba(212, 175, 55, 0.4);
        box-shadow: 0 4px 20px rgba(212, 175, 55, 0.25), inset 0 1px 0 rgba(255,255,255,0.5);
        transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
        padding: 0.7rem 1.4rem;
        font-weight: 700;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 0.85rem;
    }
    @keyframes buttonShimmer {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 12px 35px rgba(212, 175, 55, 0.4), 0 0 20px rgba(212, 175, 55, 0.15), inset 0 1px 0 rgba(255,255,255,0.6);
        color: #1a1a2e !important;
    }
    .stButton>button:active {
        transform: translateY(-1px) scale(0.99);
        transition: all 0.1s ease;
    }

    /* ===== METRIC CARDS: LIQUID GLASS ===== */
    .stMetric {
        background: rgba(255, 255, 255, 0.6);
        padding: 22px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06), inset 0 1px 0 rgba(255,255,255,0.8);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.7);
        text-align: center;
        transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
        position: relative;
        overflow: hidden;
    }
    .stMetric::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(212, 175, 55, 0.05), transparent);
        animation: metricGlow 4s ease-in-out infinite;
        pointer-events: none;
    }
    @keyframes metricGlow {
        0%, 100% { transform: rotate(0deg); opacity: 0; }
        50% { transform: rotate(180deg); opacity: 1; }
    }
    .stMetric:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(212, 175, 55, 0.15), 0 0 30px rgba(212, 175, 55, 0.05), inset 0 1px 0 rgba(255,255,255,0.9);
        border-color: rgba(212, 175, 55, 0.3);
    }
    .stMetric label {
        display: block !important;
        text-align: center !important;
        font-weight: 600 !important;
        color: #555 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.5px;
    }
    [data-testid="stMetricValue"] {
        color: #b8860b !important;
        text-align: center;
        font-size: 1.9rem !important;
        font-weight: 800 !important;
    }

    /* ===== ANIMATED TITLE ===== */
    @keyframes titleShimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    .animated-title {
        background: linear-gradient(90deg, #1a1a2e, #d4af37, #b8860b, #d4af37, #1a1a2e);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: titleShimmer 4s linear infinite;
        font-weight: 900;
        font-size: 3rem;
        margin-bottom: 0px;
        padding-bottom: 10px;
        line-height: 1.1;
    }

    /* ===== DIVIDERS ===== */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.4), transparent) !important;
    }

    /* ===== HIDE DEFAULTS ===== */
    header[data-testid="stHeader"] {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* ===== CUSTOM HEADER: FLOATING GLASS ===== */
    .custom-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(30px) saturate(200%);
        -webkit-backdrop-filter: blur(30px) saturate(200%);
        z-index: 99999;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 40px;
        box-shadow: 0 1px 30px rgba(0, 0, 0, 0.06);
        border-bottom: 1px solid rgba(212, 175, 55, 0.15);
        transition: all 0.3s ease;
    }
    .header-logo {
        color: #1a1a2e;
        font-size: 1.7rem;
        font-weight: 800;
        letter-spacing: 0.5px;
    }
    .header-logo span {
        background: linear-gradient(135deg, #d4af37, #b8860b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .header-nav a {
        color: #444;
        text-decoration: none;
        margin-left: 30px;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        padding: 8px 16px;
        border-radius: 10px;
        position: relative;
    }
    .header-nav a::after {
        content: '';
        position: absolute;
        bottom: 2px;
        left: 50%;
        width: 0;
        height: 2px;
        background: linear-gradient(90deg, #d4af37, #b8860b);
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        transform: translateX(-50%);
        border-radius: 2px;
    }
    .header-nav a:hover {
        color: #b8860b;
        background: rgba(212, 175, 55, 0.08);
    }
    .header-nav a:hover::after {
        width: 60%;
    }
    
    /* ===== SPACING FOR FIXED ELEMENTS ===== */
    .block-container {
        padding-top: 100px !important;
        padding-bottom: 110px !important;
    }

    /* ===== CUSTOM FOOTER: GLASS ===== */
    .custom-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(255, 255, 255, 0.5);
        color: #555;
        text-align: center;
        padding: 18px 0;
        font-size: 0.9rem;
        z-index: 99999;
        border-top: 1px solid rgba(212, 175, 55, 0.15);
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
    }
    .custom-footer a {
        background: linear-gradient(135deg, #d4af37, #b8860b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-decoration: none;
        font-weight: 700;
    }

    /* ===== TABLE STYLING ===== */
    .stTable, [data-testid="stTable"] {
        border-radius: 16px;
        overflow: hidden;
    }
    table {
        border-collapse: separate !important;
        border-spacing: 0 !important;
        background: rgba(255,255,255,0.5) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        border: 1px solid rgba(212, 175, 55, 0.15) !important;
    }
    th {
        background: linear-gradient(135deg, #d4af37, #e8c84a) !important;
        color: #1a1a2e !important;
        font-weight: 700 !important;
        padding: 14px 16px !important;
        font-size: 0.9rem !important;
    }
    td {
        color: #2d2d3a !important;
        padding: 12px 16px !important;
        border-bottom: 1px solid rgba(212, 175, 55, 0.08) !important;
    }
    tr:hover td {
        background: rgba(212, 175, 55, 0.05) !important;
    }

    /* ===== FLOATING PARTICLES BACKGROUND ===== */
    .particles-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .particle {
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(212, 175, 55, 0.25), transparent);
        animation: floatUp linear infinite;
    }
    @keyframes floatUp {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-10vh) rotate(360deg); opacity: 0; }
    }

    /* ===== DESCRIPTION BOX ===== */
    .desc-box {
        background: rgba(255,255,255,0.55);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 16px;
        padding: 20px 28px;
        border: 1px solid rgba(212, 175, 55, 0.15);
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        margin-top: -10px;
        margin-bottom: 30px;
        color: #444 !important;
        font-size: 1.05rem;
        line-height: 1.7;
        animation: fadeSlideIn 0.8s ease-out;
    }
    @keyframes fadeSlideIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .desc-box b {
        color: #b8860b;
    }

    /* ===== SUCCESS ALERTS ===== */
    [data-testid="stAlert"] {
        background: rgba(255,255,255,0.55) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        border-radius: 14px !important;
        color: #2d2d3a !important;
    }

    /* ===== SUBHEADERS ===== */
    .stSubheader, h2 {
        animation: fadeSlideIn 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Inject Mesh Gradient Blobs + Noise Overlay + Depth Particles
st.markdown("""
<div class="mesh-bg">
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>
    <div class="blob blob-4"></div>
    <div class="blob blob-5"></div>
</div>
<div class="noise-overlay"></div>
<div class="particles-bg">
    <!-- Near layer: sharp, larger, slower -->
    <div class="particle" style="width:10px;height:10px;left:8%;animation-duration:25s;animation-delay:0s;filter:blur(0px);opacity:0.35;"></div>
    <div class="particle" style="width:12px;height:12px;left:72%;animation-duration:28s;animation-delay:3s;filter:blur(0px);opacity:0.3;"></div>
    <div class="particle" style="width:9px;height:9px;left:45%;animation-duration:22s;animation-delay:6s;filter:blur(0px);opacity:0.35;"></div>
    <!-- Mid layer -->
    <div class="particle" style="width:6px;height:6px;left:15%;animation-duration:18s;animation-delay:1s;filter:blur(1px);opacity:0.25;"></div>
    <div class="particle" style="width:5px;height:5px;left:55%;animation-duration:20s;animation-delay:4s;filter:blur(1px);opacity:0.25;"></div>
    <div class="particle" style="width:7px;height:7px;left:82%;animation-duration:17s;animation-delay:2s;filter:blur(1px);opacity:0.2;"></div>
    <div class="particle" style="width:6px;height:6px;left:35%;animation-duration:19s;animation-delay:5s;filter:blur(1px);opacity:0.22;"></div>
    <!-- Far layer: blurry, tiny, fastest -->
    <div class="particle" style="width:3px;height:3px;left:22%;animation-duration:14s;animation-delay:0.5s;filter:blur(2px);opacity:0.15;"></div>
    <div class="particle" style="width:2px;height:2px;left:60%;animation-duration:12s;animation-delay:2.5s;filter:blur(3px);opacity:0.12;"></div>
    <div class="particle" style="width:3px;height:3px;left:90%;animation-duration:13s;animation-delay:7s;filter:blur(2px);opacity:0.15;"></div>
    <div class="particle" style="width:2px;height:2px;left:40%;animation-duration:11s;animation-delay:1.5s;filter:blur(3px);opacity:0.1;"></div>
    <div class="particle" style="width:4px;height:4px;left:5%;animation-duration:15s;animation-delay:8s;filter:blur(2px);opacity:0.13;"></div>
    <!-- Light flares: pulsing large orbs -->
    <div class="particle" style="width:20px;height:20px;left:30%;animation-duration:30s;animation-delay:0s;filter:blur(8px);opacity:0.08;background:radial-gradient(circle,rgba(255,215,0,0.5),transparent);"></div>
    <div class="particle" style="width:25px;height:25px;left:70%;animation-duration:35s;animation-delay:5s;filter:blur(10px);opacity:0.06;background:radial-gradient(circle,rgba(255,248,220,0.6),transparent);"></div>
    <div class="particle" style="width:18px;height:18px;left:50%;animation-duration:32s;animation-delay:10s;filter:blur(7px);opacity:0.07;background:radial-gradient(circle,rgba(212,175,55,0.4),transparent);"></div>
</div>
""", unsafe_allow_html=True)

# Inject Custom Header Navbar
st.markdown("""
<div class="custom-header">
    <div class="header-logo">⚙️ CPU<span>Scheduler</span></div>
    <div class="header-nav">
        <a href="." target="_self">Home</a>
        <a href="https://en.wikipedia.org/wiki/Scheduling_(computing)" target="_blank">Documentation</a>
        <a href="https://github.com/Rakshit239/OS-project-" target="_blank">GitHub</a>
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
<div class="desc-box">
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
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    label_color = '#444444'
    ax.tick_params(colors=label_color, labelsize=9)
    ax.xaxis.label.set_color(label_color)
    ax.title.set_color(label_color)
    for spine in ax.spines.values():
        spine.set_edgecolor('#ddd')
        spine.set_linewidth(0.5)

    pids = sorted({e.pid for e in result.gantt if e.pid})
    pid_map = {p: i for i, p in enumerate(pids)}

    # White & Gold palette for bars
    colors = ['#d4af37', '#e8c84a', '#c5993a', '#f0d56c', '#b8860b']

    for entry in result.gantt:
        if entry.pid:
            c = colors[pid_map[entry.pid] % len(colors)]
            ax.barh(pid_map[entry.pid], entry.end - entry.start, left=entry.start,
                    color=c, edgecolor='white', alpha=0.92, linewidth=2, height=0.6)
            ax.text((entry.start + entry.end) / 2, pid_map[entry.pid], entry.pid,
                    ha='center', va='center', color='#1a1a2e', fontweight='bold', fontsize=9)

    ax.set_yticks(list(pid_map.values()))
    ax.set_yticklabels(pids)
    ax.set_xlabel("Time")
    ax.grid(True, alpha=0.08, color='#888')
    fig.tight_layout()
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
    label_color = '#444444'
    ax.tick_params(colors=label_color, labelsize=9)
    ax.xaxis.label.set_color(label_color)
    ax.yaxis.label.set_color(label_color)
    ax.title.set_color(label_color)
    for spine in ax.spines.values():
        spine.set_edgecolor('#ddd')
        spine.set_linewidth(0.5)

    algos = [r.algorithm for r in results]
    energy = [r.total_energy for r in results]

    # Gold spectrum palette
    bar_colors = ['#d4af37', '#e8c84a', '#c5993a', '#f0d56c', '#b8860b']
    bars = ax.bar(algos, energy, color=bar_colors[:len(algos)], edgecolor='white',
                  alpha=0.92, linewidth=2, width=0.55)
    ax.set_ylabel("Energy (units)", fontweight='bold')
    ax.set_xlabel("Algorithm", fontweight='bold')
    ax.set_title("Energy Consumption Comparison", fontweight='bold', fontsize=14, pad=15)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.15, round(yval,1),
                ha='center', va='bottom', color='#b8860b', fontweight='bold', fontsize=10)

    plt.xticks(rotation=30, ha='right')
    ax.grid(True, axis='y', alpha=0.08, color='#888')
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
