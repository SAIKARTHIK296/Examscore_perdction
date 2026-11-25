import streamlit as st
import pandas as pd
import joblib
from exam_report_generator import generate_exam_report

# CONFIG
st.set_page_config(page_title="Exam Score Prediction", layout="wide")

# LOAD CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# LOAD MODEL
model = joblib.load("best_exam_score_model.pkl")

# HEADER
st.markdown("<h1>🎓 Exam Score Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p>Enter student details to estimate expected exam performance accurately.</p>", unsafe_allow_html=True)

# FORM CONTAINER
st.markdown("<div class='form-card'>", unsafe_allow_html=True)

student_name = st.text_input("Student Name")

st.subheader("📘 Academic & Lifestyle")
study_hours_per_day = st.slider("Study Hours per Day", 0.0, 12.0, 6.0)
sleep_hours = st.slider("Sleep Duration (hours/day)", 3.0, 12.0, 7.0)
attendance_percentage = st.slider("Attendance Percentage", 40, 100, 85)

social_media_hours = st.slider("Social Media Usage (hours/day)", 0.0, 5.0, 2.0)
netflix_hours = st.slider("Streaming Hours (Netflix/YouTube)", 0.0, 4.0, 1.0)
screen_time = st.slider("Other Screen Time (hours/day)", 0.0, 10.0, 3.0)

st.subheader("🧠 Psychological Factors")
stress_level = st.slider("Stress Level", 1, 10, 3)
exam_anxiety_score = st.slider("Exam Anxiety Score", 1, 10, 4)
motivation_level = st.slider("Motivation Level", 1, 10, 8)
time_management_score = st.slider("Time Management Score", 1, 10, 7)

st.subheader("📊 Academic History")
previous_gpa = st.slider("Previous GPA (0 - 4 Scale)", 0.0, 4.0, 3.2)

st.subheader("🏷 Personal & Support Factors")

parental_education_level = st.selectbox(
    "Parental Education Level",
    ["Some College", "High School", "Bachelor", "Master", "PhD"]
)

major = st.selectbox(
    "Major",
    ["Arts", "Biology", "Business", "Computer Science", "Engineering", "Psychology"]
)

study_environment = st.selectbox(
    "Study Environment",
    ["Cafe", "Co-Learning Group", "Dorm", "Library", "Quiet Room"]
)

diet_quality = st.selectbox(
    "Diet Quality",
    ["Good", "Fair", "Poor"]
)

st.markdown("</div>", unsafe_allow_html=True)

# PREDICT
if st.button("🔮 Predict Exam Score"):

    if student_name.strip() == "":
        st.markdown("""
        <div class='custom-warning'>
        ⚠️ Please enter the Student Name before predicting!
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    screen_time_total = social_media_hours + netflix_hours + screen_time
    study_sleep_ratio = study_hours_per_day / sleep_hours if sleep_hours != 0 else 0
    stress_anxiety = stress_level + exam_anxiety_score

    input_data = pd.DataFrame([{
        "previous_gpa": previous_gpa,
        "motivation_level": motivation_level,
        "stress_anxiety": stress_anxiety,
        "study_sleep_ratio": study_sleep_ratio,
        "screen_time_total": screen_time_total,
        "time_management_score": time_management_score,
        "attendance_percentage": attendance_percentage,
        "major": major,
        "study_environment": study_environment,
        "parental_education_level": parental_education_level,
        "diet_quality": diet_quality
    }])

    prediction = model.predict(input_data)[0]
    prediction = max(0, min(100, prediction))

    if prediction >= 85:
        status = "🌟 Excellent Performance"
    elif prediction >= 60:
        status = "🙂 Good Performance"
    else:
        status = "⚠️ Needs Improvement"

    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">{status}</div>
        <div class="result-score">{prediction:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    # Generate PDF
    pdf_buffer = generate_exam_report(
        student_name,
        input_data.iloc[0].to_dict(),
        prediction,
        status
    )

    st.download_button(
        label="📄 Download Report",
        data=pdf_buffer,
        file_name=f"{student_name}_exam_score_report.pdf",
        mime="application/pdf",
    )
