# day2_goa_expense_splitter_streamlit.py
import streamlit as st
import time

st.set_page_config(page_title="GOA Trip Expense Splitter - FLY EAGLES FLY", layout='wide')

# Background image (Unsplash)
BACKGROUND_URL = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1500&q=80"

# Put ALL CSS inside a Python string so Python never executes raw CSS
CSS = f"""
<style>
[data-testid="stAppViewContainer"] {{
  background-image: url('{BACKGROUND_URL}');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}}
.card {{
  background: rgba(10, 10, 15, 0.78);
  color: #fff;
  border-radius: 12px;
  padding: 14px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.6);
  margin-bottom: 12px;
}}
.person {{
  background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 8px;
}}
.countdown {{
  font-size: 48px;
  color: #ff6b6b;
  margin: 8px 0;
}}
.footer-note {{
  position: fixed;
  bottom: 12px;
  left: 12px;
  color: #cbd5e1;
}}
.button-inline {{
  display: inline-block;
  margin-top: 8px;
}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# --- Data ---
TEAM_NAME = "FLY EAGLES FLY"
PEOPLE = [
    {"name": "Rajaganesh R", "paid": 10000},
    {"name": "Krishnan S", "paid": 8000},
    {"name": "Silambarason Mohan", "paid": 11000},
    {"name": "Sivaraman Karaikudi Sankaranarayan", "paid": 6000},
]
TOTAL_EXPENSE = 90000

# Helpers
def rupee(x):
    try:
        return f"₹{int(x):,}"
    except Exception:
        return f"₹{x}"

# Session state defaults
if 'paid_flags' not in st.session_state:
    st.session_state.paid_flags = {p['name']: False for p in PEOPLE}
if 'show_expense' not in st.session_state:
    st.session_state.show_expense = False
if 'show_countdown' not in st.session_state:
    st.session_state.show_countdown = False
if 'last_payer' not in st.session_state:
    st.session_state.last_payer = ""

# Intro screen
if not st.session_state.show_expense:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"## 🎉 Congrats {PEOPLE[0]['name'].split()[0]}! — {TEAM_NAME} GOA Trip Complete", unsafe_allow_html=True)
    st.markdown("**Click below to reveal expenses & settle up**")
    if st.button("Know your expense 🏖️"):
        # set flag and let the natural rerun on button click render the next state
        st.session_state.show_expense = True
        st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()  # stop so the rest doesn't run on the intro screen

# Main dashboard
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.title(f"GOA Expense Splitter — {TEAM_NAME}")
st.write(f"**Trip squad:** {', '.join(p['name'] for p in PEOPLE)}")
st.write("---")

# Summary
st.subheader("Summary")
st.metric("Total trip expense", rupee(TOTAL_EXPENSE))
equal_share = TOTAL_EXPENSE / len(PEOPLE)
st.metric("Equal split per person", rupee(equal_share))

st.write("---")

# Contributions & settlement
st.subheader("Contributions & Settlement")
for person in PEOPLE:
    name = person['name']
    paid = person['paid']
    owe = equal_share - paid

    cols = st.columns([3, 1])
    with cols[0]:
        st.markdown(f"<div class='person'>", unsafe_allow_html=True)
        st.markdown(f"**{name}**")
        st.markdown(f"Contributed: **{rupee(paid)}**")
        st.markdown(f"Equal share: **{rupee(equal_share)}**")
        if owe > 0:
            st.markdown(f"<b style='color:#ffd166'>{name} owes {rupee(owe)}</b>", unsafe_allow_html=True)
        else:
            st.markdown(f"<b style='color:#86efac'>{name} gets back {rupee(-owe)}</b>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with cols[1]:
        if st.session_state.paid_flags.get(name):
            st.button("Paid ✅", key=f"paid_{name}")
        else:
            # Clicking Pay will set state; because a button click triggers a rerun,
            # the next run will render the countdown block below automatically.
            if st.button("Pay", key=f"pay_{name}"):
                st.session_state.last_payer = name
                st.session_state.paid_flags[name] = True
                st.session_state.show_countdown = True

st.write("---")

# Countdown / Dream modal area (rendered when flag is true)
if st.session_state.get('show_countdown'):
    payer = st.session_state.get('last_payer', '')
    # Center modal-like box
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown("<div class='card' style='text-align:center'>", unsafe_allow_html=True)
        st.markdown(f"### Processing payment for **{payer}**...", unsafe_allow_html=True)
        # Countdown visuals (blocking but simple)
        for i in range(3, 0, -1):
            st.markdown(f"<div class='countdown'>{i}</div>", unsafe_allow_html=True)
            time.sleep(1)
            # allow UI to update between sleeps by a very small script pause
        st.markdown("<h2>⏰ ALARM! Wake up, dreamer!</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#ffd166'>SATHIYAMA NEE GOA POGA MATA</h3>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#60a5fa'>'Elunthu Poi Velaya Paru' — This GOA is a dream only 😴</h4>", unsafe_allow_html=True)
        if st.button("Close Dream", key="close_dream"):
            st.session_state.show_countdown = False
        st.markdown("</div>", unsafe_allow_html=True)

# Footer note
st.markdown(f"<div class='footer-note'>Made with ❤️ for the {TEAM_NAME} — Enjoy your next real Goa trip, {PEOPLE[0]['name'].split()[0]}!</div>", unsafe_allow_html=True)
