import streamlit as st

# Page configuration
st.set_page_config(page_title='BMI Calculator', page_icon='⚖️', layout='centered')

# Custom CSS for styling
st.markdown("""
    <style>
    /* Main app background */
    .main {
        background-color: #f3f4f6;
    }
    
    /* Center align all text */
    h1 {
        color: #1e3a8a !important;
        text-align: center !important;
        font-weight: 700 !important;
    }
    
    h2, h3 {
        color: #3b82f6 !important;
        text-align: center !important;
        font-weight: 600 !important;
    }
    
    p {
        color: #4b5563 !important;
        text-align: center !important;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        color: #1e40af !important;
        font-size: 3rem !important;
        font-weight: 700 !important;
        text-align: center !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
        text-align: center !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        font-size: 1.1rem !important;
    }
    
    /* Table center alignment */
    table {
        margin: 0 auto !important;
    }
    
    th, td {
        text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header section with colored background
st.markdown("""
    <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                padding: 2.5rem; 
                border-radius: 15px; 
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 2rem;'>
        <h1 style='color: #1e3a8a; text-align: center; margin: 0;'>🏋️ BMI Calculator</h1>
        <h3 style='color: #3b82f6; text-align: center; margin: 1rem 0 0.5rem 0;'>15 Days Python Challenge — Day 4</h3>
        <p style='color: #6b7280; text-align: center; margin: 0.5rem 0 0 0;'>Enter your height and weight to calculate your Body Mass Index (BMI).</p>
    </div>
""", unsafe_allow_html=True)

# Input section
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        height_cm = st.number_input(
            'Height (cm)', 
            min_value=30.0, 
            max_value=300.0, 
            value=170.0, 
            step=0.1,
            help='Enter your height in centimeters'
        )
    
    with col2:
        weight_kg = st.number_input(
            'Weight (kg)', 
            min_value=2.0, 
            max_value=500.0, 
            value=68.0, 
            step=0.1,
            help='Enter your weight in kilograms'
        )
    
    calculate_btn = st.button('Calculate BMI', type='primary', use_container_width=True)

# Calculate and display results
if calculate_btn:
    if height_cm <= 0 or weight_kg <= 0:
        st.error('❌ Height and weight must be greater than zero!')
    else:
        # Calculate BMI
        height_m = height_cm / 100.0
        bmi = weight_kg / (height_m ** 2)
        bmi_rounded = round(bmi, 2)
        
        # Check for unusual values
        if bmi < 10 or bmi > 80:
            st.warning('⚠️ The calculated BMI seems unusual. Please verify your inputs.')
        
        # Determine category and create complete HTML
        if bmi < 18.5:
            result_html = f"""
            <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                        padding: 2.5rem; 
                        border-radius: 15px; 
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        margin-top: 2rem;'>
                <p style='color: #6b7280; font-weight: 600; font-size: 1.1rem; text-align: center; margin-bottom: 0.5rem;'>Your BMI</p>
                <h1 style='color: #1e40af; font-size: 3.5rem; font-weight: 700; text-align: center; margin: 0.5rem 0 1.5rem 0;'>{bmi_rounded}</h1>
                <div style='background: #dbeafe; padding: 1rem; border-radius: 10px; border-left: 5px solid #3b82f6; margin: 1.5rem 0;'>
                    <p style='color: #1e40af; font-weight: 600; font-size: 1.2rem; margin: 0; text-align: center;'>📊 Category: Underweight</p>
                </div>
                <p style='color: #4b5563; text-align: center; margin-top: 1rem;'>You are classified as underweight. Consider consulting a health professional for guidance on healthy weight gain.</p>
            </div>
            """
        elif 18.5 <= bmi < 25:
            result_html = f"""
            <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                        padding: 2.5rem; 
                        border-radius: 15px; 
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        margin-top: 2rem;'>
                <p style='color: #6b7280; font-weight: 600; font-size: 1.1rem; text-align: center; margin-bottom: 0.5rem;'>Your BMI</p>
                <h1 style='color: #1e40af; font-size: 3.5rem; font-weight: 700; text-align: center; margin: 0.5rem 0 1.5rem 0;'>{bmi_rounded}</h1>
                <div style='background: #d1fae5; padding: 1rem; border-radius: 10px; border-left: 5px solid #10b981; margin: 1.5rem 0;'>
                    <p style='color: #047857; font-weight: 600; font-size: 1.2rem; margin: 0; text-align: center;'>📊 Category: Normal Weight</p>
                </div>
                <p style='color: #4b5563; text-align: center; margin-top: 1rem;'>Great! Your BMI is within the normal range. Keep up your healthy lifestyle habits.</p>
            </div>
            """
        elif 25 <= bmi < 30:
            result_html = f"""
            <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                        padding: 2.5rem; 
                        border-radius: 15px; 
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        margin-top: 2rem;'>
                <p style='color: #6b7280; font-weight: 600; font-size: 1.1rem; text-align: center; margin-bottom: 0.5rem;'>Your BMI</p>
                <h1 style='color: #1e40af; font-size: 3.5rem; font-weight: 700; text-align: center; margin: 0.5rem 0 1.5rem 0;'>{bmi_rounded}</h1>
                <div style='background: #fef3c7; padding: 1rem; border-radius: 10px; border-left: 5px solid #f59e0b; margin: 1.5rem 0;'>
                    <p style='color: #d97706; font-weight: 600; font-size: 1.2rem; margin: 0; text-align: center;'>📊 Category: Overweight</p>
                </div>
                <p style='color: #4b5563; text-align: center; margin-top: 1rem;'>You are classified as overweight. Consider a balanced diet and regular physical activity.</p>
            </div>
            """
        else:
            result_html = f"""
            <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                        padding: 2.5rem; 
                        border-radius: 15px; 
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        margin-top: 2rem;'>
                <p style='color: #6b7280; font-weight: 600; font-size: 1.1rem; text-align: center; margin-bottom: 0.5rem;'>Your BMI</p>
                <h1 style='color: #1e40af; font-size: 3.5rem; font-weight: 700; text-align: center; margin: 0.5rem 0 1.5rem 0;'>{bmi_rounded}</h1>
                <div style='background: #fee2e2; padding: 1rem; border-radius: 10px; border-left: 5px solid #ef4444; margin: 1.5rem 0;'>
                    <p style='color: #dc2626; font-weight: 600; font-size: 1.2rem; margin: 0; text-align: center;'>📊 Category: Obese</p>
                </div>
                <p style='color: #4b5563; text-align: center; margin-top: 1rem;'>You are classified as obese. It is advisable to consult a healthcare provider for personalized advice.</p>
            </div>
            """
        
        # Display the complete result
        st.markdown(result_html, unsafe_allow_html=True)
        
        # BMI Reference table
        st.markdown('---')
        st.markdown('<h3 style="color: #3b82f6; text-align: center; margin-top: 2rem;">📋 BMI Reference Guide</h3>', unsafe_allow_html=True)
        
        reference_data = {
            'Category': ['Underweight', 'Normal Weight', 'Overweight', 'Obese'],
            'BMI Range': ['< 18.5', '18.5 - 24.9', '25.0 - 29.9', '≥ 30.0']
        }
        
        st.table(reference_data)

# Footer
st.markdown('---')
st.markdown('<p style="color: #9ca3af; font-size: 0.9rem; text-align: center;">💡 BMI is a screening tool and may not be accurate for athletes, elderly, or pregnant individuals.</p>', unsafe_allow_html=True)