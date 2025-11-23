import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Currency Converter 💰",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for elegant styling with black background
st.markdown("""
    <style>
    /* Main background - Pure Black */
    .stApp {
        background: #000000;
    }
    
    /* Main container styling */
    .main-container {
        background: rgba(20, 20, 20, 0.95);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(255, 215, 0, 0.2);
        margin: 2rem auto;
        max-width: 600px;
        border: 2px solid #FFD700;
    }
    
    /* Title styling - Golden Yellow */
    .title {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        color: #FFD700;
        margin-bottom: 0.5rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    }
    
    /* Subtitle styling - Golden Yellow */
    .subtitle {
        text-align: center;
        color: #FFD700;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* H3 headings - Golden Yellow */
    h3 {
        color: #FFD700 !important;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
    }
    
    /* Input section styling */
    .stNumberInput > div > div > input {
        font-size: 1.3rem;
        font-weight: 600;
        border: 2px solid #FFD700;
        border-radius: 12px;
        padding: 0.8rem;
        transition: all 0.3s ease;
        background-color: #1a1a1a;
        color: #FFB6C1;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #FFD700;
        box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.3);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid #FFD700;
        transition: all 0.3s ease;
        background-color: #1a1a1a;
    }
    
    .stSelectbox > div > div > div {
        color: #FFB6C1;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #FFD700;
        box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.3);
    }
    
    /* Result box styling */
    .result-box {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.4);
        animation: slideIn 0.5s ease;
        border: 3px solid #FFD700;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-amount {
        font-size: 3rem;
        font-weight: 800;
        color: #000000;
        margin: 0.5rem 0;
        text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.3);
    }
    
    .result-label {
        font-size: 1.2rem;
        color: #000000;
        font-weight: 600;
    }
    
    /* Exchange rate info */
    .rate-info {
        background: #1a1a1a;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: #FFB6C1;
        font-size: 0.95rem;
        border-left: 4px solid #FFD700;
        margin: 1rem 0;
        border: 2px solid #FFD700;
    }
    
    .rate-info strong {
        color: #FFD700;
    }
    
    /* Currency symbols */
    .currency-symbol {
        font-size: 2rem;
        margin: 0 1rem;
    }
    
    /* Labels - Golden Yellow */
    .stSelectbox label, .stNumberInput label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #FFD700 !important;
    }
    
    /* Swap button area */
    .swap-container {
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #000000;
        font-weight: 700;
        border: 2px solid #FFD700;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FFA500 0%, #FFD700 100%);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5);
        transform: translateY(-2px);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #FFB6C1;
        font-size: 0.9rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #FFD700;
    }
    
    .footer strong {
        color: #FFD700;
    }
    
    /* Remove default streamlit padding */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #1a4d2e;
        color: #FFD700;
        border-radius: 10px;
        padding: 1rem;
        font-weight: 600;
        border: 2px solid #FFD700;
    }
    
    /* Info message styling */
    .stInfo {
        background-color: #1a1a1a;
        color: #FFB6C1;
        border-radius: 10px;
        padding: 1rem;
        font-weight: 600;
        border: 2px solid #FFD700;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #1a1a1a;
        color: #FFD700 !important;
        border: 2px solid #FFD700;
        border-radius: 10px;
        font-weight: 600;
    }
    
    .streamlit-expanderContent {
        background-color: #0a0a0a;
        border: 2px solid #FFD700;
        border-top: none;
        color: #FFB6C1;
    }
    
    /* Metric styling */
    .stMetric {
        background-color: #1a1a1a;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #FFD700;
    }
    
    .stMetric label {
        color: #FFD700 !important;
        font-weight: 600;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #FFB6C1 !important;
    }
    
    /* Horizontal rule */
    hr {
        border-color: #FFD700;
        opacity: 0.5;
    }
    
    /* Markdown text color */
    .stMarkdown {
        color: #FFB6C1;
    }
    
    /* Expander content text */
    div[data-testid="stExpander"] div[role="button"] p {
        color: #FFD700 !important;
        font-weight: 600;
    }
    
    div[data-testid="stExpander"] div:not([role="button"]) p {
        color: #FFB6C1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Static exchange rates (base: 1 unit of currency)
EXCHANGE_RATES = {
    'INR': {
        'INR': 1.0,
        'USD': 0.012,
        'EUR': 0.011,
        'GBP': 0.0095
    },
    'USD': {
        'INR': 83.50,
        'USD': 1.0,
        'EUR': 0.92,
        'GBP': 0.79
    },
    'EUR': {
        'INR': 90.80,
        'USD': 1.09,
        'EUR': 1.0,
        'GBP': 0.86
    },
    'GBP': {
        'INR': 105.50,
        'USD': 1.26,
        'EUR': 1.16,
        'GBP': 1.0
    }
}

# Currency symbols
CURRENCY_SYMBOLS = {
    'INR': '₹',
    'USD': '$',
    'EUR': '€',
    'GBP': '£'
}

# Initialize session state
if 'amount' not in st.session_state:
    st.session_state.amount = 100.0
if 'from_currency' not in st.session_state:
    st.session_state.from_currency = 'USD'
if 'to_currency' not in st.session_state:
    st.session_state.to_currency = 'INR'

# Function to convert currency
def convert_currency(amount, from_curr, to_curr):
    if amount <= 0:
        return 0
    rate = EXCHANGE_RATES[from_curr][to_curr]
    return amount * rate

# Main app layout
st.markdown('<h1 class="title">💰 Currency Converter</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Convert between INR, USD, EUR, and GBP instantly</p>', unsafe_allow_html=True)

# Create columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("### From")
    from_currency = st.selectbox(
        "Select source currency",
        options=['INR', 'USD', 'EUR', 'GBP'],
        index=['INR', 'USD', 'EUR', 'GBP'].index(st.session_state.from_currency),
        key='from_curr_select',
        label_visibility="collapsed"
    )
    
with col2:
    st.markdown("### To")
    to_currency = st.selectbox(
        "Select target currency",
        options=['INR', 'USD', 'EUR', 'GBP'],
        index=['INR', 'USD', 'EUR', 'GBP'].index(st.session_state.to_currency),
        key='to_curr_select',
        label_visibility="collapsed"
    )

# Swap button
col_swap1, col_swap2, col_swap3 = st.columns([1, 1, 1])
with col_swap2:
    if st.button("🔄 Swap", use_container_width=True):
        st.session_state.from_currency, st.session_state.to_currency = to_currency, from_currency
        st.rerun()

st.markdown("---")

# Amount input
amount = st.number_input(
    f"Enter amount in {from_currency}",
    min_value=0.01,
    value=st.session_state.amount,
    step=1.0,
    format="%.2f",
    key='amount_input'
)

# Update session state
st.session_state.amount = amount
st.session_state.from_currency = from_currency
st.session_state.to_currency = to_currency

# Perform conversion
if amount > 0:
    converted_amount = convert_currency(amount, from_currency, to_currency)
    exchange_rate = EXCHANGE_RATES[from_currency][to_currency]
    
    # Display result
    st.markdown(f"""
        <div class="result-box">
            <div class="result-label">Converted Amount</div>
            <div class="result-amount">{CURRENCY_SYMBOLS[to_currency]} {converted_amount:,.2f}</div>
            <div class="result-label">{to_currency}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Display exchange rate info
    st.markdown(f"""
        <div class="rate-info">
            <strong>Exchange Rate:</strong> 1 {from_currency} = {exchange_rate:.4f} {to_currency}
        </div>
    """, unsafe_allow_html=True)
    
    # Success message
    st.success(f"✅ Successfully converted {CURRENCY_SYMBOLS[from_currency]}{amount:,.2f} {from_currency} to {CURRENCY_SYMBOLS[to_currency]}{converted_amount:,.2f} {to_currency}")
    
    # Additional conversion details
    with st.expander("📊 View Detailed Breakdown"):
        st.markdown(f"<p style='color: #FFB6C1;'><strong style='color: #FFD700;'>Original Amount:</strong> {CURRENCY_SYMBOLS[from_currency]}{amount:,.2f} {from_currency}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #FFB6C1;'><strong style='color: #FFD700;'>Exchange Rate:</strong> {exchange_rate:.6f}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #FFB6C1;'><strong style='color: #FFD700;'>Converted Amount:</strong> {CURRENCY_SYMBOLS[to_currency]}{converted_amount:,.2f} {to_currency}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #FFB6C1;'><strong style='color: #FFD700;'>Conversion Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>", unsafe_allow_html=True)
        
        # Show reverse conversion
        reverse_rate = EXCHANGE_RATES[to_currency][from_currency]
        st.markdown(f"<p style='color: #FFB6C1;'><strong style='color: #FFD700;'>Reverse Rate:</strong> 1 {to_currency} = {reverse_rate:.4f} {from_currency}</p>", unsafe_allow_html=True)

else:
    st.info("👆 Please enter an amount greater than 0 to convert")

# Footer
st.markdown("---")
st.markdown("""
    <div class="footer">
        <p>💡 <strong>Note:</strong> Exchange rates are static and for demonstration purposes only.</p>
        <p>For real-time rates, integrate with a live currency API.</p>
        <p style="margin-top: 1rem;">Made with ❤️ using Streamlit | Day 8 Challenge</p>
    </div>
""", unsafe_allow_html=True)

# Quick conversion reference table
with st.expander("📈 Quick Reference - All Exchange Rates"):
    st.markdown("<h3 style='color: #FFD700;'>Current Exchange Rates</h3>", unsafe_allow_html=True)
    
    for from_curr in ['INR', 'USD', 'EUR', 'GBP']:
        st.markdown(f"<p style='color: #FFD700; font-weight: 600;'>1 {from_curr} equals:</p>", unsafe_allow_html=True)
        cols = st.columns(4)
        for idx, to_curr in enumerate(['INR', 'USD', 'EUR', 'GBP']):
            with cols[idx]:
                rate = EXCHANGE_RATES[from_curr][to_curr]
                st.metric(
                    label=to_curr,
                    value=f"{CURRENCY_SYMBOLS[to_curr]}{rate:.4f}"
                )
        st.markdown("---")