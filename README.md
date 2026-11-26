<div align="center">

# 🎓 Exam Score Prediction Engine

**End-to-End Student Performance Forecasting Platform with Real-Time Feature Engineering, Glassmorphism UI & Automated PDF Assessment Reports**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-189FDD?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io/)
[![ReportLab](https://img.shields.io/badge/ReportLab-PDF_Engine-0D2A78?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)](https://www.reportlab.com/)
[![CSS3](https://img.shields.io/badge/UI-Glassmorphism_CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)]()

*Predict student exam scores from 80,000+ academic, lifestyle, and psychological records — complete with custom behavioral ratios and instant downloadable PDF performance reports.*

</div>

---

## ⚡ Overview

Academic outcomes are driven by the interplay of study habits, sleep hygiene, digital distractions, psychological pressure, and support environments. This repository delivers a **complete ML training pipeline and interactive Streamlit web application** that estimates a student's expected exam score (`0–100`) and generates a tailored, downloadable PDF assessment report in one click.

* **80,000-Record Training Pipeline** — Trained and benchmarked across `dataset_academic.csv` (80,000 rows × 31 features) using `XGBRegressor`, `RandomForestRegressor`, and `SVR`.
* **Domain Feature Engineering** — Synthesizes composite behavioral signals (`screen_time_total`, `study_sleep_ratio`, `stress_anxiety`) dynamically during both training and live inference.
* **Custom Dark Glassmorphism UI** — Styled via `style.css` with frosted-glass containers, `Space Grotesk` + `Inter` typography, and neon cyan-blue gradients.
* **Automated PDF Reporting** — `exam_report_generator.py` uses `ReportLab` to build timestamped, color-coded PDF assessment sheets with feature breakdowns and tiered study recommendations.

---

## 🏗️ System Architecture

```mermaid
flowchart LR
    subgraph Training [Offline ML Pipeline]
        D[dataset_academic.csv<br/>80,000 rows × 31 cols] --> FE1[Feature Engineering<br/>screen_time_total<br/>study_sleep_ratio<br/>stress_anxiety]
        FE1 --> PP[ColumnTransformer<br/>StandardScaler + OneHotEncoder]
        PP --> BM[Model Benchmarking<br/>XGBoost · RandomForest · SVR]
        BM --> PKL[(best_exam_score_model.pkl)]
    end

    subgraph Inference [Live Streamlit Application]
        UI[app.py + style.css<br/>15 Student Inputs] --> FE2[Live Feature Transform<br/>11 Model Features]
        PKL --> INF[Joblib Pipeline Inference<br/>Clamped 0–100]
        FE2 --> INF
        INF --> CARD[Glassmorphism Score Card<br/>& Performance Tier]
        INF --> PDF[exam_report_generator.py<br/>ReportLab PDF Buffer]
        PDF --> DL[One-Click PDF Download]
    end
