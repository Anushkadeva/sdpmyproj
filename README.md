# 🌦️ Delhi Weather Analytics Dashboard

> **Historical Climate Trends & Weather Insights**  
> An end-to-end cloud-native data analytics dashboard demonstrating the pipeline:  
> **Existing Kaggle Dataset → Pandas → Streamlit → Plotly → Docker → Kubernetes**

---

## 📌 1. Project Overview

The **Delhi Weather Analytics Dashboard** is an academic and engineering demonstration project that visualizes historical climate data for the city of New Delhi, India. It provides interactive time series explorations, correlation insights, monthly temperature patterns, dynamic KPI aggregations, and customizable date-range filtering.

The application is containerized with **Docker** and orchestrated using **Kubernetes**, reflecting modern DevOps and cloud data engineering workflows.

---

## 📊 2. Dataset Description

The application directly utilizes the existing project dataset (**Daily Climate time series data in Delhi**, originally sourced from Kaggle/India Meteorological Department):

- **Files in Project**:
  - `DailyDelhiClimateTrain.csv`: 1,462 observations (January 1, 2013 to January 1, 2017)
  - `DailyDelhiClimateTest.csv`: 114 observations (January 1, 2017 to April 24, 2017)
  - **Combined Coverage**: 1,575 daily climate records spanning over 4 continuous years.
- **Attributes / Columns**:
  - `date`: Daily observation timestamp (`YYYY-MM-DD`)
  - `meantemp`: Daily average temperature (in **°C**)
  - `humidity`: Relative air humidity (in **%**)
  - `wind_speed`: Average surface wind velocity (in **km/h**)
  - `meanpressure`: Atmospheric sea-level/station pressure (in **hPa** / mbar)
- **Data Quality**: 0 missing values; automatically deduplicated and validated upon loading.

---

## ✨ 3. Key Features

- **Dynamic KPI Metric Cards**:
  - 🌡️ **Average Temperature** (°C)
  - 🔥 **Maximum Temperature** (°C)
  - 💧 **Average Humidity** (%)
  - 💨 **Average Wind Speed** (km/h)
- **Interactive Plotly Visualizations**:
  1. **Temperature Trend Over Time**: Interactive line chart with 30-day moving average overlay.
  2. **Humidity Trend Over Time**: Time series line chart with area shading.
  3. **Wind Speed Trend**: Velocity fluctuation tracking.
  4. **Temperature vs Humidity**: Scatter plot with hover date tooltips and fitted linear regression line showing negative correlation.
  5. **Average Temperature by Month**: Categorical bar chart highlighting seasonal variations across calendar months.
  6. **Climate Summary Statistics**: Formatted meteorological summary table and statistical quartile distributions.
- **Dynamic Sidebar Controls**:
  - Interactive date range calendar picker (`start_date` to `end_date`).
  - Quick-select presets (`Full History`, `2016`, `2015`, `2014`, `2013`).
  - Instant `🔄 Reset Filters` button restoring full time span.
  - Multi-dataset selector (`Combined`, `Train (2013-2016)`, `Test (2017)`).
- **Data Inspector & Export**:
  - Expandable tabular view with search.
  - One-click `📥 Download Filtered CSV` button.

---

## 🛠️ 4. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.11 | Core application logic |
| **Data Processing** | Pandas, NumPy | Data cleaning, type conversion, aggregation |
| **Web Dashboard** | Streamlit | Responsive frontend and dynamic state management |
| **Data Visualization** | Plotly Express & Graph Objects | Interactive charts, scatter plots, and tooltips |
| **Containerization** | Docker | Standardized, lightweight image (`python:3.11-slim`) |
| **Orchestration** | Kubernetes | Declarative Pod deployment, self-healing, NodePort service |

---

## 🏗️ 5. Final Architecture

```text
Existing Kaggle Dataset (DailyDelhiClimateTrain.csv & DailyDelhiClimateTest.csv)
          ↓
       Pandas (Data Cleaning, Validation, Sorting, Aggregation)
          ↓
     Streamlit (Stateful UI, Responsive Light Theme, Filters)
          ↓
       Plotly (Interactive Visualizations & Tooltips)
          ↓
     Docker Image (weather-dashboard:latest)
          ↓
   Kubernetes Pod (Resource-constrained container with Healthchecks)
          ↓
 Kubernetes Service (NodePort: 30501 / Port: 8501)
          ↓
   Weather Dashboard (Accessible at http://localhost:8501 or http://localhost:30501)
```

---

## 📂 6. Project Structure

```text
SDP MYPROJ/
├── .github/
│   └── workflows/
│       └── main.yml              # Capstone CI/CD pipeline (Test → Build → Deploy)
├── .gitignore                    # Git ignore file for temporary artifacts
├── .streamlit/
│   └── config.toml               # Streamlit theme & server configuration
├── k8s/
│   ├── deployment.yaml           # Kubernetes Deployment specification (2 replicas)
│   ├── service.yaml              # Kubernetes Service (NodePort)
│   └── hpa.yaml                  # Horizontal Pod Autoscaler (2-5 replicas, 70% CPU)
├── tests/
│   └── test_data_pipeline.py     # Unit test suite for pytest validation
├── .dockerignore                 # Excluded files for Docker build context
├── app.py                        # Streamlit dashboard application
├── DailyDelhiClimateTrain.csv   # Existing training dataset (2013-2017)
├── DailyDelhiClimateTest.csv    # Existing test dataset (2017)
├── Dockerfile                    # Containerization recipe (non-root user, layer caching)
├── README.md                     # Comprehensive documentation
└── requirements.txt              # Python runtime dependencies (includes pytest)
```

---

## 🔄 7. Capstone CI/CD Pipeline

### Pipeline Architecture (Trigger → Test → Build → Deploy)

```text
GitHub (Push to main)
        ↓
GitHub Actions (.github/workflows/main.yml)
        ↓
┌───────────────────────────────────────────────┐
│ Stage 1: TEST                                 │
│ - Set up Python 3.11                          │
│ - Install dependencies from requirements.txt │
│ - Run pytest unit tests on data pipeline      │
└───────────────────────┬───────────────────────┘
                        ↓ (on success)
┌───────────────────────────────────────────────┐
│ Stage 2: BUILD                                │
│ - Set up Docker Buildx                        │
│ - Authenticate to Docker Hub via Secrets      │
│ - Build optimized Docker image (non-root)     │
│ - Push dual tags: :latest and :<git-sha>      │
└───────────────────────┬───────────────────────┘
                        ↓ (on success)
┌───────────────────────────────────────────────┐
│ Stage 3: DEPLOY                               │
│ - Set up kubectl environment                  │
│ - Client dry-run validate all k8s manifests   │
│ - Emit zero-downtime rolling update commands  │
└───────────────────────────────────────────────┘
```

### Horizontal Pod Autoscaler (HPA)

The application includes automated horizontal pod autoscaling configured in `k8s/hpa.yaml`:
- **Min Replicas**: 2
- **Max Replicas**: 5
- **CPU Target**: 70% utilization

To view autoscaling status:
```bash
kubectl get hpa
```

---

## 🚀 8. Step-by-Step Setup & Execution

### Option A: Running Locally with Python

1. **Clone or navigate to the project directory**:
   ```bash
   cd "d:/SDP MYPROJ"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Streamlit dashboard**:
   ```bash
   streamlit run app.py
   ```

4. **Access the application**:
   Open browser at: `http://localhost:8501`

---

### Option B: Running with Docker

1. **Build the Docker container image**:
   ```bash
   docker build -t weather-dashboard .
   ```

2. **Run the Docker container**:
   - If port `8501` is free:
     ```bash
     docker run -d -p 8501:8501 --name weather-dashboard-app weather-dashboard
     ```
     Access at: `http://localhost:8501`
   - If port `8501` is occupied (e.g., by existing Zomato project):
     ```bash
     docker run -d -p 8502:8501 --name weather-dashboard-app weather-dashboard
     ```
     Access at: `http://localhost:8502`

3. **Verify the container is running**:
   ```bash
   docker ps
   ```

4. **Stop and cleanup container (when done)**:
   ```bash
   docker stop weather-dashboard-app
   docker rm weather-dashboard-app
   ```


---

### Option C: Deploying to Kubernetes (Docker Desktop / Minikube)

1. **Ensure your Kubernetes cluster is active**:
   ```bash
   kubectl cluster-info
   ```

2. **Ensure the local Docker image is built**:
   ```bash
   docker build -t weather-dashboard:latest .
   ```

3. **Apply the Kubernetes deployment and service manifests**:
   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```

4. **Check deployment and pod status**:
   ```bash
   kubectl get pods -l app=weather-dashboard
   kubectl get svc weather-dashboard-service
   ```

5. **Access the dashboard**:
   - **Via NodePort directly (Docker Desktop / Local Cluster)**:
     `http://localhost:30501`
   - **Via Port Forwarding (Universal)**:
     ```bash
     kubectl port-forward svc/weather-dashboard-service 8501:8501
     ```
     Then open: `http://localhost:8501`

6. **Cleanup Kubernetes resources (when done)**:
   ```bash
   kubectl delete -f k8s/service.yaml
   kubectl delete -f k8s/deployment.yaml
   ```

---

## 🔍 8. Assumptions & Adaptations Made

1. **Existing Dataset Detection**: The application automatically inspects the workspace directory for `DailyDelhiClimateTrain.csv` and `DailyDelhiClimateTest.csv`. It combines and deduplicates them to provide the complete 2013–2017 timeline, while also enabling single-file views via the sidebar.
2. **Column Names**: The dataset uses `date`, `meantemp`, `humidity`, `wind_speed`, and `meanpressure`. The code handles both exact column names and case/alias variations (`temp`, `meantemp`, `pressure`, etc.).
3. **Pressure Anomalies**: Historical sensor dropouts/spikes present in the Kaggle dataset (e.g., negative or extreme pressure readings) are documented and reported transparently in the statistical summary without mutating raw data.

---

## 🔮 9. Future Improvements

- Incorporate machine learning forecasting (e.g. ARIMA, Prophet, or LSTM) for predictive weather trends.
- Add live weather API integration (e.g., OpenWeatherMap) to compare historical climate with real-time conditions.
- Implement automated CI/CD pipeline using GitHub Actions to push images to Docker Hub / Container Registry.
- Configure Kubernetes Horizontal Pod Autoscaler (HPA) and Ingress controller with TLS.
