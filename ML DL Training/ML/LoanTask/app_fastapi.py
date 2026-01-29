import streamlit as st
import joblib
import pandas as pd

# Title and description
st.title("📊 Loan Prediction App")
st.write("This app uses a pretrained machine learning model (`loan_pretrained.pkl`) to predict loan approvals.")

# Load the pretrained model
model = joblib.load("loan_pretrained.pkl")
st.success("✅ Model loaded successfully: `loan_pretrained.pkl`")

# Sidebar for user input
st.sidebar.header("Enter Applicant Details")

# Example input fields (customize based on your dataset features)
age = st.sidebar.number_input("Age", min_value=18, max_value=70, value=30)
income = st.sidebar.number_input("Annual Income (₹)", min_value=0, value=500000)
loan_amount = st.sidebar.number_input("Loan Amount (₹)", min_value=0, value=200000)
credit_score = st.sidebar.slider("Credit Score", min_value=300, max_value=850, value=650)

# Create dataframe from inputs
input_data = pd.DataFrame({
    "Age": [age],
    "Income": [income],
    "LoanAmount": [loan_amount],
    "CreditScore": [credit_score]
})

st.subheader("🔎 Applicant Data Preview")
st.write(input_data)

# Prediction button
if st.button("Predict Loan Approval"):
    prediction = model.predict(input_data)
    if prediction[0] == 1:
        st.success("🎉 Loan Approved!")
    else:
        st.error("❌ Loan Not Approved")
