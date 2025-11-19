import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os

# Page config
st.set_page_config(
    page_title="💧 Hydration Hub",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with fixed visibility and alignment
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Fix for Streamlit containers */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* White card containers - FIXED */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        margin: 15px 0;
    }
    
    /* Input section styling */
    div[data-testid="stNumberInput"] label,
    div[data-testid="stDateInput"] label {
        color: #333333 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input {
        background: #f8f9fa !important;
        border: 2px solid #667eea !important;
        border-radius: 10px !important;
        color: #333333 !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    
    /* Headers with better contrast */
    h1 {
        color: white !important;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.5) !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    h3 {
        color: #333333 !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    
    /* Subtitle text */
    .subtitle {
        color: white !important;
        font-size: 1.3rem !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4) !important;
        margin-bottom: 2rem !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 15px 40px !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Metric styling - HIGH CONTRAST */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    div[data-testid="stMetric"] label {
        color: white !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 32px !important;
        font-weight: 800 !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #ffd700 !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    /* Success message */
    .stSuccess {
        background-color: #d4edda !important;
        border: 2px solid #28a745 !important;
        color: #155724 !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    
    /* Reminder box */
    .reminder-box {
        background: rgba(255, 255, 255, 0.95) !important;
        border-left: 8px solid #ffd700 !important;
        padding: 20px !important;
        border-radius: 15px !important;
        color: #333333 !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        margin: 20px 0 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Achievement badge */
    .achievement-badge {
        background: linear-gradient(135deg, #ffd700, #ffed4e);
        border-radius: 50%;
        width: 100px;
        height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 50px;
        margin: 20px auto;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6);
        border: 5px solid white;
    }
    
    .achievement-text {
        color: #333333 !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        text-align: center !important;
    }
    
    /* Download button container */
    .download-container {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        text-align: center;
    }
    
    /* Footer text */
    .footer-text {
        color: white !important;
        font-size: 1.2rem !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4) !important;
        opacity: 0.95 !important;
    }
    
    /* Plotly chart containers */
    .js-plotly-plot {
        border-radius: 15px;
        overflow: hidden;
    }
    
    /* Column alignment fix */
    div[data-testid="column"] {
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Data persistence
DATA_FILE = "hydration_data.json"

def load_data():
    """Load hydration data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    """Save hydration data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def add_intake(date_str, amount):
    """Add water intake for a specific date"""
    data = load_data()
    if date_str not in data:
        data[date_str] = 0
    data[date_str] += amount
    save_data(data)
    return data[date_str]

def get_today_intake():
    """Get today's total intake"""
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    return data.get(today, 0)

def get_weekly_data():
    """Get last 7 days of data"""
    data = load_data()
    weekly_data = []
    
    for i in range(6, -1, -1):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        day_name = date.strftime("%a")
        intake = data.get(date_str, 0)
        weekly_data.append({
            'date': date_str,
            'day': day_name,
            'intake': intake,
            'date_obj': date
        })
    
    return weekly_data

def create_radial_gauge(current, goal=3000):
    """Create a radial gauge chart for daily progress"""
    percentage = min((current / goal) * 100, 100)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': "<b>Today's Hydration</b>", 
            'font': {'size': 28, 'color': '#333333', 'family': 'Arial Black'}
        },
        delta={'reference': goal, 'suffix': ' ml', 'font': {'size': 20, 'color': '#333333'}},
        number={'suffix': ' ml', 'font': {'size': 48, 'color': '#667eea', 'family': 'Arial Black'}},
        gauge={
            'axis': {
                'range': [None, goal], 
                'tickwidth': 2, 
                'tickcolor': "#333333",
                'tickfont': {'size': 14, 'color': '#333333'}
            },
            'bar': {'color': "#667eea", 'thickness': 0.8},
            'bgcolor': "#f0f0f0",
            'borderwidth': 3,
            'bordercolor': "#667eea",
            'steps': [
                {'range': [0, goal * 0.33], 'color': '#ffcdd2'},
                {'range': [goal * 0.33, goal * 0.66], 'color': '#fff9c4'},
                {'range': [goal * 0.66, goal], 'color': '#c8e6c9'}
            ],
            'threshold': {
                'line': {'color': "#e74c3c", 'width': 5},
                'thickness': 0.8,
                'value': goal
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'color': "#333333", 'family': "Arial"},
        height=400,
        margin=dict(l=20, r=20, t=80, b=20)
    )
    
    return fig

def create_weekly_chart(weekly_data):
    """Create an interactive weekly chart - FIXED"""
    df = pd.DataFrame(weekly_data)
    
    # Color based on goal achievement
    colors = ['#e74c3c' if x < 3000 else '#27ae60' for x in df['intake']]
    
    fig = go.Figure()
    
    # Add bar chart
    fig.add_trace(go.Bar(
        x=df['day'],
        y=df['intake'],
        text=df['intake'],
        textposition='outside',
        texttemplate='<b>%{text} ml</b>',
        textfont=dict(size=16, color='#333333', family='Arial Black'),
        marker=dict(
            color=colors,
            line=dict(color='#333333', width=2)
        ),
        hovertemplate='<b>%{x}</b><br>Intake: <b>%{y} ml</b><extra></extra>'
    ))
    
    # Add goal line
    fig.add_hline(
        y=3000, 
        line_dash="dash", 
        line_color="#e74c3c", 
        line_width=3,
        annotation_text="<b>Daily Goal (3000 ml)</b>", 
        annotation_position="right",
        annotation_font=dict(size=14, color='#e74c3c', family='Arial Black')
    )
    
    # FIXED: Use title_font instead of titlefont
    fig.update_layout(
        title={
            'text': "<b>Weekly Hydration Summary</b>",
            'font': {'size': 24, 'color': '#333333', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis={
            'title': {'text': "<b>Day</b>", 'font': {'size': 18, 'color': '#333333', 'family': 'Arial Black'}},
            'tickfont': {'size': 14, 'color': '#333333', 'family': 'Arial Black'}
        },
        yaxis={
            'title': {'text': "<b>Water Intake (ml)</b>", 'font': {'size': 18, 'color': '#333333', 'family': 'Arial Black'}},
            'tickfont': {'size': 14, 'color': '#333333', 'family': 'Arial Black'}
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        height=450,
        hovermode='x unified',
        margin=dict(l=60, r=40, t=80, b=60)
    )
    
    return fig

def create_bubble_chart(weekly_data):
    """Create a bubble chart showing daily intake - FIXED"""
    df = pd.DataFrame(weekly_data)
    df['size'] = df['intake'].apply(lambda x: max(x / 20, 10))  # Minimum size for visibility
    
    fig = px.scatter(
        df, 
        x='day', 
        y=[1]*len(df), 
        size='size', 
        color='intake',
        hover_data={'intake': True, 'size': False},
        color_continuous_scale='Blues',
        size_max=70
    )
    
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Intake: <b>%{customdata[0]} ml</b><extra></extra>'
    )
    
    # FIXED: Use title_font instead of titlefont
    fig.update_layout(
        title={
            'text': "<b>Daily Hydration Bubbles</b>",
            'font': {'size': 20, 'color': '#333333', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        showlegend=False,
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        xaxis={
            'title': {'text': "<b>Day of Week</b>", 'font': {'size': 16, 'color': '#333333', 'family': 'Arial Black'}},
            'tickfont': {'size': 14, 'color': '#333333', 'family': 'Arial Black'}
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=280,
        margin=dict(l=40, r=40, t=60, b=50)
    )
    
    return fig

def get_hydration_message(current, goal=3000):
    """Get encouraging message based on progress"""
    percentage = (current / goal) * 100
    
    if percentage == 0:
        return "🌟 Start your hydration journey! Every drop counts!"
    elif percentage < 25:
        return "💧 Great start! Keep sipping throughout the day!"
    elif percentage < 50:
        return "🌊 You're making waves! Halfway to your goal!"
    elif percentage < 75:
        return "🚀 Fantastic progress! You're on fire (but stay hydrated)!"
    elif percentage < 100:
        return "⭐ Almost there! Just a few more glasses to go!"
    else:
        return "🏆 GOAL ACHIEVED! You're a hydration champion!"

# Main App
def main():
    # Header with proper spacing
    st.markdown("<h1 style='text-align: center;'>💧 Hydration Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle' style='text-align: center;'>Track your daily water intake and stay healthy!</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Input Section - Centered with white background
    col_spacer1, col_input, col_spacer2 = st.columns([1, 3, 1])
    
    with col_input:
        with st.container():
            st.markdown("### 📝 Log Your Intake")
            
            input_col1, input_col2 = st.columns(2)
            
            with input_col1:
                amount = st.number_input(
                    "Amount (ml)",
                    min_value=50,
                    max_value=2000,
                    value=250,
                    step=50,
                    help="Enter the amount of water you drank"
                )
            
            with input_col2:
                selected_date = st.date_input(
                    "Date",
                    value=datetime.now(),
                    max_value=datetime.now(),
                    help="Select the date for this entry"
                )
            
            if st.button("💧 Add Intake"):
                date_str = selected_date.strftime("%Y-%m-%d")
                new_total = add_intake(date_str, amount)
                st.success(f"✅ Added {amount} ml for {selected_date.strftime('%B %d, %Y')}")
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Get today's data
    today_intake = get_today_intake()
    goal = 3000
    percentage = min((today_intake / goal) * 100, 100)
    
    # Hydration message with high contrast
    message = get_hydration_message(today_intake, goal)
    st.markdown(f"<div class='reminder-box'>{message}</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Progress visualization - Two columns
    prog_col1, prog_col2 = st.columns([2, 1])
    
    with prog_col1:
        with st.container():
            fig = create_radial_gauge(today_intake, goal)
            st.plotly_chart(fig, use_container_width=True)
    
    with prog_col2:
        with st.container():
            st.markdown("### 📊 Quick Stats")
            st.metric("Current", f"{today_intake} ml", f"{today_intake - goal} ml")
            st.metric("Goal", f"{goal} ml")
            st.metric("Progress", f"{percentage:.1f}%")
            
            if percentage >= 100:
                st.markdown("<div class='achievement-badge'>🏆</div>", unsafe_allow_html=True)
                st.markdown("<p class='achievement-text'>Goal Achieved!</p>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Weekly Summary Section
    st.markdown("<h2 style='text-align: center;'>📅 Weekly Hydration Summary</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    weekly_data = get_weekly_data()
    
    week_col1, week_col2 = st.columns(2)
    
    with week_col1:
        with st.container():
            fig = create_weekly_chart(weekly_data)
            st.plotly_chart(fig, use_container_width=True)
    
    with week_col2:
        with st.container():
            # Weekly statistics
            total_week = sum([day['intake'] for day in weekly_data])
            avg_week = total_week / 7
            days_met_goal = sum([1 for day in weekly_data if day['intake'] >= 3000])
            
            st.markdown("### 📈 Weekly Statistics")
            st.metric("Total (7 days)", f"{total_week} ml")
            st.metric("Daily Average", f"{avg_week:.0f} ml")
            st.metric("Days Goal Met", f"{days_met_goal}/7")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Bubble visualization
            fig_bubble = create_bubble_chart(weekly_data)
            st.plotly_chart(fig_bubble, use_container_width=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Download Section - Centered
    col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
    
    with col_dl2:
        with st.container():
            st.markdown("### 📥 Export Data")
            
            # Create CSV
            df_export = pd.DataFrame(weekly_data)
            df_export = df_export[['date', 'day', 'intake']]
            df_export.columns = ['Date', 'Day', 'Intake (ml)']
            
            csv = df_export.to_csv(index=False)
            
            st.download_button(
                label="📊 Download Week CSV",
                data=csv,
                file_name=f"hydration_week_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p class='footer-text' style='text-align: center;'>💧 Stay hydrated, stay healthy! Drink water regularly throughout the day. 💧</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()