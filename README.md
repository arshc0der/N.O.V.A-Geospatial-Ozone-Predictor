# 🌍 N.O.V.A. — Geospatial Ozone Predictor

> An advanced atmospheric intelligence platform using NASA data (1994–2021), Stochastic Machine Learning, and Real-Time Telemetry.

<p align="left">
  <img src="https://img.shields.io/badge/status-Stable-brightgreen.svg" />
  <img src="https://img.shields.io/github/license/arshc0der/N.O.V.A-Geospatial-Ozone-Predictor?color=green" />
  <img src="https://img.shields.io/badge/language-Python%203-3776AB.svg?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/framework-Tkinter-blue.svg" />
  <img src="https://img.shields.io/badge/AI-Scikit--Learn-F7931E.svg" />
  <img src="https://img.shields.io/badge/data-NASA-0B3D91.svg" />
  <img src="https://img.shields.io/github/stars/arshc0der/N.O.V.A-Geospatial-Ozone-Predictor?style=social" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/arshc0der/N.O.V.A-Geospatial-Ozone-Predictor/refs/heads/main/preview/logo.svg" width="100%" alt="NOVA Dashboard"/>
</p>

---

# 📌 Overview

**N.O.V.A. (North American Ozone Visual Analytics)** is a Mission Control–style atmospheric intelligence system designed to analyze, visualize, and predict stratospheric and tropospheric Ozone (O₃) concentrations across Western North America.

It transforms nearly 30 years of NASA/FLEXPART atmospheric back-trajectory data into an interactive desktop dashboard combining:

- 📊 Historical Geospatial Visualization  
- 🤖 Random Forest Machine Learning Prediction  
- 🛰️ Real-Time ISS Telemetry Tracking  

---

# ✨ Core Features

| Feature | Description |
|----------|-------------|
| 🌌 **3D Geospatial Visualization** | Interactive 3D atmospheric ozone distribution |
| 📈 **Trend Analysis** | Historical line graph and seasonal analysis |
| 🤖 **AI Prediction Engine** | 50-tree Random Forest Regressor |
| 🛰️ **Live ISS Tracker** | Real-time satellite telemetry via API |
| 🎛️ **Mission Control UI** | Dark cyber-corporate themed interface |

---

# 🖼 UI Preview

## 1️⃣ Dashboard
<p align="center">
  <img src="https://raw.githubusercontent.com/arshc0der/N.O.V.A-Geospatial-Ozone-Predictor/refs/heads/main/preview/1.png" width="100%" />
</p>

---

## 2️⃣ 3D Visualization
<p align="center">
  <img src="https://raw.githubusercontent.com/arshc0der/N.O.V.A-Geospatial-Ozone-Predictor/refs/heads/main/preview/2.png" width="100%" />
</p>

---

## 3️⃣ Line Graph Analysis
<p align="center">
  <img src="https://raw.githubusercontent.com/arshc0der/N.O.V.A-Geospatial-Ozone-Predictor/refs/heads/main/preview/3.png" width="100%" />
</p>

---

## 4️⃣ AI Prediction Engine
<p align="center">
  <img src="https://raw.githubusercontent.com/arshc0der/N.O.V.A-Geospatial-Ozone-Predictor/refs/heads/main/preview/4.png" width="100%" />
</p>

---

## 5️⃣ Live Satellite Location (ISS Tracking)
<p align="center">
  <img src="https://raw.githubusercontent.com/arshc0der/N.O.V.A-Geospatial-Ozone-Predictor/refs/heads/main/preview/5.png" width="100%" />
</p>

---

# 🧠 Data Science & AI Logic

### 📥 Independent Variables (Features)
- Pressure (hPa) — Represents altitude  
- Latitude  
- Longitude  
- Month  
- Year  

### 📤 Dependent Variable (Target)
- Ozone Concentration (ppbv)

---

### 🤖 Model Details

- Algorithm: **Random Forest Regressor**
- Trees: 50 (`n_estimators=50`)
- Train/Test Split: 80/20
- Typical R² Score: **0.85 – 0.94**
- Most Influential Feature: **Pressure (Altitude)**

Random Forest was selected because atmospheric ozone behavior is non-linear and seasonal, making linear regression insufficient.

---

# 🛰️ Real-Time Telemetry

The ISS tracking system:

- Fetches live coordinates from a public API
- Updates every 3 seconds
- Runs in a background thread
- Prevents UI freezing using multithreading

---

# 🏗 Architecture

N.O.V.A. follows the **Model–View–Controller (MVC)** pattern:

| Layer | Role |
|--------|------|
| Model | Data processing & AI engine |
| View | Tkinter GUI interface |
| Controller | User-triggered simulation & visualization logic |

---

# 🛠 Installation & Setup

## 🔹 1. Clone Repository

```bash
git clone https://github.com/arshc0der/N.O.V.A-Geospatial-Ozone-Predictor.git
cd N.O.V.A-Geospatial-Ozone-Predictor
````

---

## 🔹 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

## 🔹 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔹 4. Ensure Dataset File Exists

Place this file in the root directory:

```
Receptor_western_NAmerica_ozone_obs_1994_2021_from900to300.csv
```

---

## 🔹 5. Run Application

```bash
python app.py
```

---

# 📦 requirements.txt

```
pandas
numpy
scikit-learn
matplotlib
seaborn
requests
tkintermapview
```

---

# 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Submit a Pull Request

---

# 📜 License

Distributed under the **MIT License**.
© 2026 Arsh

---

### 🚀 Built using NASA atmospheric back-trajectory data.
