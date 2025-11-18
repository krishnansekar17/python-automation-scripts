import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Unit Converter - Day 5 Challenge",
    page_icon="🔄",
    layout="centered"
)

# Title and description
st.title("🔄 Unit Converter")
st.markdown("**Day 5 - Python Challenge**")
st.markdown("Convert between different units in real-time!")

# Sidebar for conversion type selection
st.sidebar.header("Select Conversion Type")
conversion_type = st.sidebar.radio(
    "Choose a category:",
    ["💱 Currency (INR ↔ USD)", 
     "🌡️ Temperature (°C ↔ °F)", 
     "📏 Length (cm ↔ inch)", 
     "⚖️ Weight (kg ↔ lb)"]
)

# Add a divider
st.divider()

# Currency Conversion
if conversion_type == "💱 Currency (INR ↔ USD)":
    st.subheader("💱 Currency Converter")
    st.info("Using exchange rate: 1 USD = 83.50 INR (Fixed rate for demo)")
    
    # Exchange rate (you can update this or use an API for live rates)
    USD_TO_INR = 83.50
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**INR to USD**")
        inr_amount = st.number_input("Enter amount in INR:", min_value=0.0, value=100.0, step=10.0, key="inr")
        # Convert INR to USD
        usd_result = inr_amount / USD_TO_INR
        st.success(f"**Result:** ₹{inr_amount:,.2f} = ${usd_result:,.2f}")
    
    with col2:
        st.markdown("**USD to INR**")
        usd_amount = st.number_input("Enter amount in USD:", min_value=0.0, value=100.0, step=10.0, key="usd")
        # Convert USD to INR
        inr_result = usd_amount * USD_TO_INR
        st.success(f"**Result:** ${usd_amount:,.2f} = ₹{inr_result:,.2f}")

# Temperature Conversion
elif conversion_type == "🌡️ Temperature (°C ↔ °F)":
    st.subheader("🌡️ Temperature Converter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Celsius to Fahrenheit**")
        celsius = st.number_input("Enter temperature in °C:", value=25.0, step=1.0, key="celsius")
        # Formula: °F = (°C × 9/5) + 32
        fahrenheit_result = (celsius * 9/5) + 32
        st.success(f"**Result:** {celsius}°C = {fahrenheit_result:.2f}°F")
    
    with col2:
        st.markdown("**Fahrenheit to Celsius**")
        fahrenheit = st.number_input("Enter temperature in °F:", value=77.0, step=1.0, key="fahrenheit")
        # Formula: °C = (°F - 32) × 5/9
        celsius_result = (fahrenheit - 32) * 5/9
        st.success(f"**Result:** {fahrenheit}°F = {celsius_result:.2f}°C")

# Length Conversion
elif conversion_type == "📏 Length (cm ↔ inch)":
    st.subheader("📏 Length Converter")
    st.info("Conversion factor: 1 inch = 2.54 cm")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Centimeters to Inches**")
        cm = st.number_input("Enter length in cm:", min_value=0.0, value=10.0, step=1.0, key="cm")
        # Formula: inches = cm / 2.54
        inches_result = cm / 2.54
        st.success(f"**Result:** {cm} cm = {inches_result:.2f} inches")
    
    with col2:
        st.markdown("**Inches to Centimeters**")
        inches = st.number_input("Enter length in inches:", min_value=0.0, value=10.0, step=1.0, key="inches")
        # Formula: cm = inches × 2.54
        cm_result = inches * 2.54
        st.success(f"**Result:** {inches} inches = {cm_result:.2f} cm")

# Weight Conversion
elif conversion_type == "⚖️ Weight (kg ↔ lb)":
    st.subheader("⚖️ Weight Converter")
    st.info("Conversion factor: 1 kg = 2.20462 lb")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Kilograms to Pounds**")
        kg = st.number_input("Enter weight in kg:", min_value=0.0, value=10.0, step=1.0, key="kg")
        # Formula: lb = kg × 2.20462
        lb_result = kg * 2.20462
        st.success(f"**Result:** {kg} kg = {lb_result:.2f} lb")
    
    with col2:
        st.markdown("**Pounds to Kilograms**")
        lb = st.number_input("Enter weight in lb:", min_value=0.0, value=22.05, step=1.0, key="lb")
        # Formula: kg = lb / 2.20462
        kg_result = lb / 2.20462
        st.success(f"**Result:** {lb} lb = {kg_result:.2f} kg")

# Footer
st.divider()
st.markdown("---")
st.markdown("""
### 📝 Conversion Formulas Used:
- **Currency:** 1 USD = 83.50 INR (fixed rate)
- **Temperature:** °F = (°C × 9/5) + 32 | °C = (°F - 32) × 5/9
- **Length:** 1 inch = 2.54 cm
- **Weight:** 1 kg = 2.20462 lb

*Built for Day 5 of Python Challenge 🚀*
""")