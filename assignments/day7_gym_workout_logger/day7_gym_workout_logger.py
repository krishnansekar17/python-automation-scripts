import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os

# Page config
st.set_page_config(
    page_title="💪 Gym Workout Logger",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with proper contrast and visibility
st.markdown("""
<style>
    /* Main background - Fitness theme with orange/red gradient */
    .main {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 50%, #c44569 100%);
        padding: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 50%, #c44569 100%);
    }
    
    /* Block container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* White card containers with proper rendering */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] > div[data-testid="stVerticalBlock"] {
        background: white !important;
        border-radius: 20px !important;
        padding: 30px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3) !important;
        margin: 15px 0 !important;
    }
    
    /* Headers */
    h1 {
        color: white !important;
        text-shadow: 4px 4px 8px rgba(0, 0, 0, 0.6) !important;
        font-size: 4rem !important;
        font-weight: 900 !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: 2px !important;
    }
    
    h2 {
        color: white !important;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.5) !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        color: #2d3436 !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        margin-bottom: 1.5rem !important;
        border-bottom: 3px solid #ff6b6b !important;
        padding-bottom: 10px !important;
    }
    
    /* Subtitle */
    .subtitle {
        color: white !important;
        font-size: 1.4rem !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 2rem !important;
        font-weight: 600 !important;
    }
    
    /* Input labels - HIGH CONTRAST */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stDateInput"] label,
    div[data-testid="stTextInput"] label {
        color: #2d3436 !important;
        font-weight: 700 !important;
        font-size: 17px !important;
    }
    
    /* Input fields */
    div[data-testid="stSelectbox"] > div,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input,
    div[data-testid="stTextInput"] input {
        background: #f8f9fa !important;
        border: 2px solid #ff6b6b !important;
        border-radius: 12px !important;
        color: #2d3436 !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    /* Select box specific */
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background: #f8f9fa !important;
        border: 2px solid #ff6b6b !important;
        border-radius: 12px !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #ff6b6b 0%, #c44569 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 18px 45px !important;
        font-weight: 800 !important;
        font-size: 19px !important;
        box-shadow: 0 8px 25px rgba(196, 69, 105, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 35px rgba(196, 69, 105, 0.6) !important;
        background: linear-gradient(135deg, #c44569 0%, #ff6b6b 100%) !important;
    }
    
    /* Metric styling - HIGH CONTRAST */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #ff6b6b 0%, #c44569 100%) !important;
        padding: 25px !important;
        border-radius: 18px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
        border: 3px solid white !important;
    }
    
    div[data-testid="stMetric"] label {
        color: white !important;
        font-size: 19px !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3) !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 36px !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3) !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #ffeaa7 !important;
        font-size: 18px !important;
        font-weight: 700 !important;
    }
    
    /* Success message */
    .stSuccess {
        background-color: #d4edda !important;
        border: 3px solid #28a745 !important;
        color: #155724 !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 18px !important;
        font-size: 16px !important;
    }
    
    /* Info box */
    .info-box {
        background: rgba(255, 255, 255, 0.98) !important;
        border-left: 8px solid #ff6b6b !important;
        padding: 25px !important;
        border-radius: 15px !important;
        color: #2d3436 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        margin: 20px 0 !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Achievement badge */
    .achievement-badge {
        background: linear-gradient(135deg, #ffd700, #ffed4e);
        border-radius: 50%;
        width: 120px;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 60px;
        margin: 20px auto;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.7);
        border: 6px solid white;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .achievement-text {
        color: #2d3436 !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        text-align: center !important;
    }
    
    /* Table styling */
    .dataframe {
        border: 2px solid #ff6b6b !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #ff6b6b 0%, #c44569 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        padding: 15px !important;
        text-align: center !important;
    }
    
    .dataframe td {
        color: #2d3436 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        padding: 12px !important;
        text-align: center !important;
        border-bottom: 1px solid #dfe6e9 !important;
    }
    
    /* Footer text */
    .footer-text {
        color: white !important;
        font-size: 1.3rem !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5) !important;
        opacity: 0.95 !important;
        font-weight: 600 !important;
    }
    
    /* Plotly chart containers */
    .js-plotly-plot {
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Column alignment */
    div[data-testid="column"] {
        padding: 10px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #ff6b6b 0%, #c44569 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white !important;
        color: #2d3436 !important;
        font-weight: 700 !important;
        border-radius: 10px 10px 0 0 !important;
        padding: 15px 30px !important;
        font-size: 16px !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff6b6b 0%, #c44569 100%) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Data persistence
DATA_FILE = "gym_workout_data.json"

# Exercise categories and common exercises
EXERCISE_CATEGORIES = {
    "Chest": ["Bench Press", "Incline Press", "Dumbbell Flyes", "Push-ups", "Cable Crossover"],
    "Back": ["Deadlift", "Pull-ups", "Barbell Row", "Lat Pulldown", "T-Bar Row"],
    "Legs": ["Squat", "Leg Press", "Lunges", "Leg Curl", "Calf Raises"],
    "Shoulders": ["Overhead Press", "Lateral Raises", "Front Raises", "Shrugs", "Arnold Press"],
    "Arms": ["Bicep Curl", "Tricep Extension", "Hammer Curl", "Skull Crushers", "Preacher Curl"],
    "Core": ["Plank", "Crunches", "Russian Twist", "Leg Raises", "Cable Crunch"]
}

def load_data():
    """Load workout data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    """Save workout data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_workout(date_str, exercise, category, sets, reps, weight):
    """Add a workout entry"""
    data = load_data()
    
    workout_entry = {
        "date": date_str,
        "exercise": exercise,
        "category": category,
        "sets": sets,
        "reps": reps,
        "weight": weight,
        "total_volume": sets * reps * weight,
        "timestamp": datetime.now().isoformat()
    }
    
    data.append(workout_entry)
    save_data(data)
    return workout_entry

def get_weekly_data():
    """Get last 7 days of workout data"""
    data = load_data()
    
    # Filter for last 7 days
    seven_days_ago = datetime.now() - timedelta(days=6)
    
    weekly_data = []
    for entry in data:
        entry_date = datetime.fromisoformat(entry['timestamp'])
        if entry_date >= seven_days_ago:
            weekly_data.append(entry)
    
    return weekly_data

def get_today_workouts():
    """Get today's workouts"""
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    
    return [entry for entry in data if entry['date'] == today]

def create_weekly_volume_chart(weekly_data):
    """Create weekly total volume chart"""
    if not weekly_data:
        # Empty state
        fig = go.Figure()
        fig.add_annotation(
            text="No workout data yet. Start logging!",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20, color="#636e72")
        )
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400
        )
        return fig
    
    # Group by date
    df = pd.DataFrame(weekly_data)
    daily_volume = df.groupby('date')['total_volume'].sum().reset_index()
    daily_volume['date'] = pd.to_datetime(daily_volume['date'])
    daily_volume = daily_volume.sort_values('date')
    
    # Create bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=daily_volume['date'],
        y=daily_volume['total_volume'],
        text=daily_volume['total_volume'],
        textposition='outside',
        texttemplate='<b>%{text:,.0f} kg</b>',
        textfont=dict(size=14, color='#2d3436', family='Arial Black'),
        marker=dict(
            color=daily_volume['total_volume'],
            colorscale='Reds',
            line=dict(color='#2d3436', width=2),
            showscale=False
        ),
        hovertemplate='<b>%{x|%b %d}</b><br>Total Volume: <b>%{y:,.0f} kg</b><extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "<b>Weekly Training Volume</b>",
            'font': {'size': 26, 'color': '#2d3436', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis={
            'title': {'text': "<b>Date</b>", 'font': {'size': 18, 'color': '#2d3436', 'family': 'Arial Black'}},
            'tickfont': {'size': 14, 'color': '#2d3436', 'family': 'Arial'},
            'tickformat': '%b %d'
        },
        yaxis={
            'title': {'text': "<b>Total Volume (kg)</b>", 'font': {'size': 18, 'color': '#2d3436', 'family': 'Arial Black'}},
            'tickfont': {'size': 14, 'color': '#2d3436', 'family': 'Arial'}
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        height=450,
        hovermode='x unified',
        margin=dict(l=70, r=40, t=80, b=70)
    )
    
    return fig

def create_exercise_progress_chart(weekly_data, exercise_name):
    """Create progress chart for specific exercise"""
    if not weekly_data:
        fig = go.Figure()
        fig.add_annotation(
            text="No data for this exercise",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color="#636e72")
        )
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350
        )
        return fig
    
    df = pd.DataFrame(weekly_data)
    exercise_data = df[df['exercise'] == exercise_name].copy()
    
    if exercise_data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text=f"No data for {exercise_name}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color="#636e72")
        )
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350
        )
        return fig
    
    exercise_data['date'] = pd.to_datetime(exercise_data['date'])
    exercise_data = exercise_data.sort_values('date')
    
    fig = go.Figure()
    
    # Weight progression
    fig.add_trace(go.Scatter(
        x=exercise_data['date'],
        y=exercise_data['weight'],
        mode='lines+markers',
        name='Weight',
        line=dict(color='#ff6b6b', width=4),
        marker=dict(size=12, color='#c44569', line=dict(color='white', width=2)),
        hovertemplate='<b>%{x|%b %d}</b><br>Weight: <b>%{y} kg</b><extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': f"<b>{exercise_name} - Weight Progress</b>",
            'font': {'size': 22, 'color': '#2d3436', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis={
            'title': {'text': "<b>Date</b>", 'font': {'size': 16, 'color': '#2d3436', 'family': 'Arial Black'}},
            'tickfont': {'size': 12, 'color': '#2d3436'},
            'tickformat': '%b %d'
        },
        yaxis={
            'title': {'text': "<b>Weight (kg)</b>", 'font': {'size': 16, 'color': '#2d3436', 'family': 'Arial Black'}},
            'tickfont': {'size': 12, 'color': '#2d3436'}
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        height=350,
        margin=dict(l=60, r=40, t=70, b=60)
    )
    
    return fig

def create_category_distribution(weekly_data):
    """Create pie chart for exercise category distribution"""
    if not weekly_data:
        fig = go.Figure()
        fig.add_annotation(
            text="No workout data yet",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color="#636e72")
        )
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400
        )
        return fig
    
    df = pd.DataFrame(weekly_data)
    category_counts = df['category'].value_counts()
    
    colors = ['#ff6b6b', '#ee5a6f', '#c44569', '#ffeaa7', '#fdcb6e', '#e17055']
    
    fig = go.Figure(data=[go.Pie(
        labels=category_counts.index,
        values=category_counts.values,
        hole=0.4,
        marker=dict(colors=colors, line=dict(color='white', width=3)),
        textfont=dict(size=16, color='white', family='Arial Black'),
        hovertemplate='<b>%{label}</b><br>Exercises: %{value}<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': "<b>Muscle Group Distribution</b>",
            'font': {'size': 24, 'color': '#2d3436', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        showlegend=True,
        legend=dict(
            font=dict(size=14, color='#2d3436', family='Arial'),
            orientation="v",
            x=1.1,
            y=0.5
        ),
        margin=dict(l=40, r=150, t=80, b=40)
    )
    
    return fig

def create_volume_by_category(weekly_data):
    """Create bar chart for volume by category"""
    if not weekly_data:
        fig = go.Figure()
        fig.add_annotation(
            text="No workout data yet",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color="#636e72")
        )
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400
        )
        return fig
    
    df = pd.DataFrame(weekly_data)
    category_volume = df.groupby('category')['total_volume'].sum().reset_index()
    category_volume = category_volume.sort_values('total_volume', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=category_volume['category'],
        x=category_volume['total_volume'],
        orientation='h',
        text=category_volume['total_volume'],
        textposition='outside',
        texttemplate='<b>%{text:,.0f} kg</b>',
        textfont=dict(size=14, color='#2d3436', family='Arial Black'),
        marker=dict(
            color=category_volume['total_volume'],
            colorscale='Reds',
            line=dict(color='#2d3436', width=2),
            showscale=False
        ),
        hovertemplate='<b>%{y}</b><br>Volume: <b>%{x:,.0f} kg</b><extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "<b>Volume by Muscle Group</b>",
            'font': {'size': 24, 'color': '#2d3436', 'family': 'Arial Black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis={
            'title': {'text': "<b>Total Volume (kg)</b>", 'font': {'size': 16, 'color': '#2d3436', 'family': 'Arial Black'}},
            'tickfont': {'size': 12, 'color': '#2d3436'}
        },
        yaxis={
            'title': {'text': "", 'font': {'size': 16, 'color': '#2d3436', 'family': 'Arial Black'}},
            'tickfont': {'size': 14, 'color': '#2d3436', 'family': 'Arial Black'}
        },
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        height=400,
        margin=dict(l=100, r=100, t=80, b=60)
    )
    
    return fig

def get_workout_stats(weekly_data):
    """Calculate workout statistics"""
    if not weekly_data:
        return {
            'total_workouts': 0,
            'total_volume': 0,
            'total_sets': 0,
            'total_reps': 0,
            'avg_weight': 0,
            'unique_exercises': 0
        }
    
    df = pd.DataFrame(weekly_data)
    
    return {
        'total_workouts': len(df),
        'total_volume': df['total_volume'].sum(),
        'total_sets': df['sets'].sum(),
        'total_reps': df['reps'].sum(),
        'avg_weight': df['weight'].mean(),
        'unique_exercises': df['exercise'].nunique()
    }

# Main App
def main():
    # Header
    st.markdown("<h1 style='text-align: center;'>💪 GYM WORKOUT LOGGER</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle' style='text-align: center;'>Track your exercises, monitor progress, and crush your fitness goals!</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Input Section
    st.markdown("<h2 style='text-align: center;'>📝 Log Your Workout</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_spacer1, col_input, col_spacer2 = st.columns([0.5, 4, 0.5])
    
    with col_input:
        with st.container():
            st.markdown("### 🏋️ Exercise Details")
            
            # Row 1: Category and Exercise
            input_row1_col1, input_row1_col2 = st.columns(2)
            
            with input_row1_col1:
                category = st.selectbox(
                    "Muscle Group",
                    options=list(EXERCISE_CATEGORIES.keys()),
                    help="Select the muscle group you're training"
                )
            
            with input_row1_col2:
                # Get exercises for selected category
                exercises = EXERCISE_CATEGORIES[category] + ["Custom Exercise"]
                exercise = st.selectbox(
                    "Exercise",
                    options=exercises,
                    help="Select the exercise or choose 'Custom Exercise'"
                )
            
            # Custom exercise input
            if exercise == "Custom Exercise":
                exercise = st.text_input(
                    "Enter Custom Exercise Name",
                    placeholder="e.g., Cable Flyes",
                    help="Enter your custom exercise name"
                )
            
            # Row 2: Sets, Reps, Weight
            input_row2_col1, input_row2_col2, input_row2_col3 = st.columns(3)
            
            with input_row2_col1:
                sets = st.number_input(
                    "Sets",
                    min_value=1,
                    max_value=20,
                    value=3,
                    step=1,
                    help="Number of sets performed"
                )
            
            with input_row2_col2:
                reps = st.number_input(
                    "Reps",
                    min_value=1,
                    max_value=100,
                    value=10,
                    step=1,
                    help="Number of repetitions per set"
                )
            
            with input_row2_col3:
                weight = st.number_input(
                    "Weight (kg)",
                    min_value=0.0,
                    max_value=500.0,
                    value=20.0,
                    step=2.5,
                    help="Weight used for the exercise"
                )
            
            # Row 3: Date
            selected_date = st.date_input(
                "Workout Date",
                value=datetime.now(),
                max_value=datetime.now(),
                help="Select the date of your workout"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Calculate and display volume
            total_volume = sets * reps * weight
            st.markdown(f"<div class='info-box'>💪 <b>Total Volume:</b> {total_volume:,.1f} kg ({sets} sets × {reps} reps × {weight} kg)</div>", unsafe_allow_html=True)
            
            # Add button
            if st.button("🔥 LOG WORKOUT"):
                if exercise and exercise != "Custom Exercise":
                    date_str = selected_date.strftime("%Y-%m-%d")
                    workout = add_workout(date_str, exercise, category, sets, reps, weight)
                    st.success(f"✅ Logged: {exercise} - {sets}×{reps} @ {weight}kg on {selected_date.strftime('%B %d, %Y')}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("⚠️ Please enter a valid exercise name!")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Get data
    weekly_data = get_weekly_data()
    today_workouts = get_today_workouts()
    stats = get_workout_stats(weekly_data)
    
    # Today's Summary
    if today_workouts:
        st.markdown("<h2 style='text-align: center;'>🔥 Today's Training Session</h2>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        today_col1, today_col2, today_col3, today_col4 = st.columns(4)
        
        today_df = pd.DataFrame(today_workouts)
        today_exercises = len(today_df)
        today_volume = today_df['total_volume'].sum()
        today_sets = today_df['sets'].sum()
        today_reps = today_df['reps'].sum()
        
        with today_col1:
            st.metric("Exercises", f"{today_exercises}")
        
        with today_col2:
            st.metric("Total Volume", f"{today_volume:,.0f} kg")
        
        with today_col3:
            st.metric("Total Sets", f"{today_sets}")
        
        with today_col4:
            st.metric("Total Reps", f"{today_reps}")
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Weekly Statistics
    st.markdown("<h2 style='text-align: center;'>📊 Weekly Statistics (Last 7 Days)</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    stats_col1, stats_col2, stats_col3, stats_col4, stats_col5, stats_col6 = st.columns(6)
    
    with stats_col1:
        st.metric("Total Workouts", f"{stats['total_workouts']}")
    
    with stats_col2:
        st.metric("Total Volume", f"{stats['total_volume']:,.0f} kg")
    
    with stats_col3:
        st.metric("Total Sets", f"{stats['total_sets']}")
    
    with stats_col4:
        st.metric("Total Reps", f"{stats['total_reps']}")
    
    with stats_col5:
        st.metric("Avg Weight", f"{stats['avg_weight']:.1f} kg")
    
    with stats_col6:
        st.metric("Unique Exercises", f"{stats['unique_exercises']}")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Progress Charts
    st.markdown("<h2 style='text-align: center;'>📈 Progress Tracking</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Weekly volume chart
    chart_col1, chart_col2 = st.columns([2, 1])
    
    with chart_col1:
        with st.container():
            fig_volume = create_weekly_volume_chart(weekly_data)
            st.plotly_chart(fig_volume, use_container_width=True)
    
    with chart_col2:
        with st.container():
            fig_category = create_category_distribution(weekly_data)
            st.plotly_chart(fig_category, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Volume by category and exercise progress
    chart2_col1, chart2_col2 = st.columns(2)
    
    with chart2_col1:
        with st.container():
            fig_cat_volume = create_volume_by_category(weekly_data)
            st.plotly_chart(fig_cat_volume, use_container_width=True)
    
    with chart2_col2:
        with st.container():
            st.markdown("### 🎯 Exercise Progress Tracker")
            
            if weekly_data:
                df = pd.DataFrame(weekly_data)
                unique_exercises = sorted(df['exercise'].unique())
                
                selected_exercise = st.selectbox(
                    "Select Exercise to Track",
                    options=unique_exercises,
                    help="View your progress for a specific exercise"
                )
                
                fig_progress = create_exercise_progress_chart(weekly_data, selected_exercise)
                st.plotly_chart(fig_progress, use_container_width=True)
            else:
                st.info("📝 No exercises logged yet. Start tracking to see progress!")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Workout History Table
    st.markdown("<h2 style='text-align: center;'>📋 Workout History (Last 7 Days)</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if weekly_data:
        df_display = pd.DataFrame(weekly_data)
        df_display = df_display[['date', 'category', 'exercise', 'sets', 'reps', 'weight', 'total_volume']]
        df_display.columns = ['Date', 'Muscle Group', 'Exercise', 'Sets', 'Reps', 'Weight (kg)', 'Volume (kg)']
        df_display = df_display.sort_values('Date', ascending=False)
        df_display['Volume (kg)'] = df_display['Volume (kg)'].apply(lambda x: f"{x:,.1f}")
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Download button
        col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
        
        with col_dl2:
            csv = df_display.to_csv(index=False)
            st.download_button(
                label="📥 DOWNLOAD WORKOUT DATA (CSV)",
                data=csv,
                file_name=f"gym_workout_log_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("📝 No workout data yet. Start logging your exercises above!")
    
    # Achievement section
    if stats['total_workouts'] >= 5:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='achievement-badge'>🏆</div>", unsafe_allow_html=True)
        st.markdown("<p class='achievement-text'>Consistency Champion! 5+ Workouts This Week!</p>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p class='footer-text' style='text-align: center;'>💪 Train Hard, Track Smart, Achieve Greatness! 🏋️‍♂️</p>", unsafe_allow_html=True)
    st.markdown("<p class='footer-text' style='text-align: center;'>Remember: Progressive overload is the key to muscle growth!</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()