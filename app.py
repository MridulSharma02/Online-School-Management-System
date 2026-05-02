import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # noqa
import numpy as np
from datetime import date

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DPS School Management",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inject custom CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  --bg:       #0b0f1a;
  --surface:  #131929;
  --card:     #1a2236;
  --border:   #252f45;
  --accent:   #4f8ef7;
  --green:    #3ecf8e;
  --amber:    #f5a623;
  --red:      #ff5b5b;
  --text:     #e8edf5;
  --muted:    #8896b0;
  --font:     'Sora', sans-serif;
  --mono:     'JetBrains Mono', monospace;
}

html, body, [class*="css"] {
  font-family: var(--font) !important;
  background: var(--bg) !important;
  color: var(--text) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1400px; }

/* ── Hero banner ── */
.hero {
  background: linear-gradient(135deg, #0d1b3e 0%, #1a2a5e 50%, #0d1b3e 100%);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 3rem 3rem 2.5rem;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute; top: -50%; right: -10%;
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(79,142,247,.15) 0%, transparent 70%);
  pointer-events: none;
}
.hero h1 { font-size: 2.6rem; font-weight: 800; margin: 0 0 .4rem;
  background: linear-gradient(90deg, #fff 30%, #4f8ef7);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero p  { color: var(--muted); font-size: 1rem; margin: 0; }
.badge   { display: inline-block; background: rgba(79,142,247,.15);
  border: 1px solid rgba(79,142,247,.4); color: var(--accent);
  font-size: .72rem; font-family: var(--mono); padding: .25rem .7rem;
  border-radius: 20px; margin-bottom: 1rem; letter-spacing: .05em; }

/* ── Portal cards ── */
.portal-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1.2rem; }
.portal-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 16px; padding: 2rem 1.6rem; cursor: pointer;
  transition: all .25s; position: relative; overflow: hidden;
}
.portal-card:hover { transform: translateY(-4px); border-color: var(--accent);
  box-shadow: 0 12px 40px rgba(79,142,247,.15); }
.portal-card .icon { font-size: 2.4rem; margin-bottom: .8rem; display: block; }
.portal-card h3    { font-size: 1.1rem; font-weight: 700; margin: 0 0 .4rem; }
.portal-card p     { color: var(--muted); font-size: .82rem; margin: 0; }
.portal-card .pill {
  position: absolute; top: 1rem; right: 1rem;
  font-size: .65rem; font-family: var(--mono);
  padding: .2rem .55rem; border-radius: 10px; font-weight: 600;
}
.pill-admin  { background: rgba(245,166,35,.12); color: var(--amber); border: 1px solid rgba(245,166,35,.3); }
.pill-teacher{ background: rgba(62,207,142,.12);  color: var(--green); border: 1px solid rgba(62,207,142,.3); }
.pill-student{ background: rgba(79,142,247,.12);  color: var(--accent); border: 1px solid rgba(79,142,247,.3); }

/* ── Section headers ── */
.sec-header {
  display: flex; align-items: center; gap: .8rem;
  margin: .5rem 0 1.4rem;
}
.sec-header .line { flex: 1; height: 1px; background: var(--border); }
.sec-header span  { color: var(--muted); font-size: .75rem;
  font-family: var(--mono); letter-spacing: .1em; text-transform: uppercase; }

/* ── Metric cards ── */
.metric-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 1.6rem; }
.metric-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 12px; padding: 1.2rem 1.4rem;
}
.metric-card .label { color: var(--muted); font-size: .75rem;
  text-transform: uppercase; letter-spacing: .08em; margin-bottom: .4rem; }
.metric-card .value { font-size: 1.8rem; font-weight: 800;
  font-family: var(--mono); }
.metric-card .sub   { color: var(--muted); font-size: .75rem; margin-top: .2rem; }
.val-green { color: var(--green); }
.val-blue  { color: var(--accent); }
.val-amber { color: var(--amber); }
.val-red   { color: var(--red); }

/* ── Data table ── */
.stDataFrame { border-radius: 10px !important; }
thead tr th  { background: var(--surface) !important; color: var(--accent) !important;
  font-family: var(--mono) !important; font-size: .78rem !important; }
tbody tr:hover td { background: rgba(79,142,247,.05) !important; }

/* ── Form inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input {
  background: var(--surface) !important; border: 1px solid var(--border) !important;
  color: var(--text) !important; border-radius: 8px !important;
  font-family: var(--font) !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(79,142,247,.15) !important;
}

/* ── Buttons ── */
.stButton > button {
  background: var(--accent) !important; color: #fff !important;
  border: none !important; border-radius: 8px !important;
  font-family: var(--font) !important; font-weight: 600 !important;
  padding: .55rem 1.4rem !important; transition: all .2s !important;
}
.stButton > button:hover {
  background: #6ba3ff !important; transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(79,142,247,.35) !important;
}

/* ── Alert boxes ── */
.stSuccess { background: rgba(62,207,142,.08) !important;
  border: 1px solid rgba(62,207,142,.3) !important; border-radius: 10px !important; }
.stError   { background: rgba(255,91,91,.08) !important;
  border: 1px solid rgba(255,91,91,.3) !important; border-radius: 10px !important; }
.stInfo    { background: rgba(79,142,247,.08) !important;
  border: 1px solid rgba(79,142,247,.3) !important; border-radius: 10px !important; }
.stWarning { background: rgba(245,166,35,.08) !important;
  border: 1px solid rgba(245,166,35,.3) !important; border-radius: 10px !important; }

/* ── Sidebar ── */
.css-1d391kg, [data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important; border-radius: 10px !important;
  padding: 4px !important; gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
  color: var(--muted) !important; border-radius: 7px !important;
  font-family: var(--font) !important; font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
  background: var(--accent) !important; color: #fff !important;
}

/* ── Progress bar ── */
.prog-wrap { background: var(--border); border-radius: 20px; height: 8px; overflow: hidden; margin: .4rem 0; }
.prog-fill  { height: 100%; border-radius: 20px; background: var(--accent); transition: width .6s ease; }

/* ── Subject chip ── */
.chip { display: inline-block; background: rgba(79,142,247,.12);
  border: 1px solid rgba(79,142,247,.25); color: var(--accent);
  border-radius: 6px; padding: .2rem .6rem; font-size: .75rem;
  font-family: var(--mono); margin: .15rem; }

/* ── Grade badge ── */
.grade { display: inline-flex; align-items: center; justify-content: center;
  width: 38px; height: 38px; border-radius: 8px;
  font-size: .85rem; font-weight: 800; font-family: var(--mono); }
.grade-A { background: rgba(62,207,142,.15); color: var(--green); }
.grade-B { background: rgba(79,142,247,.15); color: var(--accent); }
.grade-C { background: rgba(245,166,35,.15); color: var(--amber); }
.grade-D { background: rgba(255,91,91,.15);  color: var(--red); }

/* ── Back button ── */
.back-btn { display: inline-flex; align-items: center; gap: .5rem;
  color: var(--muted); font-size: .82rem; cursor: pointer;
  margin-bottom: 1.2rem; transition: color .2s; }
.back-btn:hover { color: var(--accent); }

/* ── Status pill ── */
.status-paid    { background: rgba(62,207,142,.12); color: var(--green);
  border: 1px solid rgba(62,207,142,.3); border-radius: 20px;
  padding: .15rem .6rem; font-size: .72rem; font-family: var(--mono); }
.status-pending { background: rgba(255,91,91,.12); color: var(--red);
  border: 1px solid rgba(255,91,91,.3); border-radius: 20px;
  padding: .15rem .6rem; font-size: .72rem; font-family: var(--mono); }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  DEMO DATA
# ══════════════════════════════════════════════════════════════════════════════
USERS = {
    # userid : (password, role, display_name, id)
    "ab@dpsrkp.org":      ("abc123",  "admin",   "Admin AB",     "A112"),
    "mridul@dpsrkp.org":  ("nani",    "student", "Mridul Sharma","S7172"),
    "abc@dpsrkp.org":     ("rock",    "student", "ABC",          "S7173"),
    "lp@dpsrkp.org":      ("physics", "teacher", "Lipi",         "T819"),
}

STUDENTS = pd.DataFrame([
    {"admin_no":"S7172","name":"Mridul Sharma","dob":"2003-08-05","phno":"991047948","gender":"M"},
    {"admin_no":"S7173","name":"ABC",           "dob":"2020-01-02","phno":"98765432", "gender":"F"},
    {"admin_no":"S7174","name":"Priya Kapoor",  "dob":"2003-11-15","phno":"912345678","gender":"F"},
    {"admin_no":"S7175","name":"Rohan Mehta",   "dob":"2003-04-22","phno":"987654321","gender":"M"},
])

TEACHERS = pd.DataFrame([
    {"tid":"T819","name":"Lipi","doj":"2010-02-12","phno":"971132543","subject":"Physics"},
    {"tid":"T820","name":"Mohitendra Dey","doj":"2008-06-01","phno":"981234567","subject":"CS"},
    {"tid":"T821","name":"Sunita Sharma","doj":"2015-03-18","phno":"976543210","subject":"Maths"},
])

SALARY = pd.DataFrame([
    {"tid":"T819","name":"Lipi","basic":50000,"allow":1000,"tax":4000,"ded":2000,"net":45000},
    {"tid":"T820","name":"Mohitendra Dey","basic":55000,"allow":2000,"tax":4400,"ded":1000,"net":51600},
    {"tid":"T821","name":"Sunita Sharma","basic":48000,"allow":1500,"tax":3840,"ded":0,"net":45660},
])

MARKS = {
    "utone": pd.DataFrame([
        {"admin_no":"S7172","name":"Mridul Sharma","phy":44,"chem":45,"math":45,"eng":43,"cs":49},
        {"admin_no":"S7173","name":"ABC",           "phy":46,"chem":48,"math":45,"eng":46,"cs":50},
        {"admin_no":"S7174","name":"Priya Kapoor",  "phy":40,"chem":42,"math":44,"eng":47,"cs":45},
        {"admin_no":"S7175","name":"Rohan Mehta",   "phy":38,"chem":39,"math":41,"eng":40,"cs":43},
    ]),
    "hye": pd.DataFrame([
        {"admin_no":"S7172","name":"Mridul Sharma","phy":95,"chem":93,"math":92,"eng":94,"cs":97},
        {"admin_no":"S7173","name":"ABC",           "phy":88,"chem":91,"math":85,"eng":87,"cs":90},
        {"admin_no":"S7174","name":"Priya Kapoor",  "phy":78,"chem":80,"math":82,"eng":76,"cs":84},
        {"admin_no":"S7175","name":"Rohan Mehta",   "phy":65,"chem":68,"math":70,"eng":62,"cs":72},
    ]),
    "uttwo": pd.DataFrame([
        {"admin_no":"S7172","name":"Mridul Sharma","phy":47,"chem":46,"math":48,"eng":45,"cs":50},
        {"admin_no":"S7173","name":"ABC",           "phy":44,"chem":45,"math":43,"eng":46,"cs":47},
        {"admin_no":"S7174","name":"Priya Kapoor",  "phy":39,"chem":41,"math":42,"eng":38,"cs":44},
        {"admin_no":"S7175","name":"Rohan Mehta",   "phy":35,"chem":36,"math":38,"eng":34,"cs":40},
    ]),
    "fye": pd.DataFrame([
        {"admin_no":"S7172","name":"Mridul Sharma","phy":91,"chem":88,"math":94,"eng":89,"cs":96},
        {"admin_no":"S7173","name":"ABC",           "phy":82,"chem":85,"math":80,"eng":83,"cs":88},
        {"admin_no":"S7174","name":"Priya Kapoor",  "phy":72,"chem":74,"math":78,"eng":70,"cs":80},
        {"admin_no":"S7175","name":"Rohan Mehta",   "phy":60,"chem":63,"math":65,"eng":58,"cs":68},
    ]),
}

ASSIGNMENTS = pd.DataFrame([
    {"agno":1,"subject":"Physics","topic":"EMI","dos":"2020-12-17","status":"Pending"},
    {"agno":2,"subject":"Chemistry","topic":"Organic Reactions","dos":"2020-12-20","status":"Submitted"},
    {"agno":3,"subject":"Mathematics","topic":"Integration","dos":"2020-12-22","status":"Pending"},
    {"agno":4,"subject":"CS","topic":"SQL Joins","dos":"2020-12-24","status":"Submitted"},
])

FEES = pd.DataFrame([
    {"admin_no":"S7172","name":"Mridul Sharma","amt":30000,"jan_mar":"Paid","apr_jun":"Paid","jul_sep":"Paid","oct_dec":"Paid"},
    {"admin_no":"S7173","name":"ABC",           "amt":30000,"jan_mar":"Paid","apr_jun":"Paid","jul_sep":"Pending","oct_dec":"Pending"},
    {"admin_no":"S7174","name":"Priya Kapoor",  "amt":30000,"jan_mar":"Paid","apr_jun":"Pending","jul_sep":"Pending","oct_dec":"Pending"},
    {"admin_no":"S7175","name":"Rohan Mehta",   "amt":30000,"jan_mar":"Paid","apr_jun":"Paid","jul_sep":"Paid","oct_dec":"Pending"},
])

SUBJECTS = ["Physics","Chemistry","Math","English","CS"]
EXAM_KEYS = {"Weekly Test 1":"utone","Half Yearly":"hye","Weekly Test 2":"uttwo","Final Exam":"fye"}
MAX_MARKS  = {"utone":50,"hye":100,"uttwo":50,"fye":100}

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def init_state():
    defaults = dict(logged_in=False, role=None, user=None, uid=None,
                    page="login", students=STUDENTS.copy(),
                    teachers=TEACHERS.copy(), salary=SALARY.copy(),
                    marks={k:v.copy() for k,v in MARKS.items()},
                    assignments=ASSIGNMENTS.copy(), fees=FEES.copy())
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
ss = st.session_state

# ══════════════════════════════════════════════════════════════════════════════
#  UTILITY
# ══════════════════════════════════════════════════════════════════════════════
def grade_label(pct):
    if pct >= 90: return "A+"
    if pct >= 80: return "A"
    if pct >= 70: return "B+"
    if pct >= 60: return "B"
    if pct >= 45: return "C"
    return "F"

def grade_class(g):
    return "grade-A" if g.startswith("A") else \
           "grade-B" if g.startswith("B") else \
           "grade-C" if g.startswith("C") else "grade-D"

def progress_bar(value, max_val, color="#4f8ef7"):
    pct = min(100, value / max_val * 100)
    return f"""<div class="prog-wrap">
  <div class="prog-fill" style="width:{pct:.0f}%;background:{color}"></div>
</div>"""

def sec_header(label):
    st.markdown(f"""<div class="sec-header">
      <div class="line"></div><span>{label}</span><div class="line"></div>
    </div>""", unsafe_allow_html=True)

def go(page): ss.page = page; st.rerun()

def logout():
    for k in ["logged_in","role","user","uid"]: ss[k] = None if k != "logged_in" else False
    ss.page = "login"; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
def page_login():
    st.markdown("""<div class="hero">
      <div class="badge">CBSE CLASS XII · 2023-24</div>
      <h1>🏫 Online School Management</h1>
      <p>Delhi Public School, Sector-12, R.K. Puram, New Delhi</p>
    </div>""", unsafe_allow_html=True)

    sec_header("SELECT PORTAL")
    st.markdown("""<div class="portal-grid">
      <div class="portal-card">
        <span class="pill pill-admin">ADMIN</span>
        <span class="icon">🛡️</span>
        <h3>Administration</h3>
        <p>Manage students, teachers, fees & salary records</p>
      </div>
      <div class="portal-card">
        <span class="pill pill-teacher">STAFF</span>
        <span class="icon">👩‍🏫</span>
        <h3>Teacher Portal</h3>
        <p>Upload marks, manage assignments & view salary</p>
      </div>
      <div class="portal-card">
        <span class="pill pill-student">STUDENT</span>
        <span class="icon">🎓</span>
        <h3>Student Portal</h3>
        <p>View report cards, progress analysis & pay fees</p>
      </div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    sec_header("LOGIN")
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        with st.container():
            uid  = st.text_input("User ID",  placeholder="user@dpsrkp.org")
            pwd  = st.text_input("Password", type="password", placeholder="••••••••")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔐  Sign In", use_container_width=True):
                if uid in USERS and USERS[uid][0] == pwd:
                    ss.logged_in = True
                    ss.user = uid
                    ss.role = USERS[uid][1]
                    ss.uid  = USERS[uid][3]
                    ss.uname = USERS[uid][2]
                    ss.page = "dashboard"
                    st.rerun()
                else:
                    st.error("❌ Invalid User ID or Password")

            st.markdown("""<div style="background:rgba(79,142,247,.07);border:1px solid rgba(79,142,247,.2);
              border-radius:10px;padding:.9rem 1rem;margin-top:1rem;font-size:.78rem;color:#8896b0">
              <b style="color:#4f8ef7">Demo credentials</b><br>
              🛡️ Admin &nbsp;&nbsp;&nbsp; ab@dpsrkp.org / abc123<br>
              👩‍🏫 Teacher &nbsp; lp@dpsrkp.org / physics<br>
              🎓 Student &nbsp; mridul@dpsrkp.org / nani
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SHARED TOPBAR
# ══════════════════════════════════════════════════════════════════════════════
def topbar():
    role_icons = {"admin":"🛡️","teacher":"👩‍🏫","student":"🎓"}
    role_colors= {"admin":"#f5a623","teacher":"#3ecf8e","student":"#4f8ef7"}
    c = role_colors.get(ss.role,"#4f8ef7")
    i = role_icons.get(ss.role,"👤")
    st.markdown(f"""<div style="display:flex;align-items:center;justify-content:space-between;
      background:var(--surface);border:1px solid var(--border);border-radius:14px;
      padding:.8rem 1.4rem;margin-bottom:1.6rem">
      <div style="display:flex;align-items:center;gap:.8rem">
        <span style="font-size:1.5rem">{i}</span>
        <div>
          <div style="font-weight:700;font-size:.95rem">{ss.uname}</div>
          <div style="color:var(--muted);font-size:.72rem;font-family:var(--mono)">{ss.user}</div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:.8rem">
        <span style="background:rgba(79,142,247,.1);border:1px solid rgba(79,142,247,.25);
          color:{c};border-radius:20px;padding:.2rem .7rem;
          font-size:.7rem;font-family:var(--mono);text-transform:uppercase">{ss.role}</span>
        <span style="color:var(--muted);font-size:.8rem">ID: {ss.uid}</span>
      </div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  MARKS / REPORT CARD  helpers
# ══════════════════════════════════════════════════════════════════════════════
def show_report_card(exam_key, adno):
    df = ss.marks[exam_key]
    row = df[df["admin_no"] == adno]
    if row.empty:
        st.info("No record found for this admission number.")
        return
    r = row.iloc[0]
    mx = MAX_MARKS[exam_key]
    total = r["phy"] + r["chem"] + r["math"] + r["eng"] + r["cs"]
    pct   = total / (mx * 5) * 100
    g     = grade_label(pct)

    st.markdown(f"""<div style="background:var(--card);border:1px solid var(--border);
      border-radius:16px;padding:1.4rem 1.8rem;margin-bottom:1rem">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem">
        <div>
          <div style="font-weight:700;font-size:1.05rem">{r['name']}</div>
          <div style="color:var(--muted);font-size:.78rem;font-family:var(--mono)">{adno}</div>
        </div>
        <div style="text-align:right">
          <div class="grade {grade_class(g)}" style="font-size:1.2rem;width:52px;height:52px">{g}</div>
          <div style="color:var(--muted);font-size:.72rem;margin-top:.3rem">{pct:.1f}%</div>
        </div>
      </div>""", unsafe_allow_html=True)

    subjects_display = [("Physics",r["phy"]),("Chemistry",r["chem"]),
                        ("Math",r["math"]),("English",r["eng"]),("CS",r["cs"])]
    for sub, score in subjects_display:
        col_color = "#3ecf8e" if score/mx >= .8 else "#4f8ef7" if score/mx >= .6 else "#f5a623" if score/mx >= .45 else "#ff5b5b"
        st.markdown(f"""<div style="display:flex;align-items:center;gap:.8rem;margin:.45rem 0">
          <div style="width:90px;color:var(--muted);font-size:.8rem">{sub}</div>
          <div style="flex:1">{progress_bar(score,mx,col_color)}</div>
          <div style="width:55px;text-align:right;font-family:var(--mono);font-size:.82rem;font-weight:600">{score}/{mx}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    passed = pct >= 45
    if passed:
        st.success(f"✅ **PASSED** — {pct:.1f}% — Grade {g}")
    else:
        st.error(f"❌ **FAILED** — {pct:.1f}% — Below pass mark (45%)")

def show_progress_chart(adno):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    fig.patch.set_facecolor("#131929")
    ax.set_facecolor("#131929")

    colors  = ["#4f8ef7","#3ecf8e","#f5a623","#ff5b5b"]
    labels  = list(EXAM_KEYS.keys())
    x       = np.arange(len(SUBJECTS))
    width   = 0.18

    for i, (exam_label, exam_key) in enumerate(EXAM_KEYS.items()):
        df  = ss.marks[exam_key]
        row = df[df["admin_no"] == adno]
        if row.empty: continue
        r   = row.iloc[0]
        mx  = MAX_MARKS[exam_key]
        scores = [r["phy"]/mx*100, r["chem"]/mx*100,
                  r["math"]/mx*100, r["eng"]/mx*100, r["cs"]/mx*100]
        offset = (i - 1.5) * width
        bars = ax.bar(x + offset, scores, width, label=exam_label,
                      color=colors[i], alpha=.85, zorder=3)

    ax.axhline(45, color="#ff5b5b", linestyle="--", linewidth=1.2,
               label="Pass mark (45%)", alpha=.7, zorder=2)
    ax.set_xticks(x); ax.set_xticklabels(SUBJECTS, color="#8896b0", fontsize=9)
    ax.set_yticks([0,25,50,75,100])
    ax.set_yticklabels(["0%","25%","50%","75%","100%"], color="#8896b0", fontsize=9)
    ax.set_ylabel("% Score", color="#8896b0", fontsize=9)
    ax.set_title("Progress Analysis — All Exams", color="#e8edf5", fontsize=12, fontweight="bold", pad=14)
    ax.tick_params(colors="#8896b0"); ax.spines[:].set_visible(False)
    ax.yaxis.grid(True, color="#252f45", linestyle="--", linewidth=.6, zorder=0)
    legend = ax.legend(loc="upper right", frameon=True, fontsize=8)
    legend.get_frame().set_facecolor("#1a2236")
    legend.get_frame().set_edgecolor("#252f45")
    for t in legend.get_texts(): t.set_color("#e8edf5")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
#  STUDENT DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_student():
    topbar()
    adno = ss.uid
    row  = ss.students[ss.students["admin_no"] == adno]
    name = row.iloc[0]["name"] if not row.empty else ss.uname

    st.markdown(f"""<div class="hero" style="padding:2rem 2.4rem">
      <div class="badge">STUDENT PORTAL</div>
      <h1 style="font-size:1.9rem">Welcome back, {name.split()[0]}! 👋</h1>
      <p>Academic year 2023-24 · {adno}</p>
    </div>""", unsafe_allow_html=True)

    # quick metrics
    fye_df  = ss.marks["fye"]
    row_fye = fye_df[fye_df["admin_no"] == adno]
    if not row_fye.empty:
        r  = row_fye.iloc[0]
        tot= r["phy"]+r["chem"]+r["math"]+r["eng"]+r["cs"]
        pct= tot/500*100; g = grade_label(pct)
        fee_row = ss.fees[ss.fees["admin_no"] == adno]
        paid = sum(1 for c in ["jan_mar","apr_jun","jul_sep","oct_dec"]
                   if not fee_row.empty and fee_row.iloc[0][c]=="Paid")
        st.markdown(f"""<div class="metric-row">
          <div class="metric-card"><div class="label">Final %</div>
            <div class="value val-green">{pct:.1f}%</div>
            <div class="sub">Grade {g}</div></div>
          <div class="metric-card"><div class="label">Subjects</div>
            <div class="value val-blue">5</div>
            <div class="sub">PCM · Eng · CS</div></div>
          <div class="metric-card"><div class="label">Assignments</div>
            <div class="value val-amber">{len(ss.assignments)}</div>
            <div class="sub">this term</div></div>
          <div class="metric-card"><div class="label">Fees Paid</div>
            <div class="value {'val-green' if paid==4 else 'val-amber'}">{paid}/4</div>
            <div class="sub">quarters</div></div>
        </div>""", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📋 Report Card","📈 Progress","📝 Assignments","💳 Fees","🔑 Update Password"])

    # ── Report Card ──
    with tab1:
        sec_header("REPORT CARD")
        exam = st.selectbox("Select Examination", list(EXAM_KEYS.keys()), key="sel_exam")
        show_report_card(EXAM_KEYS[exam], adno)

    # ── Progress ──
    with tab2:
        sec_header("PROGRESS ANALYSIS")
        show_progress_chart(adno)

    # ── Assignments ──
    with tab3:
        sec_header("WEEKLY ASSIGNMENTS")
        for _, a in ss.assignments.iterrows():
            status_html = f'<span class="status-{"paid" if a["status"]=="Submitted" else "pending"}">{a["status"]}</span>'
            st.markdown(f"""<div style="background:var(--card);border:1px solid var(--border);
              border-radius:10px;padding:.9rem 1.2rem;margin:.4rem 0;
              display:flex;align-items:center;justify-content:space-between">
              <div>
                <span class="chip">#{a['agno']}</span>
                <span class="chip">{a['subject']}</span>
                <span style="margin-left:.4rem;font-weight:600;font-size:.9rem">{a['topic']}</span>
              </div>
              <div style="display:flex;align-items:center;gap:1rem">
                <span style="color:var(--muted);font-size:.78rem;font-family:var(--mono)">Due: {a['dos']}</span>
                {status_html}
              </div>
            </div>""", unsafe_allow_html=True)

    # ── Fees ──
    with tab4:
        sec_header("FEES MANAGEMENT")
        fee_row = ss.fees[ss.fees["admin_no"] == adno]
        if not fee_row.empty:
            fr = fee_row.iloc[0]
            quarters = [("Jan – Mar","jan_mar"),("Apr – Jun","apr_jun"),
                        ("Jul – Sep","jul_sep"),("Oct – Dec","oct_dec")]
            cols = st.columns(4)
            for idx, (label, key) in enumerate(quarters):
                status = fr[key]
                with cols[idx]:
                    color = "#3ecf8e" if status=="Paid" else "#ff5b5b"
                    icon  = "✅" if status=="Paid" else "⏳"
                    st.markdown(f"""<div style="background:var(--card);border:1px solid var(--border);
                      border-radius:12px;padding:1.2rem;text-align:center">
                      <div style="font-size:1.8rem">{icon}</div>
                      <div style="font-weight:700;margin:.3rem 0">{label}</div>
                      <div style="color:{color};font-family:var(--mono);font-size:.8rem">{status}</div>
                      <div style="color:var(--muted);font-size:.72rem;margin-top:.2rem">₹7,500</div>
                    </div>""", unsafe_allow_html=True)

            if st.button("💳  Mark January–March as Paid"):
                idx_f = ss.fees[ss.fees["admin_no"] == adno].index[0]
                ss.fees.at[idx_f,"jan_mar"] = "Paid"
                st.success("Payment recorded!"); st.rerun()

    # ── Update Password ──
    with tab5:
        sec_header("UPDATE PASSWORD")
        col1, _, _ = st.columns([1.2, 1, 1])
        with col1:
            old_p = st.text_input("Current Password", type="password")
            new_p = st.text_input("New Password",     type="password")
            c_p   = st.text_input("Confirm Password", type="password")
            if st.button("Update Password"):
                if old_p != USERS[ss.user][0]:
                    st.error("Current password is incorrect.")
                elif new_p != c_p:
                    st.error("New passwords do not match.")
                elif len(new_p) < 4:
                    st.warning("Password must be at least 4 characters.")
                else:
                    st.success("Password updated successfully! (Demo mode: not persisted)")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪  Log Out"):
        logout()

# ══════════════════════════════════════════════════════════════════════════════
#  TEACHER DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_teacher():
    topbar()
    tid   = ss.uid
    t_row = ss.salary[ss.salary["tid"] == tid]

    st.markdown(f"""<div class="hero" style="padding:2rem 2.4rem">
      <div class="badge">TEACHER PORTAL</div>
      <h1 style="font-size:1.9rem">Teacher Dashboard 👩‍🏫</h1>
      <p>Manage results, assignments & view your salary</p>
    </div>""", unsafe_allow_html=True)

    net = t_row.iloc[0]["net"] if not t_row.empty else 0
    st.markdown(f"""<div class="metric-row">
      <div class="metric-card"><div class="label">Total Students</div>
        <div class="value val-blue">{len(ss.students)}</div><div class="sub">enrolled</div></div>
      <div class="metric-card"><div class="label">Assignments</div>
        <div class="value val-amber">{len(ss.assignments)}</div><div class="sub">active</div></div>
      <div class="metric-card"><div class="label">Net Salary</div>
        <div class="value val-green">₹{net:,}</div><div class="sub">this month</div></div>
      <div class="metric-card"><div class="label">Exams</div>
        <div class="value val-blue">4</div><div class="sub">per year</div></div>
    </div>""", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Report Cards","📝 Assignments","💰 Salary","🔑 Password"])

    # ── Report Cards ──
    with tab1:
        sec_header("MANAGE REPORT CARDS")
        exam = st.selectbox("Examination", list(EXAM_KEYS.keys()), key="t_exam")
        ekey = EXAM_KEYS[exam]
        act  = st.radio("Action", ["View All","Add Marks","Update Marks","Delete Record"],
                        horizontal=True, key="t_act")

        if act == "View All":
            df = ss.marks[ekey][["admin_no","name","phy","chem","math","eng","cs"]].copy()
            df.columns = ["Adm No","Name","Physics","Chemistry","Math","English","CS"]
            st.dataframe(df, use_container_width=True, hide_index=True)

        elif act == "Add Marks":
            adno = st.text_input("Admission Number")
            name = st.text_input("Student Name")
            mx   = MAX_MARKS[ekey]
            cols = st.columns(5)
            scores = {}
            for i, sub in enumerate(["phy","chem","math","eng","cs"]):
                scores[sub] = cols[i].number_input(SUBJECTS[i], 0, mx, key=f"add_{sub}")
            if st.button("➕ Add Record"):
                new_row = {"admin_no":adno,"name":name,**scores}
                ss.marks[ekey] = pd.concat(
                    [ss.marks[ekey], pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Marks added for {adno}!")

        elif act == "Update Marks":
            adno = st.text_input("Admission Number to Update")
            if adno and not ss.marks[ekey][ss.marks[ekey]["admin_no"]==adno].empty:
                mx = MAX_MARKS[ekey]
                cols = st.columns(5)
                scores = {}
                for i, sub in enumerate(["phy","chem","math","eng","cs"]):
                    scores[sub] = cols[i].number_input(SUBJECTS[i], 0, mx, key=f"upd_{sub}")
                if st.button("💾 Update"):
                    for sub, val in scores.items():
                        ss.marks[ekey].loc[ss.marks[ekey]["admin_no"]==adno, sub] = val
                    st.success("Marks updated!")
            elif adno:
                st.warning("No record found for that admission number.")

        elif act == "Delete Record":
            adno = st.text_input("Admission Number to Delete")
            if st.button("🗑️ Delete"):
                ss.marks[ekey] = ss.marks[ekey][ss.marks[ekey]["admin_no"] != adno]
                st.success("Record deleted.")

    # ── Assignments ──
    with tab2:
        sec_header("WEEKLY ASSIGNMENTS")
        act2 = st.radio("Action",["View","Add","Update Status","Delete"],horizontal=True,key="t_asgn")
        if act2 == "View":
            for _, a in ss.assignments.iterrows():
                status_html = f'<span class="status-{"paid" if a["status"]=="Submitted" else "pending"}">{a["status"]}</span>'
                st.markdown(f"""<div style="background:var(--card);border:1px solid var(--border);
                  border-radius:10px;padding:.9rem 1.2rem;margin:.4rem 0;
                  display:flex;align-items:center;justify-content:space-between">
                  <div><span class="chip">#{a['agno']}</span>
                    <span class="chip">{a['subject']}</span>
                    <b style="margin-left:.4rem">{a['topic']}</b></div>
                  <div style="display:flex;align-items:center;gap:1rem">
                    <span style="color:var(--muted);font-size:.78rem;font-family:var(--mono)">Due: {a['dos']}</span>
                    {status_html}</div>
                </div>""", unsafe_allow_html=True)

        elif act2 == "Add":
            c1, c2 = st.columns(2)
            agno = c1.number_input("Assignment No.", min_value=1, value=len(ss.assignments)+1)
            sub  = c1.selectbox("Subject", SUBJECTS)
            top  = c2.text_input("Topic")
            dos  = c2.date_input("Due Date", date.today())
            stat = c2.selectbox("Status", ["Pending","Submitted"])
            if st.button("➕ Add Assignment"):
                new = {"agno":agno,"subject":sub,"topic":top,"dos":str(dos),"status":stat}
                ss.assignments = pd.concat(
                    [ss.assignments, pd.DataFrame([new])], ignore_index=True)
                st.success("Assignment added!")

        elif act2 == "Update Status":
            agno = st.number_input("Assignment No.", min_value=1, value=1)
            stat = st.selectbox("New Status", ["Pending","Submitted"])
            if st.button("💾 Update"):
                ss.assignments.loc[ss.assignments["agno"]==agno,"status"] = stat
                st.success("Status updated!")

        elif act2 == "Delete":
            agno = st.number_input("Assignment No. to Delete", min_value=1)
            if st.button("🗑️ Delete"):
                ss.assignments = ss.assignments[ss.assignments["agno"]!=agno]
                st.success("Deleted.")

    # ── Salary ──
    with tab3:
        sec_header("NET IN-HAND SALARY")
        if not t_row.empty:
            r = t_row.iloc[0]
            col1, col2 = st.columns([1.2, 1])
            with col1:
                st.markdown(f"""<div style="background:var(--card);border:1px solid var(--border);
                  border-radius:16px;padding:1.6rem">
                  <div style="margin-bottom:.8rem;color:var(--muted);font-size:.75rem;
                    font-family:var(--mono);text-transform:uppercase">Salary Breakdown — {r['name']}</div>
                  {''.join(f"""<div style="display:flex;justify-content:space-between;
                    padding:.55rem 0;border-bottom:1px solid var(--border)">
                    <span style="color:var(--muted);font-size:.88rem">{label}</span>
                    <span style="font-family:var(--mono);font-weight:600;color:{color}">₹{val:,}</span>
                  </div>""" for label,val,color in [
                    ("Basic Pay",r["basic"],"#e8edf5"),
                    ("Allowances",r["allow"],"#3ecf8e"),
                    ("Tax (8%)",r["tax"],"#ff5b5b"),
                    ("Leave Deductions",r["ded"],"#ff5b5b"),
                  ])}
                  <div style="display:flex;justify-content:space-between;
                    padding:.7rem 0;margin-top:.2rem">
                    <span style="font-weight:700">Net In-Hand</span>
                    <span style="font-family:var(--mono);font-weight:800;
                      color:#3ecf8e;font-size:1.1rem">₹{r['net']:,}</span>
                  </div>
                </div>""", unsafe_allow_html=True)

    # ── Password ──
    with tab4:
        sec_header("UPDATE PASSWORD")
        col1, _, _ = st.columns([1.2, 1, 1])
        with col1:
            new_p = st.text_input("New Password", type="password")
            c_p   = st.text_input("Confirm",      type="password")
            if st.button("Update"):
                if new_p == c_p and len(new_p) >= 4:
                    st.success("Password updated! (Demo: not persisted)")
                else:
                    st.error("Passwords don't match or too short.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪  Log Out"):
        logout()

# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_admin():
    topbar()
    st.markdown("""<div class="hero" style="padding:2rem 2.4rem">
      <div class="badge">ADMINISTRATION PORTAL</div>
      <h1 style="font-size:1.9rem">Admin Control Panel 🛡️</h1>
      <p>Full access — students, teachers, fees & salary</p>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="metric-row">
      <div class="metric-card"><div class="label">Students</div>
        <div class="value val-blue">{len(ss.students)}</div><div class="sub">enrolled</div></div>
      <div class="metric-card"><div class="label">Teachers</div>
        <div class="value val-green">{len(ss.teachers)}</div><div class="sub">on staff</div></div>
      <div class="metric-card"><div class="label">Fee Collection</div>
        <div class="value val-amber">₹{len(ss.students)*30000:,}</div><div class="sub">expected</div></div>
      <div class="metric-card"><div class="label">Salary Outflow</div>
        <div class="value val-red">₹{ss.salary['net'].sum():,}</div><div class="sub">per month</div></div>
    </div>""", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🎓 Students","👩‍🏫 Teachers","💳 Fees","💰 Salary"])

    # ── Students ──
    def crud_table(tab, df_key, id_col, display_name):
        with tab:
            sec_header(display_name.upper())
            act = st.radio("Action",["View All","Add","Update","Delete"],
                           horizontal=True, key=f"adm_{df_key}")
            if act == "View All":
                st.dataframe(getattr(ss, df_key), use_container_width=True, hide_index=True)

            elif act == "Add":
                if df_key == "students":
                    c1, c2 = st.columns(2)
                    adno  = c1.text_input("Admission No.")
                    name  = c1.text_input("Name")
                    dob   = c1.date_input("Date of Birth", date(2003,1,1))
                    phno  = c2.text_input("Phone")
                    gender= c2.selectbox("Gender", ["M","F"])
                    if st.button("➕ Add Student"):
                        new = {"admin_no":adno,"name":name,"dob":str(dob),"phno":phno,"gender":gender}
                        ss.students = pd.concat([ss.students, pd.DataFrame([new])], ignore_index=True)
                        st.success(f"Student {name} added!")
                elif df_key == "teachers":
                    c1, c2 = st.columns(2)
                    tid  = c1.text_input("Teacher ID")
                    name = c1.text_input("Name")
                    doj  = c1.date_input("Date of Joining")
                    phno = c2.text_input("Phone")
                    sub  = c2.selectbox("Subject", SUBJECTS)
                    if st.button("➕ Add Teacher"):
                        new = {"tid":tid,"name":name,"doj":str(doj),"phno":phno,"subject":sub}
                        ss.teachers = pd.concat([ss.teachers, pd.DataFrame([new])], ignore_index=True)
                        st.success(f"Teacher {name} added!")

            elif act == "Update":
                rid = st.text_input(f"Enter {id_col} to update")
                phno = st.text_input("New Phone Number")
                if st.button("💾 Update"):
                    df = getattr(ss, df_key)
                    df.loc[df[id_col] == rid, "phno"] = phno
                    setattr(ss, df_key, df)
                    st.success("Record updated!")

            elif act == "Delete":
                rid = st.text_input(f"Enter {id_col} to delete")
                if st.button("🗑️ Delete"):
                    df = getattr(ss, df_key)
                    setattr(ss, df_key, df[df[id_col] != rid])
                    st.success("Record deleted.")

    crud_table(tab1, "students", "admin_no", "Student Information")
    crud_table(tab2, "teachers", "tid",      "Teacher Information")

    # ── Fees ──
    with tab3:
        sec_header("FEES INFORMATION")
        act = st.radio("Action",["View All","Add Record","Search","Delete"],horizontal=True,key="adm_fees")
        if act == "View All":
            st.dataframe(ss.fees, use_container_width=True, hide_index=True)
        elif act == "Add Record":
            c1, c2 = st.columns(2)
            adno = c1.text_input("Admission No."); name = c2.text_input("Name")
            if st.button("➕ Add Fee Record"):
                new = {"admin_no":adno,"name":name,"amt":30000,
                       "jan_mar":"Pending","apr_jun":"Pending",
                       "jul_sep":"Pending","oct_dec":"Pending"}
                ss.fees = pd.concat([ss.fees, pd.DataFrame([new])], ignore_index=True)
                st.success("Record added!")
        elif act == "Search":
            adno = st.text_input("Admission No.")
            if adno:
                r = ss.fees[ss.fees["admin_no"]==adno]
                if not r.empty: st.dataframe(r, use_container_width=True, hide_index=True)
                else: st.info("Not found.")
        elif act == "Delete":
            adno = st.text_input("Admission No. to Delete")
            if st.button("🗑️ Delete"):
                ss.fees = ss.fees[ss.fees["admin_no"]!=adno]
                st.success("Deleted.")

    # ── Salary ──
    with tab4:
        sec_header("SALARY MANAGEMENT")
        act = st.radio("Action",["View All","Add","Update","Delete"],horizontal=True,key="adm_sal")
        if act == "View All":
            st.dataframe(ss.salary, use_container_width=True, hide_index=True)
        elif act == "Add":
            c1, c2 = st.columns(2)
            tid   = c1.text_input("Teacher ID"); name = c1.text_input("Name")
            allow = c2.number_input("Allowances", 0); ded = c2.number_input("Deductions",0)
            if st.button("➕ Add"):
                basic = 50000; tax = int(basic*0.08)
                net = basic + allow - tax - ded
                new = {"tid":tid,"name":name,"basic":basic,"allow":allow,"tax":tax,"ded":ded,"net":net}
                ss.salary = pd.concat([ss.salary, pd.DataFrame([new])], ignore_index=True)
                st.success("Salary record added!")
        elif act == "Update":
            tid   = st.text_input("Teacher ID to update")
            allow = st.number_input("New Allowances", 0)
            leaves= st.number_input("Leaves (deduction = 1000×leaves)", 0)
            if st.button("💾 Update"):
                ded = leaves * 1000; basic = 50000; tax = int(basic*0.08)
                net = basic + allow - tax - ded
                ss.salary.loc[ss.salary["tid"]==tid, ["allow","ded","net"]] = [allow, ded, net]
                st.success("Salary updated!")
        elif act == "Delete":
            tid = st.text_input("Teacher ID to delete")
            if st.button("🗑️ Delete"):
                ss.salary = ss.salary[ss.salary["tid"]!=tid]
                st.success("Record deleted.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪  Log Out"):
        logout()

# ══════════════════════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════════════════════
if not ss.logged_in:
    page_login()
else:
    if   ss.role == "student": page_student()
    elif ss.role == "teacher": page_teacher()
    elif ss.role == "admin":   page_admin()
    else: page_login()
