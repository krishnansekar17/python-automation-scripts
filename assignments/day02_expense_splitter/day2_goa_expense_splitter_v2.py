import streamlit as st
import streamlit.components.v1 as components
import time

# Page configuration
st.set_page_config(
    page_title="GOA Trip Expense Splitter",
    page_icon="🏖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    /* Main background with GOA image */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.7)), 
                          url('https://images.unsplash.com/photo-1587922546307-776227941871?q=80&w=2070');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove padding */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    iframe {
        border: none;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        color: white;
        font-size: 1.6em;
        font-weight: 700;
        padding: 18px 50px;
        border-radius: 50px;
        border: none;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
        cursor: pointer;
        font-family: 'Poppins', sans-serif;
        width: 100%;
        margin-top: 20px;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.6);
        background: linear-gradient(135deg, #FF8E53 0%, #FF6B6B 100%);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'show_welcome' not in st.session_state:
    st.session_state.show_welcome = True
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False
if 'show_payment_transition' not in st.session_state:
    st.session_state.show_payment_transition = False
if 'show_dream_reveal' not in st.session_state:
    st.session_state.show_dream_reveal = False

# ==================== STEP 1: WELCOME POPUP ====================
if st.session_state.show_welcome:
    
    welcome_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Poppins', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background: transparent;
                padding: 20px;
                overflow-y: auto;
            }
            
            .welcome-popup {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 30px;
                padding: 40px 50px;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
                animation: slideDown 1s ease-out;
                border: 3px solid rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(10px);
                max-width: 900px;
                width: 100%;
            }
            
            @keyframes slideDown {
                from {
                    opacity: 0;
                    transform: translateY(-100px) scale(0.8);
                }
                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
            
            .congrats-text {
                font-size: 3em;
                font-weight: 800;
                color: #FFD700;
                text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.5);
                margin-bottom: 15px;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0%, 100% {
                    transform: scale(1);
                }
                50% {
                    transform: scale(1.05);
                }
            }
            
            .subtitle-text {
                font-size: 1.6em;
                font-weight: 600;
                color: #FFFFFF;
                margin-bottom: 25px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
                line-height: 1.4;
            }
            
            .team-name {
                font-size: 2.5em;
                font-weight: 800;
                color: #FFD700;
                margin: 25px 0;
                text-shadow: 2px 2px 10px rgba(255, 215, 0, 0.8);
                animation: glow 2s ease-in-out infinite;
            }
            
            @keyframes glow {
                0%, 100% {
                    filter: brightness(1);
                }
                50% {
                    filter: brightness(1.3);
                }
            }
            
            .members-container {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 25px;
                margin: 25px 0;
                backdrop-filter: blur(5px);
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            
            .members-title {
                font-size: 1.4em;
                color: #FFD700;
                font-weight: 700;
                margin-bottom: 15px;
            }
            
            .member-name {
                font-size: 1.2em;
                font-weight: 600;
                color: #FFFFFF;
                margin: 10px 0;
                padding: 10px 20px;
                background: linear-gradient(90deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.05));
                border-radius: 15px;
                border-left: 5px solid #FFD700;
                transition: all 0.3s ease;
            }
            
            .member-name:hover {
                transform: translateX(10px);
                background: linear-gradient(90deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.1));
            }
            
            .memories-text {
                font-size: 1.2em;
                color: #FFFFFF;
                margin-top: 25px;
                margin-bottom: 20px;
                font-weight: 500;
                line-height: 1.6;
            }
            
            .emoji-decoration {
                font-size: 2.5em;
                margin: 0 10px;
                animation: bounce 1s infinite;
            }
            
            @keyframes bounce {
                0%, 100% {
                    transform: translateY(0);
                }
                50% {
                    transform: translateY(-20px);
                }
            }
        </style>
    </head>
    <body>
        <div class="welcome-popup">
            <span class="emoji-decoration">🎉</span>
            <span class="emoji-decoration">🏖️</span>
            <span class="emoji-decoration">🎊</span>
            
            <div class="congrats-text">
                🎉 CONGRATULATIONS! 🎉
            </div>
            
            <div class="subtitle-text">
                You've Successfully Completed Your<br>
                <strong>EPIC GOA TRIP OF THE DECADE!</strong> 🌴✨
            </div>
            
            <div class="team-name">
                🦅 FLY EAGLES FLY 🦅
            </div>
            
            <div class="members-container">
                <div class="members-title">
                    🌟 THE LEGENDS 🌟
                </div>
                <div class="member-name">👤 Rajaganesh R</div>
                <div class="member-name">👤 Krishnan S</div>
                <div class="member-name">👤 Silambarason Mohan</div>
                <div class="member-name">👤 Sivaraman Karaikudi Sankaranarayan</div>
            </div>
            
            <div class="memories-text">
                🏝️ 5 Days of Unforgettable Memories 🏝️<br>
                🌊 Sun, Sand & Endless Fun 🌊
            </div>
        </div>
    </body>
    </html>
    """
    
    # Display the HTML without button
    components.html(welcome_html, height=900, scrolling=False)
    
    # Add Streamlit button below
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💰 KNOW YOUR EXPENSES 💰", key="expense_btn"):
            st.session_state.show_welcome = False
            st.session_state.show_dashboard = True
            st.rerun()

# ==================== STEP 2: EXPENSE DASHBOARD ====================
elif st.session_state.show_dashboard:
    
    dashboard_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Poppins', sans-serif;
                background: transparent;
                padding: 20px;
                padding-top: 40px;
                overflow-y: auto;
            }
            
            .dashboard-container {
                max-width: 1200px;
                margin: 0 auto;
                animation: fadeIn 1s ease-out;
            }
            
            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .dashboard-header {
                text-align: center;
                margin-bottom: 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            }
            
            .dashboard-title {
                font-size: 2.5em;
                font-weight: 800;
                color: #FFD700;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
                margin-bottom: 10px;
            }
            
            .team-subtitle {
                font-size: 1.3em;
                color: #FFFFFF;
                font-weight: 600;
            }
            
            /* Expense Breakdown Section */
            .expense-breakdown {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
                border: 2px solid rgba(255, 255, 255, 0.1);
            }
            
            .breakdown-title {
                font-size: 2em;
                font-weight: 700;
                color: #FFD700;
                text-align: center;
                margin-bottom: 25px;
            }
            
            .day-expense {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 15px;
                border-left: 5px solid #4ECDC4;
                transition: all 0.3s ease;
            }
            
            .day-expense:hover {
                transform: translateX(10px);
                background: rgba(255, 255, 255, 0.15);
            }
            
            .day-title {
                font-size: 1.5em;
                font-weight: 700;
                color: #4ECDC4;
                margin-bottom: 15px;
            }
            
            .expense-item {
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                color: #FFFFFF;
                font-size: 1.1em;
            }
            
            .expense-category {
                font-weight: 500;
            }
            
            .expense-amount {
                font-weight: 700;
                color: #FFE66D;
            }
            
            .day-total {
                margin-top: 15px;
                padding-top: 15px;
                border-top: 2px solid rgba(255, 255, 255, 0.3);
                display: flex;
                justify-content: space-between;
                font-size: 1.3em;
                font-weight: 700;
                color: #FFD700;
            }
            
            /* Total Summary */
            .total-summary {
                background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
                text-align: center;
            }
            
            .total-amount {
                font-size: 3em;
                font-weight: 800;
                color: #FFFFFF;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
                margin: 20px 0;
            }
            
            .split-info {
                font-size: 1.5em;
                color: #FFFFFF;
                font-weight: 600;
                margin: 10px 0;
            }
            
            /* Payment Section */
            .payment-section {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
                margin-bottom: 30px;
            }
            
            .payment-title {
                font-size: 2em;
                font-weight: 700;
                color: #FFD700;
                text-align: center;
                margin-bottom: 25px;
            }
            
            .member-payment {
                background: rgba(255, 255, 255, 0.15);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 15px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border: 2px solid rgba(255, 255, 255, 0.3);
                transition: all 0.3s ease;
            }
            
            .member-payment:hover {
                background: rgba(255, 255, 255, 0.2);
                transform: scale(1.02);
            }
            
            .member-info {
                flex: 1;
            }
            
            .member-name-pay {
                font-size: 1.4em;
                font-weight: 700;
                color: #FFFFFF;
                margin-bottom: 8px;
            }
            
            .payment-details {
                font-size: 1.1em;
                color: #FFFFFF;
                font-weight: 600;
            }
            
            .amount-paid {
                color: #4ECDC4;
                font-weight: 700;
            }
            
            .amount-owed {
                color: #FFD700;
                font-weight: 800;
                font-size: 1.15em;
            }
            
            .pay-button {
                background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
                color: white;
                font-size: 1.2em;
                font-weight: 700;
                padding: 15px 40px;
                border-radius: 50px;
                border: none;
                box-shadow: 0 5px 20px rgba(255, 107, 107, 0.4);
                transition: all 0.3s ease;
                cursor: pointer;
                font-family: 'Poppins', sans-serif;
                text-transform: uppercase;
            }
            
            .pay-button:hover {
                transform: translateY(-3px) scale(1.05);
                box-shadow: 0 8px 25px rgba(255, 107, 107, 0.6);
            }
            
            .pay-button:active {
                transform: translateY(-1px) scale(1.02);
            }
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <!-- Header -->
            <div class="dashboard-header">
                <div class="dashboard-title">💰 GOA TRIP EXPENSE DASHBOARD 💰</div>
                <div class="team-subtitle">🦅 FLY EAGLES FLY 🦅</div>
            </div>
            
            <!-- 5-Day Expense Breakdown -->
            <div class="expense-breakdown">
                <div class="breakdown-title">📊 5-Day Expense Breakdown 📊</div>
                
                <!-- Day 1 -->
                <div class="day-expense">
                    <div class="day-title">🌅 Day 1 - Arrival & Check-in</div>
                    <div class="expense-item">
                        <span class="expense-category">🏨 Room</span>
                        <span class="expense-amount">₹8,000</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🚗 Travel</span>
                        <span class="expense-amount">₹5,000</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🍽️ Food</span>
                        <span class="expense-amount">₹3,000</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🍹 Beverages</span>
                        <span class="expense-amount">₹1,500</span>
                    </div>
                    <div class="day-total">
                        <span>Day 1 Total:</span>
                        <span>₹17,500</span>
                    </div>
                </div>
                
                <!-- Day 2 -->
                <div class="day-expense">
                    <div class="day-title">🏖️ Day 2 - Beach Day</div>
                    <div class="expense-item">
                        <span class="expense-category">🏨 Room</span>
                        <span class="expense-amount">₹8,000</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🚤 Water Sports</span>
                        <span class="expense-amount">₹6,000</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🍽️ Food</span>
                        <span class="expense-amount">₹3,500</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🍹 Beverages</span>
                        <span class="expense-amount">₹2,000</span>
                    </div>
                    <div class="day-total">
                        <span>Day 2 Total:</span>
                        <span>₹19,500</span>
                    </div>
                </div>
                
                <!-- Day 3 -->
                <div class="day-expense">
                    <div class="day-title">🏛️ Day 3 - Sightseeing</div>
                    <div class="expense-item">
                        <span class="expense-category">🏨 Room</span>
                        <span class="expense-amount">₹8,000</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🚗 Travel</span>
                        <span class="expense-amount">₹4,000</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🎫 Tourist Spots</span>
                        <span class="expense-amount">₹2,500</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🍽️ Food</span>
                        <span class="expense-amount">₹4,000</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🍹 Beverages</span>
                        <span class="expense-amount">₹1,500</span>
                    </div>
                    <div class="day-total">
                        <span>Day 3 Total:</span>
                        <span>₹20,000</span>
                    </div>
                </div>
                
                <!-- Day 4 -->
                <div class="day-expense">
                    <div class="day-title">🎉 Day 4 - Party Night</div>
                    <div class="expense-item">
                        <span class="expense-category">🏨 Room</span>
                        <span class="expense-amount">₹8,000</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🎊 Club Entry</span>
                        <span class="expense-amount">₹5,000</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🍽️ Food</span>
                        <span class="expense-amount">₹3,500</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🍹 Beverages</span>
                        <span class="expense-amount">₹3,000</span>
                    </div>
                    <div class="day-total">
                        <span>Day 4 Total:</span>
                        <span>₹19,500</span>
                    </div>
                </div>
                
                <!-- Day 5 -->
                <div class="day-expense">
                    <div class="day-title">✈️ Day 5 - Departure</div>
                    <div class="expense-item">
                        <span class="expense-category">🚗 Travel</span>
                        <span class="expense-amount">₹5,000</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🍽️ Food</span>
                        <span class="expense-amount">₹2,500</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🎁 Souvenirs</span>
                        <span class="expense-amount">₹3,000</span>
                    </div>
                    <div class="expense-item">
                        <span class="expense-category">🍹 Beverages</span>
                        <span class="expense-amount">₹3,000</span>
                    </div>
                    <div class="day-total">
                        <span>Day 5 Total:</span>
                        <span>₹13,500</span>
                    </div>
                </div>
            </div>
            
            <!-- Total Summary -->
            <div class="total-summary">
                <div style="font-size: 1.8em; font-weight: 700; color: #FFFFFF;">💵 TOTAL EXPENSES 💵</div>
                <div class="total-amount">₹90,000</div>
                <div class="split-info">📊 Equal Split per Person: ₹22,500</div>
            </div>
            
            <!-- Payment Section -->
            <div class="payment-section">
                <div class="payment-title">💳 Individual Payment Status 💳</div>
                
                <!-- Rajaganesh R -->
                <div class="member-payment">
                    <div class="member-info">
                        <div class="member-name-pay">👤 Rajaganesh R</div>
                        <div class="payment-details">
                            <span class="amount-paid">Paid: ₹10,000</span> | 
                            <span class="amount-owed">Owes: ₹12,500</span>
                        </div>
                    </div>
                    <button class="pay-button" onclick="window.parent.postMessage('pay_clicked', '*')">
                        💰 PAY NOW
                    </button>
                </div>
                
                <!-- Krishnan S -->
                <div class="member-payment">
                    <div class="member-info">
                        <div class="member-name-pay">👤 Krishnan S</div>
                        <div class="payment-details">
                            <span class="amount-paid">Paid: ₹8,000</span> | 
                            <span class="amount-owed">Owes: ₹14,500</span>
                        </div>
                    </div>
                    <button class="pay-button" onclick="window.parent.postMessage('pay_clicked', '*')">
                        💰 PAY NOW
                    </button>
                </div>
                
                <!-- Silambarason Mohan -->
                <div class="member-payment">
                    <div class="member-info">
                        <div class="member-name-pay">👤 Silambarason Mohan</div>
                        <div class="payment-details">
                            <span class="amount-paid">Paid: ₹11,000</span> | 
                            <span class="amount-owed">Owes: ₹11,500</span>
                        </div>
                    </div>
                    <button class="pay-button" onclick="window.parent.postMessage('pay_clicked', '*')">
                        💰 PAY NOW
                    </button>
                </div>
                
                <!-- Sivaraman Karaikudi Sankaranarayan -->
                <div class="member-payment">
                    <div class="member-info">
                        <div class="member-name-pay">👤 Sivaraman Karaikudi Sankaranarayan</div>
                        <div class="payment-details">
                            <span class="amount-paid">Paid: ₹6,000</span> | 
                            <span class="amount-owed">Owes: ₹16,500</span>
                        </div>
                    </div>
                    <button class="pay-button" onclick="window.parent.postMessage('pay_clicked', '*')">
                        💰 PAY NOW
                    </button>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Display dashboard HTML
    components.html(dashboard_html, height=2100, scrolling=True)
    
    # Add a fallback button at the bottom
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💰 PROCEED TO PAYMENT 💰", key="proceed_payment_btn"):
            st.session_state.show_dashboard = False
            st.session_state.show_payment_transition = True
            st.rerun()

# ==================== STEP 2.5: PAYMENT TRANSITION WITH COUNTDOWN ====================
elif st.session_state.show_payment_transition:
    
    transition_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                overflow: hidden;
            }
            
            .container {
                text-align: center;
                width: 100%;
                padding: 20px;
            }
            
            /* Phase 1: Connecting Message */
            .connecting-phase {
                display: block;
                animation: fadeIn 0.8s ease-in;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: scale(0.8); }
                to { opacity: 1; transform: scale(1); }
            }
            
            .connecting-text {
                font-size: 4em;
                font-weight: 900;
                color: #FFFFFF;
                text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
                letter-spacing: 3px;
                animation: pulse 1.5s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.05); opacity: 0.9; }
            }
            
            .loading-dots {
                font-size: 4em;
                color: #FFD700;
                margin-top: 20px;
                animation: blink 1s infinite;
            }
            
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.3; }
            }
            
            /* Phase 2: Countdown */
            .countdown-phase {
                display: none;
            }
            
            .countdown-number {
                font-size: 20em;
                font-weight: 900;
                color: #FFD700;
                text-shadow: 0 0 80px rgba(255, 215, 0, 0.8);
                animation: popOut 0.6s ease-out;
            }
            
            @keyframes popOut {
                0% {
                    transform: scale(0);
                    opacity: 0;
                }
                50% {
                    transform: scale(1.3);
                }
                100% {
                    transform: scale(1);
                    opacity: 1;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Phase 1: Connecting Message -->
            <div class="connecting-phase" id="connectingPhase">
                <div class="connecting-text">
                    💳 CONNECTING TO<br>PAYMENT METHOD 💳
                </div>
                <div class="loading-dots">...</div>
            </div>
            
            <!-- Phase 2: Countdown -->
            <div class="countdown-phase" id="countdownPhase">
                <div class="countdown-number" id="countdownNumber">3</div>
            </div>
        </div>
        
        <script>
            let countdown = 3;
            
            // Phase 1: Show connecting message for 3 seconds
            setTimeout(() => {
                document.getElementById('connectingPhase').style.display = 'none';
                document.getElementById('countdownPhase').style.display = 'block';
                
                // Phase 2: Countdown from 3 to 1
                const countdownInterval = setInterval(() => {
                    const numberElement = document.getElementById('countdownNumber');
                    numberElement.style.animation = 'none';
                    
                    setTimeout(() => {
                        numberElement.style.animation = 'popOut 0.6s ease-out';
                        numberElement.textContent = countdown;
                    }, 10);
                    
                    countdown--;
                    
                    if (countdown < 1) {
                        clearInterval(countdownInterval);
                        // Auto-proceed to next step after countdown
                        setTimeout(() => {
                            window.parent.postMessage('countdown_complete', '*');
                        }, 600);
                    }
                }, 700); // 0.7 seconds per number
                
            }, 3000); // 3 seconds for connecting message
        </script>
    </body>
    </html>
    """
    
    components.html(transition_html, height=900, scrolling=False)
    
    # Auto-advance after the transition completes (3s + 3*0.7s = ~5.1s total)
    time.sleep(5.5)
    st.session_state.show_payment_transition = False
    st.session_state.show_dream_reveal = True
    st.rerun()

# ==================== STEP 3: DREAM REVEAL (THE MAGIC!) ====================
elif st.session_state.show_dream_reveal:
    
    dream_reveal_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                overflow: hidden;
                transition: background 1s ease;
            }
            
            .container {
                text-align: center;
                width: 100%;
                padding: 20px;
            }
            
            /* Phase 1: Alarm with Warning Text */
            .alarm-phase {
                display: block;
                animation: fadeIn 0.5s ease-in;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            .alarm-emoji {
                font-size: 15em;
                animation: shake 0.5s infinite, pulse 1s infinite;
                filter: drop-shadow(0 0 50px rgba(255, 0, 0, 0.8));
            }
            
            @keyframes shake {
                0%, 100% { transform: rotate(-15deg); }
                50% { transform: rotate(15deg); }
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
            
            .warning-text {
                font-size: 3.5em;
                font-weight: 900;
                color: #FF0000;
                text-shadow: 0 0 30px rgba(255, 0, 0, 0.8);
                margin-top: 30px;
                animation: blink 0.8s infinite;
                letter-spacing: 3px;
            }
            
            @keyframes blink {
                0%, 50%, 100% { opacity: 1; }
                25%, 75% { opacity: 0.3; }
            }
            
            /* Phase 2: Wake Up Reality */
            .reality-phase {
                display: none;
                animation: fadeIn 1s ease-in;
            }
            
            .wake-up-gif {
                width: 600px;
                max-width: 90%;
                border-radius: 20px;
                margin-bottom: 50px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
                border: 5px solid rgba(255, 255, 255, 0.2);
            }
            
            .reality-message {
                font-size: 4em;
                font-weight: 900;
                line-height: 1.4;
                animation: colorWave 3s infinite, scaleUp 1.5s ease-out;
                background: linear-gradient(45deg, #FF6B6B, #FFD700, #FF8E53, #FF6B6B);
                background-size: 300% 300%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 0 0 40px rgba(255, 107, 107, 0.5);
                padding: 20px;
            }
            
            @keyframes colorWave {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            @keyframes scaleUp {
                from {
                    transform: scale(0.3);
                    opacity: 0;
                }
                to {
                    transform: scale(1);
                    opacity: 1;
                }
            }
            
            /* Background color transition */
            body.reality-bg {
                background: linear-gradient(135deg, #2c003e 0%, #1a0033 50%, #0d001a 100%);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Phase 1: Alarm Clock with Warning -->
            <div class="alarm-phase" id="alarmPhase">
                <div class="alarm-emoji">⏰</div>
                <div class="warning-text">
                    YOU ARE IN DREAM, WAKE UP!<br>
                    YOU ARE IN DREAM, WAKE UP!
                </div>
            </div>
            
            <!-- Phase 2: Reality Check -->
            <div class="reality-phase" id="realityPhase">
                <img src="https://media1.tenor.com/m/vPu6l5lOPecAAAAd/goa-premji.gif" alt="Waking Up Sad" class="wake-up-gif">
                <div class="reality-message">
                    APPO INTHA JENMATHUKU<br>
                    GOA POGA MUDIYATHA 😭
                </div>
            </div>
        </div>
        
        <!-- Audio Element -->
        <audio id="alarmSound" loop>
            <source src="https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3" type="audio/mpeg">
        </audio>
        
        <script>
            // Phase 1: Show alarm with sound for 5 seconds
            const alarmSound = document.getElementById('alarmSound');
            alarmSound.volume = 0.6;
            alarmSound.play();
            
            setTimeout(() => {
                // Stop alarm sound
                alarmSound.pause();
                
                // Hide alarm phase
                document.getElementById('alarmPhase').style.display = 'none';
                
                // Show reality phase with background change
                document.getElementById('realityPhase').style.display = 'block';
                document.body.classList.add('reality-bg');
            }, 5000); // 5 seconds
        </script>
    </body>
    </html>
    """
    
    components.html(dream_reveal_html, height=900, scrolling=False)

else:
    st.markdown("<h1 style='text-align: center; color: white; margin-top: 200px;'>Something went wrong...</h1>", unsafe_allow_html=True)