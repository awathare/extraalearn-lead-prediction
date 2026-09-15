import pandas as pd
import requests
import streamlit as st
import os


st.set_page_config(page_title="ExtraaLearn Lead Conversion", layout="centered")
st.title("ExtraaLearn Lead Conversion Prediction")
st.write(
    "Score a lead as likely to convert (hot) or not (cold) using the deployed ExtraaLearn model."
)

# Base URL of the Flask backend
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:7860")

st.subheader("Online Prediction")

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", min_value=18, max_value=80, value=35)
    current_occupation = st.selectbox(
        "Current Occupation", ["Professional", "Unemployed", "Student"]
    )
    first_interaction = st.selectbox("First Interaction", ["Website", "Mobile App"])
    profile_completed = st.selectbox("Profile Completed", ["High", "Medium", "Low"])
    website_visits = st.number_input("Website Visits", min_value=0, value=3)
    time_spent_on_website = st.number_input(
        "Time Spent on Website (seconds)", min_value=0, value=600
    )
with col2:
    page_views_per_visit = st.number_input(
        "Page Views per Visit", min_value=0.0, value=2.5, step=0.1
    )
    last_activity = st.selectbox(
        "Last Activity", ["Email Activity", "Phone Activity", "Website Activity"]
    )
    print_media_type1 = st.selectbox("Seen Newspaper Ad?", ["No", "Yes"])
    print_media_type2 = st.selectbox("Seen Magazine Ad?", ["No", "Yes"])
    digital_media = st.selectbox("Seen Digital Ad?", ["No", "Yes"])
    educational_channels = st.selectbox("Heard via Educational Channels?", ["No", "Yes"])
    referral = st.selectbox("Referred?", ["No", "Yes"])

payload = {
    "age": age,
    "current_occupation": current_occupation,
    "first_interaction": first_interaction,
    "profile_completed": profile_completed,
    "website_visits": website_visits,
    "time_spent_on_website": time_spent_on_website,
    "page_views_per_visit": page_views_per_visit,
    "last_activity": last_activity,
    "print_media_type1": print_media_type1,
    "print_media_type2": print_media_type2,
    "digital_media": digital_media,
    "educational_channels": educational_channels,
    "referral": referral,
}

if st.button("Predict Conversion"):
    try:
        response = requests.post(f"{BACKEND_URL}/v1/predict", json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            prediction = result["prediction"]
            probability = result["conversion_probability"]
            if prediction == "Converted":
                st.success(f"Prediction: {prediction} (hot lead)")
            else:
                st.warning(f"Prediction: {prediction} (cold lead)")
            st.info(f"Conversion probability: {probability}")
            st.progress(min(max(float(probability), 0.0), 1.0))
        else:
            st.error(f"API error {response.status_code}: {response.text}")
    except Exception as exc:
        st.error(f"Could not reach the backend at {BACKEND_URL}: {exc}")
