import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load model and features
model = joblib.load("readmission_model.pkl")
features = joblib.load("model_features.pkl")

st.set_page_config(page_title="Hospital Readmission Predictor", page_icon="🏥")
st.title("🏥 Hospital Readmission Risk Predictor")
st.markdown("---")

st.markdown("Enter patient details to predict the risk of 30-day readmission.")

# Build a dynamic input form
input_data = {}

for col in features:
    if 'num' in col or 'days' in col or 'time' in col or 'visits' in col:
        input_data[col] = st.number_input(f"{col}", min_value=0, value=1)
    else:
        input_data[col] = st.selectbox(f"{col}", options=[0, 1])

# Predict button
if st.button("Predict Readmission"):
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    st.markdown("---")
    if prediction == 1:
        st.error(f"⚠️ High risk of readmission within 30 days. Probability: {probability:.2f}")
    else:
        st.success(f"✅ Low risk of readmission. Probability: {probability:.2f}")
