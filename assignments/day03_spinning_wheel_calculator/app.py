import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Spinning Wheel Calculator",
    page_icon="🎡",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .stButton > button {
        width: 100%;
        height: 45px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        border: 2px solid #ddd;
        background-color: white !important;
        color: #333 !important;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background-color: #f0f0f0 !important;
        border-color: #999;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_operation' not in st.session_state:
    st.session_state.selected_operation = None
if 'display' not in st.session_state:
    st.session_state.display = ""
if 'num1' not in st.session_state:
    st.session_state.num1 = None
if 'result' not in st.session_state:
    st.session_state.result = None

# Title
st.markdown("<h1 style='text-align: center;'>🎡 Spinning Wheel Calculator</h1>", unsafe_allow_html=True)

# Instruction
st.markdown("""
<div style='text-align: center; margin: 20px 0;'>
    <p style='font-size: 22px; font-weight: bold; 
    background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #FFA07A, #98D8C8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;'>
    ✨ Choose the Operator from the below Spinning Board to get your dedicated calculator! ✨
    </p>
</div>
""", unsafe_allow_html=True)

# Spinning wheel
wheel_html = """
<style>
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .wheel-wrapper {
        display: flex;
        justify-content: center;
        margin: 40px auto;
        position: relative;
        width: 416px;
        height: 416px;
    }
    
    .spinning-wheel {
        width: 416px;
        height: 416px;
        border-radius: 50%;
        position: relative;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        border: 8px solid #333;
        overflow: hidden;
        background: white;
        animation: spin 3s ease-out;
    }
    
    .segment {
        position: absolute;
        width: 208px;
        height: 208px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        cursor: pointer;
        transition: filter 0.2s;
        text-decoration: none!important;
    }
    .segment, .segment:hover, .segment:visited, .segment:active {
    text-decoration: none !important;
}
    
    .segment:hover {
        filter: brightness(1.2);
    }
    
    .segment-add {
        background: #4CAF50;
        top: 0;
        right: 0;
        border-radius: 0 0 0 100%;
    }
    
    .segment-subtract {
        background: #2196F3;
        bottom: 0;
        right: 0;
        border-radius: 100% 0 0 0;
    }
    
    .segment-multiply {
        background: #9C27B0;
        bottom: 0;
        left: 0;
        border-radius: 0 100% 0 0;
    }
    
    .segment-divide {
        background: #FF9800;
        top: 0;
        left: 0;
        border-radius: 0 0 100% 0;
    }
    
    .operator {
        font-size: 60px;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        pointer-events: none;
    }
    
    .label {
        font-size: 18px;
        margin-top: 5px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        pointer-events: none;
    }
    
    .center-dot {
        position: absolute;
        width: 40px;
        height: 40px;
        background: white;
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border: 3px solid #333;
        z-index: 10;
        pointer-events: none;
    }
</style>

<div class="wheel-wrapper">
    <div class="spinning-wheel">
        <a href="?op=addition" target="_self" class="segment segment-add">
            <div class="operator">+</div>
            <div class="label">Add</div>
        </a>
        <a href="?op=subtraction" target="_self" class="segment segment-subtract">
            <div class="operator">−</div>
            <div class="label">Subtract</div>
        </a>
        <a href="?op=multiplication" target="_self" class="segment segment-multiply">
            <div class="operator">×</div>
            <div class="label">Multiply</div>
        </a>
        <a href="?op=division" target="_self" class="segment segment-divide">
            <div class="operator">÷</div>
            <div class="label">Divide</div>
        </a>
        <div class="center-dot"></div>
    </div>
</div>
"""

st.markdown(wheel_html, unsafe_allow_html=True)

# Get query parameters
query_params = st.query_params
if 'op' in query_params:
    if st.session_state.selected_operation != query_params['op']:
        st.session_state.selected_operation = query_params['op']
        st.session_state.display = ""
        st.session_state.num1 = None
        st.session_state.result = None

# Show calculator
if st.session_state.selected_operation:
    
    # ADDITION CALCULATOR
    if st.session_state.selected_operation == "addition":
        # Use Streamlit container with custom styling
        with st.container():
            st.markdown("""
            <div style='text-align: center; font-size: 22px; font-weight: bold; color: #ffffff; margin: 15px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                Let's Add Some Magic! ✨ Time to Sum Things Up!
            </div>
            <style>
            div[data-testid="stVerticalBlock"] > div:has(div.addition-calc) {
                background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%) !important;
                padding: 25px !important;
                border-radius: 20px !important;
                max-width: 450px !important;
                margin: 0 auto 30px auto !important;
                box-shadow: 0 10px 30px rgba(76, 175, 80, 0.4) !important;
            }
            </style>
            <div class="addition-calc" style="display:none;"></div>
            """, unsafe_allow_html=True)
            
            display_text = st.session_state.result if st.session_state.result else (st.session_state.display if st.session_state.display else "0")
            
            st.markdown(f"""
            <div style='background: #1a1a1a; color: #00ff00; padding: 18px; 
                        border-radius: 10px; font-size: 24px; font-family: "Courier New", monospace;
                        text-align: right; min-height: 55px; margin-bottom: 18px;
                        box-shadow: inset 0 4px 10px rgba(0,0,0,0.5); 
                        word-wrap: break-word; overflow-wrap: break-word;'>
                {display_text}
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("7", key="a7"):
                    st.session_state.display = "7" if st.session_state.result else st.session_state.display + "7"
                    st.session_state.result = None
                    st.rerun()
                if st.button("4", key="a4"):
                    st.session_state.display = "4" if st.session_state.result else st.session_state.display + "4"
                    st.session_state.result = None
                    st.rerun()
                if st.button("1", key="a1"):
                    st.session_state.display = "1" if st.session_state.result else st.session_state.display + "1"
                    st.session_state.result = None
                    st.rerun()
            with col2:
                if st.button("8", key="a8"):
                    st.session_state.display = "8" if st.session_state.result else st.session_state.display + "8"
                    st.session_state.result = None
                    st.rerun()
                if st.button("5", key="a5"):
                    st.session_state.display = "5" if st.session_state.result else st.session_state.display + "5"
                    st.session_state.result = None
                    st.rerun()
                if st.button("2", key="a2"):
                    st.session_state.display = "2" if st.session_state.result else st.session_state.display + "2"
                    st.session_state.result = None
                    st.rerun()
            with col3:
                if st.button("9", key="a9"):
                    st.session_state.display = "9" if st.session_state.result else st.session_state.display + "9"
                    st.session_state.result = None
                    st.rerun()
                if st.button("6", key="a6"):
                    st.session_state.display = "6" if st.session_state.result else st.session_state.display + "6"
                    st.session_state.result = None
                    st.rerun()
                if st.button("3", key="a3"):
                    st.session_state.display = "3" if st.session_state.result else st.session_state.display + "3"
                    st.session_state.result = None
                    st.rerun()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("0", key="a0"):
                    st.session_state.display = "0" if st.session_state.result else st.session_state.display + "0"
                    st.session_state.result = None
                    st.rerun()
            with col2:
                if st.button(".", key="adot"):
                    if st.session_state.result:
                        st.session_state.display = "0."
                        st.session_state.result = None
                    elif '.' not in st.session_state.display:
                        st.session_state.display += "." if st.session_state.display else "0."
                    st.rerun()
            with col3:
                if st.button("C", key="aclear"):
                    st.session_state.display = ""
                    st.session_state.num1 = None
                    st.session_state.result = None
                    st.rerun()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➕ SET", key="aset"):
                    if st.session_state.display:
                        st.session_state.num1 = float(st.session_state.display)
                        st.session_state.display = ""
                        st.session_state.result = None
                    st.rerun()
            with col2:
                if st.button("= CALC", key="acalc"):
                    if st.session_state.display and st.session_state.num1 is not None:
                        num2 = float(st.session_state.display)
                        result = st.session_state.num1 + num2
                        st.session_state.result = f"{st.session_state.num1} + {num2} = {result}"
                        st.session_state.display = str(result)
                    st.rerun()
    
    # SUBTRACTION CALCULATOR
    elif st.session_state.selected_operation == "subtraction":
        with st.container():
            st.markdown("""
            <div style='text-align: center; font-size: 22px; font-weight: bold; color: #ffffff; margin: 15px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                Subtract & Conquer! 💪 Let's Take Things Away!
            </div>
            <style>
            div[data-testid="stVerticalBlock"] > div:has(div.subtract-calc) {
                background: linear-gradient(135deg, #2196F3 0%, #64B5F6 100%) !important;
                padding: 25px !important;
                border-radius: 15px !important;
                max-width: 480px !important;
                margin: 0 auto 30px auto !important;
                box-shadow: 0 10px 30px rgba(33, 150, 243, 0.4) !important;
            }
            </style>
            <div class="subtract-calc" style="display:none;"></div>
            """, unsafe_allow_html=True)
            
            display_text = st.session_state.result if st.session_state.result else (st.session_state.display if st.session_state.display else "0")
            
            st.markdown(f"""
            <div style='background: #0d47a1; color: #ffffff; padding: 18px; 
                        border-radius: 8px; font-size: 24px; font-family: Arial, sans-serif;
                        text-align: right; min-height: 55px; margin-bottom: 18px;
                        box-shadow: inset 0 4px 10px rgba(0,0,0,0.5); border: 3px solid #1565c0;
                        word-wrap: break-word; overflow-wrap: break-word;'>
                {display_text}
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("7", key="s7"):
                    st.session_state.display = "7" if st.session_state.result else st.session_state.display + "7"
                    st.session_state.result = None
                    st.rerun()
                if st.button("4", key="s4"):
                    st.session_state.display = "4" if st.session_state.result else st.session_state.display + "4"
                    st.session_state.result = None
                    st.rerun()
                if st.button("1", key="s1"):
                    st.session_state.display = "1" if st.session_state.result else st.session_state.display + "1"
                    st.session_state.result = None
                    st.rerun()
                if st.button("0", key="s0"):
                    st.session_state.display = "0" if st.session_state.result else st.session_state.display + "0"
                    st.session_state.result = None
                    st.rerun()
            with col2:
                if st.button("8", key="s8"):
                    st.session_state.display = "8" if st.session_state.result else st.session_state.display + "8"
                    st.session_state.result = None
                    st.rerun()
                if st.button("5", key="s5"):
                    st.session_state.display = "5" if st.session_state.result else st.session_state.display + "5"
                    st.session_state.result = None
                    st.rerun()
                if st.button("2", key="s2"):
                    st.session_state.display = "2" if st.session_state.result else st.session_state.display + "2"
                    st.session_state.result = None
                    st.rerun()
                if st.button(".", key="sdot"):
                    if st.session_state.result:
                        st.session_state.display = "0."
                        st.session_state.result = None
                    elif '.' not in st.session_state.display:
                        st.session_state.display += "." if st.session_state.display else "0."
                    st.rerun()
            with col3:
                if st.button("9", key="s9"):
                    st.session_state.display = "9" if st.session_state.result else st.session_state.display + "9"
                    st.session_state.result = None
                    st.rerun()
                if st.button("6", key="s6"):
                    st.session_state.display = "6" if st.session_state.result else st.session_state.display + "6"
                    st.session_state.result = None
                    st.rerun()
                if st.button("3", key="s3"):
                    st.session_state.display = "3" if st.session_state.result else st.session_state.display + "3"
                    st.session_state.result = None
                    st.rerun()
                if st.button("C", key="sclear"):
                    st.session_state.display = ""
                    st.session_state.num1 = None
                    st.session_state.result = None
                    st.rerun()
            with col4:
                if st.button("➖ SET", key="sset"):
                    if st.session_state.display:
                        st.session_state.num1 = float(st.session_state.display)
                        st.session_state.display = ""
                        st.session_state.result = None
                    st.rerun()
                if st.button("= CALC", key="scalc"):
                    if st.session_state.display and st.session_state.num1 is not None:
                        num2 = float(st.session_state.display)
                        result = st.session_state.num1 - num2
                        st.session_state.result = f"{st.session_state.num1} - {num2} = {result}"
                        st.session_state.display = str(result)
                    st.rerun()
    
    # MULTIPLICATION CALCULATOR
    elif st.session_state.selected_operation == "multiplication":
        with st.container():
            st.markdown("""
            <div style='text-align: center; font-size: 22px; font-weight: bold; color: #ffffff; margin: 15px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                Multiply the Fun! 🎉 Let's Make It Bigger!
            </div>
            <style>
            div[data-testid="stVerticalBlock"] > div:has(div.multiply-calc) {
                background: linear-gradient(135deg, #9C27B0 0%, #E91E63 100%) !important;
                padding: 25px !important;
                border-radius: 40px !important;
                max-width: 450px !important;
                margin: 0 auto 30px auto !important;
                box-shadow: 0 10px 30px rgba(156, 39, 176, 0.5) !important;
            }
            </style>
            <div class="multiply-calc" style="display:none;"></div>
            """, unsafe_allow_html=True)
            
            display_text = st.session_state.result if st.session_state.result else (st.session_state.display if st.session_state.display else "0")
            
            st.markdown(f"""
            <div style='background: #000000; color: #ff00ff; padding: 18px; 
                        border-radius: 20px; font-size: 24px; font-family: "Courier New", monospace;
                        text-align: center; min-height: 55px; margin-bottom: 18px;
                        box-shadow: 0 0 20px rgba(255, 0, 255, 0.5); border: 4px solid #6a1b9a;
                        word-wrap: break-word; overflow-wrap: break-word;'>
                {display_text}
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("7", key="m7"):
                    st.session_state.display = "7" if st.session_state.result else st.session_state.display + "7"
                    st.session_state.result = None
                    st.rerun()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("4", key="m4"):
                    st.session_state.display = "4" if st.session_state.result else st.session_state.display + "4"
                    st.session_state.result = None
                    st.rerun()
            with col2:
                if st.button("8", key="m8"):
                    st.session_state.display = "8" if st.session_state.result else st.session_state.display + "8"
                    st.session_state.result = None
                    st.rerun()
            with col3:
                if st.button("6", key="m6"):
                    st.session_state.display = "6" if st.session_state.result else st.session_state.display + "6"
                    st.session_state.result = None
                    st.rerun()
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("2", key="m2"):
                    st.session_state.display = "2" if st.session_state.result else st.session_state.display + "2"
                    st.session_state.result = None
                    st.rerun()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("1", key="m1"):
                    st.session_state.display = "1" if st.session_state.result else st.session_state.display + "1"
                    st.session_state.result = None
                    st.rerun()
            with col2:
                if st.button("5", key="m5"):
                    st.session_state.display = "5" if st.session_state.result else st.session_state.display + "5"
                    st.session_state.result = None
                    st.rerun()
            with col3:
                if st.button("9", key="m9"):
                    st.session_state.display = "9" if st.session_state.result else st.session_state.display + "9"
                    st.session_state.result = None
                    st.rerun()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("0", key="m0"):
                    st.session_state.display = "0" if st.session_state.result else st.session_state.display + "0"
                    st.session_state.result = None
                    st.rerun()
            with col2:
                if st.button("3", key="m3"):
                    st.session_state.display = "3" if st.session_state.result else st.session_state.display + "3"
                    st.session_state.result = None
                    st.rerun()
            with col3:
                if st.button(".", key="mdot"):
                    if st.session_state.result:
                        st.session_state.display = "0."
                        st.session_state.result = None
                    elif '.' not in st.session_state.display:
                        st.session_state.display += "." if st.session_state.display else "0."
                    st.rerun()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("C", key="mclear"):
                    st.session_state.display = ""
                    st.session_state.num1 = None
                    st.session_state.result = None
                    st.rerun()
            with col2:
                if st.button("✖️ SET", key="mset"):
                    if st.session_state.display:
                        st.session_state.num1 = float(st.session_state.display)
                        st.session_state.display = ""
                        st.session_state.result = None
                    st.rerun()
            with col3:
                if st.button("= CALC", key="mcalc"):
                    if st.session_state.display and st.session_state.num1 is not None:
                        num2 = float(st.session_state.display)
                        result = st.session_state.num1 * num2
                        st.session_state.result = f"{st.session_state.num1} × {num2} = {result}"
                        st.session_state.display = str(result)
                    st.rerun()
    
    # DIVISION CALCULATOR
    elif st.session_state.selected_operation == "division":
        with st.container():
            st.markdown("""
            <div style='text-align: center; font-size: 22px; font-weight: bold; color: #ffffff; margin: 15px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                Divide & Rule! 👑 Let's Split It Up!
            </div>
            <style>
            div[data-testid="stVerticalBlock"] > div:has(div.divide-calc) {
                background: linear-gradient(135deg, #FF9800 0%, #F44336 100%) !important;
                padding: 25px 20px !important;
                border-radius: 25px 25px 40px 40px !important;
                max-width: 380px !important;
                margin: 0 auto 30px auto !important;
                box-shadow: 0 10px 30px rgba(255, 152, 0, 0.5) !important;
            }
            </style>
            <div class="divide-calc" style="display:none;"></div>
            """, unsafe_allow_html=True)
            
            display_text = st.session_state.result if st.session_state.result else (st.session_state.display if st.session_state.display else "0")
            
            st.markdown(f"""
            <div style='background: #1b5e20; color: #76ff03; padding: 18px; 
                        border-radius: 10px; font-size: 24px; font-family: "Digital", monospace;
                        text-align: right; min-height: 55px; margin-bottom: 18px;
                        box-shadow: inset 0 3px 8px rgba(0,0,0,0.6); border: 2px solid #2e7d32;
                        word-wrap: break-word; overflow-wrap: break-word;'>
                {display_text}
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("1", key="d1"):
                    st.session_state.display = "1" if st.session_state.result else st.session_state.display + "1"
                    st.session_state.result = None
                    st.rerun()
            with col2:
                if st.button("2", key="d2"):
                    st.session_state.display = "2" if st.session_state.result else st.session_state.display + "2"
                    st.session_state.result = None
                    st.rerun()
            with col3:
                if st.button("3", key="d3"):
                    st.session_state.display = "3" if st.session_state.result else st.session_state.display + "3"
                    st.session_state.result = None
                    st.rerun()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("4", key="d4"):
                    st.session_state.display = "4" if st.session_state.result else st.session_state.display + "4"
                    st.session_state.result = None
                    st.rerun()
            with col2:
                if st.button("5", key="d5"):
                    st.session_state.display = "5" if st.session_state.result else st.session_state.display + "5"
                    st.session_state.result = None
                    st.rerun()
            with col3:
                if st.button("6", key="d6"):
                    st.session_state.display = "6" if st.session_state.result else st.session_state.display + "6"
                    st.session_state.result = None
                    st.rerun()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("7", key="d7"):
                    st.session_state.display = "7" if st.session_state.result else st.session_state.display + "7"
                    st.session_state.result = None
                    st.rerun()
            with col2:
                if st.button("8", key="d8"):
                    st.session_state.display = "8" if st.session_state.result else st.session_state.display + "8"
                    st.session_state.result = None
                    st.rerun()
            with col3:
                if st.button("9", key="d9"):
                    st.session_state.display = "9" if st.session_state.result else st.session_state.display + "9"
                    st.session_state.result = None
                    st.rerun()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(".", key="ddot"):
                    if st.session_state.result:
                        st.session_state.display = "0."
                        st.session_state.result = None
                    elif '.' not in st.session_state.display:
                        st.session_state.display += "." if st.session_state.display else "0."
                    st.rerun()
            with col2:
                if st.button("0", key="d0"):
                    st.session_state.display = "0" if st.session_state.result else st.session_state.display + "0"
                    st.session_state.result = None
                    st.rerun()
            with col3:
                if st.button("C", key="dclear"):
                    st.session_state.display = ""
                    st.session_state.num1 = None
                    st.session_state.result = None
                    st.rerun()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➗ SET", key="dset"):
                    if st.session_state.display:
                        st.session_state.num1 = float(st.session_state.display)
                        st.session_state.display = ""
                        st.session_state.result = None
                    st.rerun()
            with col2:
                if st.button("= CALC", key="dcalc"):
                    if st.session_state.display and st.session_state.num1 is not None:
                        num2 = float(st.session_state.display)
                        if num2 != 0:
                            result = st.session_state.num1 / num2
                            st.session_state.result = f"{st.session_state.num1} ÷ {num2} = {result}"
                            st.session_state.display = str(result)
                        else:
                            st.session_state.result = "Error: Division by Zero!"
                            st.session_state.display = "Error"
                    st.rerun()