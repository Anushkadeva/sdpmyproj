"""
🌦️ Delhi Weather Analytics Dashboard
Historical Climate Trends & Weather Insights
Stack: Dataset -> Pandas -> Streamlit -> Plotly -> Docker -> Kubernetes
"""

import os
import glob
import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# 1. STREAMLIT PAGE CONFIGURATION & MODERN STYLING
# ==============================================================================
st.set_page_config(
    page_title="🌦️ Delhi Weather Analytics Dashboard",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern, clean academic light theme
st.markdown(
    """
    <style>
        /* Main background & base typography */
        .main {
            background-color: #F8FAFC;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #0F172A;
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            font-weight: 600;
        }
        
        /* Header Hero Banner */
        .hero-banner {
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border: 1px solid #BFDBFE;
            border-radius: 14px;
            padding: 24px 28px;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .hero-title {
            font-size: 2.1rem;
            font-weight: 700;
            color: #1E3A8A;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .hero-subtitle {
            font-size: 1.05rem;
            color: #3B82F6;
            margin-top: 6px;
            font-weight: 500;
        }
        .hero-badges {
            display: flex;
            gap: 10px;
            margin-top: 14px;
            flex-wrap: wrap;
        }
        .badge {
            background-color: #FFFFFF;
            color: #1E40AF;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 9999px;
            border: 1px solid #DBEAFE;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        /* KPI Metric Cards */
        .kpi-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        .kpi-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            position: relative;
            overflow: hidden;
        }
        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        }
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
        }
        .kpi-temp::before { background: #EF4444; }
        .kpi-maxtemp::before { background: #F97316; }
        .kpi-hum::before { background: #3B82F6; }
        .kpi-wind::before { background: #10B981; }
        .kpi-press::before { background: #8B5CF6; }

        .kpi-label {
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748B;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .kpi-value {
            font-size: 1.85rem;
            font-weight: 700;
            color: #0F172A;
            line-height: 1.2;
        }
        .kpi-unit {
            font-size: 0.95rem;
            font-weight: 500;
            color: #94A3B8;
            margin-left: 4px;
        }
        .kpi-sub {
            font-size: 0.8rem;
            color: #64748B;
            margin-top: 4px;
        }

        /* Chart container */
        .chart-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }

        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #FFFFFF;
        }
        
        /* Table styling */
        .dataframe {
            border-radius: 8px !important;
            border: 1px solid #E2E8F0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# 2. DATA INSPECTION, DISCOVERY & CLEANING PIPELINE
# ==============================================================================
def find_available_datasets():
    """Discover existing CSV dataset files in the project."""
    csv_candidates = glob.glob("*.csv") + glob.glob("**/*.csv", recursive=True)
    csv_candidates = list(dict.fromkeys(csv_candidates))  # remove duplicates
    return sorted(csv_candidates)


@st.cache_data
def load_and_clean_data(selected_source="Combined (Train + Test)"):
    """
    Load, clean, and validate Delhi Climate dataset based on actual project files.
    Adapts dynamically to column names:
      - date -> date
      - meantemp -> mean temperature
      - humidity -> humidity
      - wind_speed -> wind speed
      - meanpressure -> mean pressure
    """
    train_file = "DailyDelhiClimateTrain.csv"
    test_file = "DailyDelhiClimateTest.csv"

    # Verify existing files in project
    has_train = os.path.exists(train_file)
    has_test = os.path.exists(test_file)

    if not has_train and not has_test:
        # Fallback to any discovered csv
        available = find_available_datasets()
        if not available:
            st.error("❌ No CSV dataset found in the project. Please ensure dataset is present.")
            return None, "Dataset missing"
        source_df = pd.read_csv(available[0])
        loaded_name = available[0]
    elif selected_source == "Combined (Train + Test)" and has_train and has_test:
        df_train = pd.read_csv(train_file)
        df_test = pd.read_csv(test_file)
        source_df = pd.concat([df_train, df_test], ignore_index=True)
        loaded_name = f"Combined ({train_file} + {test_file})"
    elif selected_source == "Testing Dataset (2017)" and has_test:
        source_df = pd.read_csv(test_file)
        loaded_name = test_file
    elif has_train:
        source_df = pd.read_csv(train_file)
        loaded_name = train_file
    elif has_test:
        source_df = pd.read_csv(test_file)
        loaded_name = test_file
    else:
        available = find_available_datasets()
        source_df = pd.read_csv(available[0])
        loaded_name = available[0]

    # --- Identify and Map Columns Dynamically ---
    col_mapping = {}
    normalized_cols = {col.strip().lower(): col for col in source_df.columns}

    # Date column detection
    for cand in ["date", "datetime", "timestamp", "day"]:
        if cand in normalized_cols:
            col_mapping[normalized_cols[cand]] = "date"
            break

    # Temperature column detection
    for cand in ["meantemp", "temp", "temperature", "mean_temperature", "avg_temp"]:
        if cand in normalized_cols:
            col_mapping[normalized_cols[cand]] = "meantemp"
            break

    # Humidity column detection
    for cand in ["humidity", "hum", "relative_humidity"]:
        if cand in normalized_cols:
            col_mapping[normalized_cols[cand]] = "humidity"
            break

    # Wind speed column detection
    for cand in ["wind_speed", "windspeed", "wind", "speed_wind"]:
        if cand in normalized_cols:
            col_mapping[normalized_cols[cand]] = "wind_speed"
            break

    # Pressure column detection
    for cand in ["meanpressure", "pressure", "mean_pressure", "air_pressure"]:
        if cand in normalized_cols:
            col_mapping[normalized_cols[cand]] = "meanpressure"
            break

    # Validation check
    required_standard_cols = ["date", "meantemp", "humidity", "wind_speed"]
    mapped_targets = list(col_mapping.values())
    missing_required = [req for req in required_standard_cols if req not in mapped_targets]

    if missing_required:
        st.error(
            f"❌ Dataset Validation Error: Could not identify required columns: {missing_required}. "
            f"Available columns in dataset: {list(source_df.columns)}"
        )
        return None, loaded_name

    # Rename to canonical names for standard downstream processing
    df = source_df.rename(columns=col_mapping).copy()

    # --- Data Cleaning ---
    # 1. Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    # 2. Convert numerical columns to numeric
    for col in ["meantemp", "humidity", "wind_speed", "meanpressure"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 3. Handle duplicates: drop duplicates on date column, keeping first
    df = df.drop_duplicates(subset=["date"])

    # 4. Sort chronologically by date
    df = df.sort_values("date").reset_index(drop=True)

    # 5. Extract temporal features for monthly analysis
    df["year"] = df["date"].dt.year
    df["month_num"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b")
    df["month_full"] = df["date"].dt.strftime("%B")
    df["year_month"] = df["date"].dt.strftime("%Y-%m")

    return df, loaded_name


# ==============================================================================
# 3. SIDEBAR CONTROLS & DATE FILTERING
# ==============================================================================
st.sidebar.markdown(
    """
    <div style='padding: 10px 0;'>
        <h2 style='color:#1E3A8A; margin:0;'>🌦️ Dashboard Controls</h2>
        <p style='color:#64748B; font-size:0.85rem; margin-top:2px;'>Delhi Climate Analytics</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Dataset source selector
dataset_options = ["Combined (Train + Test)", "Training Dataset (2013-2016)", "Testing Dataset (2017)"]
selected_dataset = st.sidebar.selectbox(
    "📁 Dataset Source",
    dataset_options,
    index=0,
    help="Select whether to view the combined 2013-2017 dataset or individual splits.",
)

# Load data
df_full, dataset_name = load_and_clean_data(selected_dataset)

if df_full is None or df_full.empty:
    st.stop()

# Date range boundaries
min_dataset_date = df_full["date"].min().date()
max_dataset_date = df_full["date"].max().date()

# Session state initialization for date reset
if "filter_start" not in st.session_state or "filter_end" not in st.session_state:
    st.session_state["filter_start"] = min_dataset_date
    st.session_state["filter_end"] = max_dataset_date

# Date reset button callback
def reset_dates():
    st.session_state["filter_start"] = min_dataset_date
    st.session_state["filter_end"] = max_dataset_date

st.sidebar.markdown("---")
st.sidebar.subheader("📅 Date Range Filter")

# Reset button
col_reset, col_info = st.sidebar.columns([1, 1])
if col_reset.button("🔄 Reset Filters", use_container_width=True, on_click=reset_dates):
    st.sidebar.success("Date filter reset to full range!")

# Quick presets
preset_choice = st.sidebar.selectbox(
    "⚡ Quick Presets",
    ["Select a Preset...", "Full History", "Year 2016", "Year 2015", "Year 2014", "Year 2013"],
    index=0,
)
if preset_choice == "Full History":
    st.session_state["filter_start"] = min_dataset_date
    st.session_state["filter_end"] = max_dataset_date
elif preset_choice == "Year 2016":
    st.session_state["filter_start"] = max(min_dataset_date, datetime.date(2016, 1, 1))
    st.session_state["filter_end"] = min(max_dataset_date, datetime.date(2016, 12, 31))
elif preset_choice == "Year 2015":
    st.session_state["filter_start"] = max(min_dataset_date, datetime.date(2015, 1, 1))
    st.session_state["filter_end"] = min(max_dataset_date, datetime.date(2015, 12, 31))
elif preset_choice == "Year 2014":
    st.session_state["filter_start"] = max(min_dataset_date, datetime.date(2014, 1, 1))
    st.session_state["filter_end"] = min(max_dataset_date, datetime.date(2014, 12, 31))
elif preset_choice == "Year 2013":
    st.session_state["filter_start"] = max(min_dataset_date, datetime.date(2013, 1, 1))
    st.session_state["filter_end"] = min(max_dataset_date, datetime.date(2013, 12, 31))

# Date Range Picker
date_input_value = st.sidebar.date_input(
    "Select Date Range",
    value=(st.session_state["filter_start"], st.session_state["filter_end"]),
    min_value=min_dataset_date,
    max_value=max_dataset_date,
    help="Filter all KPIs, charts, and summary statistics by start and end dates.",
)

# Unpack date selection
if isinstance(date_input_value, (tuple, list)) and len(date_input_value) == 2:
    start_date, end_date = date_input_value
    st.session_state["filter_start"] = start_date
    st.session_state["filter_end"] = end_date
elif isinstance(date_input_value, (tuple, list)) and len(date_input_value) == 1:
    start_date = date_input_value[0]
    end_date = max_dataset_date
else:
    start_date = min_dataset_date
    end_date = max_dataset_date

# Filter DataFrame by selected date range
mask = (df_full["date"].dt.date >= start_date) & (df_full["date"].dt.date <= end_date)
df_filtered = df_full.loc[mask].copy()

if df_filtered.empty:
    st.warning("⚠️ No data available for the selected date range. Please broaden your date filter.")
    st.stop()

# Sidebar summary info
st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    <div style='background:#F1F5F9; border-radius:8px; padding:12px; font-size:0.85rem; color:#475569;'>
        <b>📊 Filter Details</b><br>
        • Selected Days: <b>{len(df_filtered):,}</b><br>
        • From: <b>{start_date}</b><br>
        • To: <b>{end_date}</b><br>
        • Active Source: <b>{dataset_name}</b>
    </div>
    """,
    unsafe_allow_html=True,
)

# Architecture badge in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style='font-size:0.75rem; color:#64748B; text-align:center;'>
        <b>System Pipeline</b><br>
        Dataset → Pandas → Streamlit → Plotly → Docker → Kubernetes
    </div>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# 4. MAIN DASHBOARD HEADER & HERO BANNER
# ==============================================================================
st.markdown(
    f"""
    <div class="hero-banner">
        <h1 class="hero-title">🌦️ Delhi Weather Analytics Dashboard</h1>
        <div class="hero-subtitle">Historical Climate Trends & Weather Insights</div>
        <div class="hero-badges">
            <span class="badge">📍 City: New Delhi, India</span>
            <span class="badge">📅 Timeline: {start_date} to {end_date}</span>
            <span class="badge">📊 Records: {len(df_filtered):,} Daily Observations</span>
            <span class="badge">🚀 Production Ready: Docker & Kubernetes</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# 5. DYNAMIC KPI CARDS
# ==============================================================================
avg_temp = df_filtered["meantemp"].mean()
max_temp = df_filtered["meantemp"].max()
min_temp = df_filtered["meantemp"].min()
avg_hum = df_filtered["humidity"].mean()
avg_wind = df_filtered["wind_speed"].mean()

# Pressure stats (handling sensor anomalies gracefully)
valid_pressure = df_filtered["meanpressure"].dropna()
# Clean pressure for KPI display (exclude sensor malfunctions < 500 or > 2000 if present)
sensible_pressure = valid_pressure[(valid_pressure >= 800) & (valid_pressure <= 1200)]
avg_press = sensible_pressure.mean() if not sensible_pressure.empty else valid_pressure.mean()

st.markdown(
    f"""
    <div class="kpi-container">
        <div class="kpi-card kpi-temp">
            <div class="kpi-label">🌡️ Average Temperature</div>
            <div class="kpi-value">{avg_temp:.1f}<span class="kpi-unit">°C</span></div>
            <div class="kpi-sub">Min: {min_temp:.1f}°C in period</div>
        </div>
        <div class="kpi-card kpi-maxtemp">
            <div class="kpi-label">🔥 Maximum Temperature</div>
            <div class="kpi-value">{max_temp:.1f}<span class="kpi-unit">°C</span></div>
            <div class="kpi-sub">Peak heat recorded</div>
        </div>
        <div class="kpi-card kpi-hum">
            <div class="kpi-label">💧 Average Humidity</div>
            <div class="kpi-value">{avg_hum:.1f}<span class="kpi-unit">%</span></div>
            <div class="kpi-sub">Relative air moisture</div>
        </div>
        <div class="kpi-card kpi-wind">
            <div class="kpi-label">💨 Average Wind Speed</div>
            <div class="kpi-value">{avg_wind:.2f}<span class="kpi-unit">km/h</span></div>
            <div class="kpi-sub">Surface wind velocity</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# 6. VISUALIZATIONS (PLOTLY CHARTS)
# ==============================================================================

# Standard Plotly layout styling for a clean, professional academic presentation
PLOT_LAYOUT_DEFAULTS = dict(
    template="plotly_white",
    font=dict(family="Segoe UI, Roboto, sans-serif", color="#1E293B", size=12),
    title_font=dict(size=16, color="#0F172A", family="Segoe UI, Roboto, sans-serif"),
    margin=dict(l=40, r=30, t=55, b=40),
    hoverlabel=dict(bgcolor="#FFFFFF", font_size=12, font_family="Segoe UI, sans-serif"),
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
)

tab_overview, tab_monthly_corr, tab_summary, tab_raw = st.tabs(
    ["📈 Time Series Trends", "📊 Monthly & Correlation Analysis", "📋 Weather Summary", "🔍 Dataset Inspector"]
)

with tab_overview:
    # --------------------------------------------------------------------------
    # 1. Temperature Trend
    # --------------------------------------------------------------------------
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig_temp = go.Figure()

    # Daily line
    fig_temp.add_trace(
        go.Scatter(
            x=df_filtered["date"],
            y=df_filtered["meantemp"],
            mode="lines",
            name="Daily Mean Temp",
            line=dict(color="#EF4444", width=1.8),
            hovertemplate="<b>Date:</b> %{x|%d %b %Y}<br><b>Mean Temp:</b> %{y:.1f} °C<extra></extra>",
        )
    )

    # 30-day moving average for smoothing if dataset spans > 45 days
    if len(df_filtered) >= 45:
        df_filtered["temp_ma30"] = df_filtered["meantemp"].rolling(window=30, min_periods=7).mean()
        fig_temp.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered["temp_ma30"],
                mode="lines",
                name="30-Day Trend (MA)",
                line=dict(color="#991B1B", width=2.5, dash="solid"),
                hovertemplate="<b>Date:</b> %{x|%d %b %Y}<br><b>30-Day MA:</b> %{y:.1f} °C<extra></extra>",
            )
        )

    fig_temp.update_layout(
        **PLOT_LAYOUT_DEFAULTS,
        title="<b>Temperature Trend Over Time</b>",
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor="#F1F5F9",
            rangeslider=dict(visible=False),
        ),
        yaxis=dict(title="Mean Temperature (°C)", showgrid=True, gridcolor="#F1F5F9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=380,
    )
    st.plotly_chart(fig_temp, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 2. Humidity Trend
    # --------------------------------------------------------------------------
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig_hum = go.Figure()

    fig_hum.add_trace(
        go.Scatter(
            x=df_filtered["date"],
            y=df_filtered["humidity"],
            mode="lines",
            name="Daily Humidity",
            line=dict(color="#2563EB", width=1.8),
            fill="tozeroy",
            fillcolor="rgba(37, 99, 235, 0.08)",
            hovertemplate="<b>Date:</b> %{x|%d %b %Y}<br><b>Humidity:</b> %{y:.1f} %<extra></extra>",
        )
    )

    if len(df_filtered) >= 45:
        df_filtered["hum_ma30"] = df_filtered["humidity"].rolling(window=30, min_periods=7).mean()
        fig_hum.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered["hum_ma30"],
                mode="lines",
                name="30-Day Trend (MA)",
                line=dict(color="#1E40AF", width=2.5),
                hovertemplate="<b>Date:</b> %{x|%d %b %Y}<br><b>30-Day MA:</b> %{y:.1f} %<extra></extra>",
            )
        )

    fig_hum.update_layout(
        **PLOT_LAYOUT_DEFAULTS,
        title="<b>Humidity Trend Over Time</b>",
        xaxis=dict(title="Date", showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(title="Humidity (%)", showgrid=True, gridcolor="#F1F5F9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=360,
    )
    st.plotly_chart(fig_hum, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 3. Wind Speed Trend
    # --------------------------------------------------------------------------
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig_wind = go.Figure()

    fig_wind.add_trace(
        go.Scatter(
            x=df_filtered["date"],
            y=df_filtered["wind_speed"],
            mode="lines",
            name="Daily Wind Speed",
            line=dict(color="#059669", width=1.6),
            hovertemplate="<b>Date:</b> %{x|%d %b %Y}<br><b>Wind Speed:</b> %{y:.2f} km/h<extra></extra>",
        )
    )

    if len(df_filtered) >= 45:
        df_filtered["wind_ma30"] = df_filtered["wind_speed"].rolling(window=30, min_periods=7).mean()
        fig_wind.add_trace(
            go.Scatter(
                x=df_filtered["date"],
                y=df_filtered["wind_ma30"],
                mode="lines",
                name="30-Day Trend (MA)",
                line=dict(color="#065F46", width=2.2),
                hovertemplate="<b>Date:</b> %{x|%d %b %Y}<br><b>30-Day MA:</b> %{y:.2f} km/h<extra></extra>",
            )
        )

    fig_wind.update_layout(
        **PLOT_LAYOUT_DEFAULTS,
        title="<b>Wind Speed Trend</b>",
        xaxis=dict(title="Date", showgrid=True, gridcolor="#F1F5F9"),
        yaxis=dict(title="Wind Speed (km/h)", showgrid=True, gridcolor="#F1F5F9"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=360,
    )
    st.plotly_chart(fig_wind, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


with tab_monthly_corr:
    col_chart_left, col_chart_right = st.columns(2)

    with col_chart_left:
        # ----------------------------------------------------------------------
        # 4. Temperature vs Humidity (Scatter Plot)
        # ----------------------------------------------------------------------
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)

        fig_scatter = px.scatter(
            df_filtered,
            x="meantemp",
            y="humidity",
            color="month_name",
            color_discrete_sequence=px.colors.qualitative.Safe,
            hover_name=df_filtered["date"].dt.strftime("%Y-%m-%d"),
            hover_data={"date": False, "meantemp": ":.1f", "humidity": ":.1f", "wind_speed": ":.1f"},
            labels={
                "meantemp": "Mean Temperature (°C)",
                "humidity": "Humidity (%)",
                "month_name": "Month",
            },
            title="<b>Temperature vs Humidity</b>",
        )

        # Standalone regression trendline without requiring extra dependencies
        if len(df_filtered.dropna(subset=["meantemp", "humidity"])) > 2:
            clean_scatter = df_filtered.dropna(subset=["meantemp", "humidity"])
            x_vals = clean_scatter["meantemp"].values
            y_vals = clean_scatter["humidity"].values
            # Linear fit: y = m*x + c
            coeffs = np.polyfit(x_vals, y_vals, 1)
            x_trend = np.linspace(x_vals.min(), x_vals.max(), 100)
            y_trend = np.polyval(coeffs, x_trend)
            fig_scatter.add_trace(
                go.Scatter(
                    x=x_trend,
                    y=y_trend,
                    mode="lines",
                    name=f"Linear Fit (Slope: {coeffs[0]:.2f})",
                    line=dict(color="#1E293B", width=2.5, dash="dash"),
                    hoverinfo="skip",
                )
            )

        fig_scatter.update_layout(
            **PLOT_LAYOUT_DEFAULTS,
            height=460,
            xaxis=dict(title="Temperature (°C)", showgrid=True, gridcolor="#F1F5F9"),
            yaxis=dict(title="Humidity (%)", showgrid=True, gridcolor="#F1F5F9"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_chart_right:
        # ----------------------------------------------------------------------
        # 5. Monthly Temperature Analysis (Bar Chart)
        # ----------------------------------------------------------------------
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)

        # Group data by month and calculate average temperature
        month_order = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ]
        monthly_stats = (
            df_filtered.groupby("month_name", as_index=False)["meantemp"]
            .mean()
            .rename(columns={"meantemp": "avg_meantemp"})
        )
        # Sort chronologically by calendar month
        monthly_stats["month_cat"] = pd.Categorical(monthly_stats["month_name"], categories=month_order, ordered=True)
        monthly_stats = monthly_stats.sort_values("month_cat").reset_index(drop=True)

        fig_monthly = px.bar(
            monthly_stats,
            x="month_name",
            y="avg_meantemp",
            text="avg_meantemp",
            labels={"month_name": "Month", "avg_meantemp": "Average Temperature (°C)"},
            title="<b>Average Temperature by Month</b>",
            color="avg_meantemp",
            color_continuous_scale="Temps",
        )

        fig_monthly.update_traces(
            texttemplate="%{text:.1f}°C",
            textposition="outside",
            marker_line_color="#FFFFFF",
            marker_line_width=1.5,
        )

        fig_monthly.update_layout(
            **PLOT_LAYOUT_DEFAULTS,
            height=460,
            coloraxis_showscale=False,
            xaxis=dict(title="Month", showgrid=False),
            yaxis=dict(
                title="Average Temperature (°C)",
                showgrid=True,
                gridcolor="#F1F5F9",
                range=[0, max(monthly_stats["avg_meantemp"].max() * 1.2, 40)],
            ),
        )
        st.plotly_chart(fig_monthly, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


with tab_summary:
    # --------------------------------------------------------------------------
    # 6. Weather Summary Table
    # --------------------------------------------------------------------------
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("📋 Climate Summary Statistics")
    st.markdown(
        "Key meteorological indicators computed dynamically over the selected date range "
        f"(**{start_date}** to **{end_date}**):"
    )

    # Calculate required summary values
    sum_avg_temp = df_filtered["meantemp"].mean()
    sum_min_temp = df_filtered["meantemp"].min()
    sum_max_temp = df_filtered["meantemp"].max()
    sum_avg_hum = df_filtered["humidity"].mean()
    sum_avg_wind = df_filtered["wind_speed"].mean()

    # Pressure: compute standard average
    if "meanpressure" in df_filtered.columns and not df_filtered["meanpressure"].dropna().empty:
        sum_avg_press = df_filtered["meanpressure"].mean()
        # Also clean anomaly-filtered pressure for transparency
        sensible_press_series = df_filtered["meanpressure"][
            (df_filtered["meanpressure"] >= 800) & (df_filtered["meanpressure"] <= 1200)
        ]
        sum_avg_press_clean = (
            sensible_press_series.mean() if not sensible_press_series.empty else sum_avg_press
        )
    else:
        sum_avg_press = np.nan
        sum_avg_press_clean = np.nan

    # Create presentation dataframe
    summary_data = [
        {"Metric": "Average Temperature", "Value": f"{sum_avg_temp:.2f} °C", "Description": "Mean daily temperature across period"},
        {"Metric": "Minimum Temperature", "Value": f"{sum_min_temp:.2f} °C", "Description": "Lowest recorded daily mean temperature"},
        {"Metric": "Maximum Temperature", "Value": f"{sum_max_temp:.2f} °C", "Description": "Highest recorded daily mean temperature"},
        {"Metric": "Average Humidity", "Value": f"{sum_avg_hum:.2f} %", "Description": "Mean relative atmospheric humidity"},
        {"Metric": "Average Wind Speed", "Value": f"{sum_avg_wind:.2f} km/h", "Description": "Mean daily surface wind speed"},
        {
            "Metric": "Average Pressure",
            "Value": f"{sum_avg_press:.2f} hPa" if np.isnan(sum_avg_press_clean) or abs(sum_avg_press - sum_avg_press_clean) < 50 else f"{sum_avg_press_clean:.2f} hPa (Raw: {sum_avg_press:.2f} hPa)",
            "Description": "Mean sea-level/station atmospheric pressure",
        },
    ]

    summary_df = pd.DataFrame(summary_data)
    st.table(summary_df)

    st.markdown("---")
    st.markdown("#### 📐 Statistical Distribution (Percentiles)")
    describe_df = df_filtered[["meantemp", "humidity", "wind_speed", "meanpressure"]].describe().T
    describe_df.columns = ["Count", "Mean", "Std Dev", "Min", "25%", "50% (Median)", "75%", "Max"]
    describe_df = describe_df.round(2)
    st.dataframe(describe_df, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


with tab_raw:
    # --------------------------------------------------------------------------
    # Dataset Inspector & Download
    # --------------------------------------------------------------------------
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.subheader("🔍 Dataset Inspector & Verification")
    st.markdown(
        f"Active Dataset: **`{dataset_name}`** | Filtered Rows: **{len(df_filtered)}** of **{len(df_full)}**"
    )

    # Column inspection metadata
    col_meta1, col_meta2, col_meta3, col_meta4 = st.columns(4)
    col_meta1.metric("Date Column", "date (datetime64)")
    col_meta2.metric("Temperature Column", "meantemp (float64)")
    col_meta3.metric("Humidity Column", "humidity (float64)")
    col_meta4.metric("Wind Speed Column", "wind_speed (float64)")

    # Data preview
    st.dataframe(
        df_filtered[["date", "meantemp", "humidity", "wind_speed", "meanpressure"]].head(50),
        use_container_width=True,
    )

    # CSV Download Button
    csv_bytes = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered CSV",
        data=csv_bytes,
        file_name=f"delhi_weather_filtered_{start_date}_{end_date}.csv",
        mime="text/csv",
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# 7. FOOTER
# ==============================================================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #64748B; font-size: 0.85rem; padding: 10px 0;'>
        <b>Delhi Weather Analytics Dashboard</b> | Academic & Engineering Demo<br>
        Architecture: Existing Dataset → Pandas Data Cleaning → Streamlit → Plotly Visualizations → Docker Container → Kubernetes Pod
    </div>
    """,
    unsafe_allow_html=True,
)
