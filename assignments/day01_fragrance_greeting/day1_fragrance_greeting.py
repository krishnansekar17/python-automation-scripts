import streamlit as st
from streamlit.components.v1 import html

# ================== CONFIG ==================
st.set_page_config(page_title="Fragrance Greeter", page_icon="💐", layout="centered")

# Dark winter background
BG_IMAGE = "https://4kwallpapers.com/images/walls/thumbs_3t/5591.jpg"

# ================== STYLES ==================
st.markdown(f"""
<style>
.block-container {{
  padding-top: 6rem;
  padding-bottom: 2.5rem;
  max-width: 760px;
  margin: auto;
}}

.stApp {{
  background: url('{BG_IMAGE}') no-repeat center center fixed;
  background-size: cover;
  padding: 0 12px;
}}

@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&display=swap');
.hero-title {{
  display: grid; place-items: center;
  font-family: 'Cinzel Decorative', serif;
  font-weight: 800;
  font-size: clamp(28px, 5vw, 44px);
  color: #3b0d78;
  background: rgba(248, 244, 255, 0.92);
  padding: 18px 24px;
  border-radius: 20px;
  margin: 0 auto 22px auto;
  letter-spacing: 1.2px;
  box-shadow: 0 8px 30px rgba(106,13,173,0.22);
  width: fit-content;
  line-height: 1.2;
}}
.hero-title .line {{ grid-area: 1 / 1; opacity: 0; transform: translateY(6px); animation: swap 4s infinite ease-in-out; white-space: nowrap; }}
.hero-title .one {{ opacity: 1; animation-delay: 0s; }}
.hero-title .two {{ animation-delay: 2s; }}
@keyframes swap {{
  0%   {{ opacity: 0; transform: translateY(6px); }}
  5%   {{ opacity: 1; transform: translateY(0);  }}
  45%  {{ opacity: 1; transform: translateY(0);  }}
  50%  {{ opacity: 0; transform: translateY(-6px); }}
  100% {{ opacity: 0; transform: translateY(-6px); }}
}}

.intro-line {{
  font-size: 17px;
  color: #f8f5ff;
  background: rgba(0,0,0,0.45);
  padding: 12px 18px;
  border-radius: 14px;
  text-align: center;
  margin: 20px auto 24px auto;
  line-height: 1.5;
  backdrop-filter: blur(4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}}

.input-label {{
  display: inline-block;
  font-weight: 600;
  font-size: 15px;
  color: #7C1CEC;
  background: #f4eeff;
  padding: 6px 12px;
  border-radius: 10px;
  margin: 10px 0 6px 0;
}}

div[data-testid="stTextInputRootElement"] {{ background: transparent !important; margin: 0 !important; padding: 0 !important; }}
.stTextInput, .stTextInput>div:first-child {{ background: transparent !important; }}
.stTextInput > div > div > input {{
  background: #f4eeff !important;
  border: 2px solid #ab91ea !important;
  border-radius: 12px !important;
  color: #2c1c48 !important;
  font-size: 16px !important;
  padding: 12px 14px !important;
  box-shadow: none !important;
}}

div[data-testid="stSlider"] {{
  background: #f4eeff !important;
  border: 2px solid #ab91ea !important;
  border-radius: 12px !important;
  padding: 12px 16px 18px 16px !important;
  margin-top: 4px !important;
}}
.stSlider > div[data-baseweb="slider"] {{ background: transparent !important; padding: 0 !important; }}

/* Hide the static "0" and "80" range labels above the slider */
div[data-testid="stThumbValue"] + div > div[role="presentation"] {{
  display: none !important;
}}

.stButton > button {{
  background: linear-gradient(90deg, #bca8ed, #6A0DAD 80%) !important;
  color: #fff !important; font-weight: 700;
  padding: 12px 26px !important;
  border-radius: 14px !important; font-size: 16px !important; border: none;
  box-shadow: 0 4px 18px rgba(123,63,251,0.25) !important;
  margin-top: 10px !important;
}}
.stButton > button:hover {{ background: linear-gradient(90deg, #6A0DAD, #a993ee) !important; }}

.alert {{
  border-radius: 18px;
  padding: 22px;
  margin-top: 22px;
  background: rgba(255,255,255,0.94);
  backdrop-filter: blur(6px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.25);
  border: 2px solid rgba(123,63,251,0.3);
  color: #1f2937;
  text-align: center;
  animation: fadeIn 0.8s ease-in;
}}
@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(10px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
.alert h4 {{ margin: 0 0 8px 0; font-weight: 800; color: #3b0764; font-size: 22px; }}
.alert .meta {{ color: #5b21b6; font-weight: 700; }}
.alert .row-icons {{
  font-size: 30px; letter-spacing: 10px; margin-bottom: 10px;
  animation: float 1.4s cubic-bezier(.81,-0.68,.16,1.3) infinite alternate;
}}
@keyframes float {{ 0% {{transform: translateY(0);}} 100% {{transform: translateY(-6px);}} }}
.alert p {{
  color: #312e81;
  margin-top: 10px;
  font-size: 16px;
  line-height: 1.5;
}}

.err {{
  margin-top: 14px;
  background: rgba(255, 240, 240, 0.95);
  border: 2px solid #fda4af;
  color: #7f1d1d;
  padding: 10px 12px;
  border-radius: 12px;
  font-weight: 600;
  text-align: center;
}}
</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
st.markdown("""
<div class="hero-title" aria-live="polite">
  <span class="line one">Welcome To The Fragrance World!</span>
  <span class="line two">The Winter Is Coming</span>
</div>
""", unsafe_allow_html=True)

# ================== INTRO LINE ==================
st.markdown("""
<div class="intro-line">
  Enter your name and select your age so we can help you find the fragrance collection that perfectly matches your vibe this season.
</div>
""", unsafe_allow_html=True)

# ================== INPUT FIELDS ==================
st.markdown('<span class="input-label">Enter your name</span>', unsafe_allow_html=True)
name = st.text_input("Name", label_visibility="collapsed", key="name_box")

st.markdown('<span class="input-label">Select your age</span>', unsafe_allow_html=True)
age = st.slider("Age", min_value=0, max_value=80, value=0, step=1,
                label_visibility="collapsed", key="age_slider")

submitted = st.button("Show Greeting")

# ================== LOGIC & RESULT ==================
if submitted:
    errors = []
    if not name or not name.strip():
        errors.append("Please enter your name.")
    if age == 0:
        errors.append("Please move the age slider (cannot be 0).")

    if errors:
        st.markdown(f'<div class="err">{" ".join(errors)} 💡</div>', unsafe_allow_html=True)
    else:
        try:
            st.snow()
        except Exception:
            pass

        n = name.strip()
        if age < 25:
            collection = "Fresh Citrus Collection 🍊🍋"
            tip = "Experience our sparkling citrus blends, perfect for lively, youthful days!"
            icon_row = "❄️🍋✨💠❄️"
        elif age < 45:
            collection = "Elegant Floral Collection 🌹🌸"
            tip = "Indulge in timeless florals that inspire confidence and beauty in every moment."
            icon_row = "❄️🌹✨💠❄️"
        else:
            collection = "Classic Woody Collection 🪵🌿"
            tip = "Immerse yourself in rich, classic sophistication that evokes warmth and strength."
            icon_row = "❄️🪵✨💠❄️"

        st.markdown('<div id="greet-result"></div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="alert">
              <div class="row-icons">{icon_row}</div>
              <h4>Hello {n}!</h4>
              <div class="meta">Welcome to The Fragrance World</div>
              <p><b>Your Age:</b> {age}<br>
              <b>Recommended Collection:</b> <span style="color:#6A0DAD;">{collection}</span></p>
              <p>{tip}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        html("""
            <script>
              try {
                const parentDoc = window.parent?.document || document;
                const target = parentDoc.querySelector('#greet-result');
                if (target && target.scrollIntoView) {
                  target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                  parentDoc.documentElement.scrollTo({ top: parentDoc.body.scrollHeight, behavior: 'smooth' });
                }
              } catch (e) {}
            </script>
        """, height=0)
