
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# ---- Title & Description ----
st.title("Fraud Detection Dashboard")
st.markdown("""
### Project Overview  
This dashboard provides an interactive analysis of transaction data to detect fraudulent activities.  
It helps identify key patterns related to transaction amount, time, location, and customer segments.

### Problem Statement  
Financial institutions struggle with quickly detecting fraudulent transactions among massive data.  
This dashboard simplifies fraud analysis through an easy-to-use interface for exploring transaction data.
""")

# ---- Load Dataset ----
df = pd.read_csv("C:\\Users\\ADMIN\\Documents\\finance_transactions_dataset.csv")

# Preprocess
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])
df['Transaction Year'] = df['Transaction Date'].dt.year
df['Transaction Month'] = df['Transaction Date'].dt.month
df['Transaction Day'] = df['Transaction Date'].dt.day

# ---- Fraud Prediction Inputs ----
st.sidebar.header("🔍 Fraud Check Input")
st.sidebar.markdown("Use this form to test if a transaction is likely fraudulent.")

amount_input = st.sidebar.number_input("Transaction Amount (KES)", min_value=0.0, value=5000.0)
year_input = st.sidebar.number_input("Transaction Year", min_value=2000, max_value=2100, value=2023)
month_input = st.sidebar.number_input("Transaction Month", min_value=1, max_value=12, value=1)
day_input = st.sidebar.number_input("Transaction Day", min_value=1, max_value=31, value=1)
transaction_type_input = st.sidebar.selectbox("Transaction Type", df["Transaction Type"].unique())
channel_input = st.sidebar.selectbox("Transaction Channel", df["Transaction Channel"].unique())

# ---- Fraud Prediction ----
st.header("🔍 Predict Fraudulent Transaction")
if st.button("Run Fraud Check"):
    # Dummy logic — replace with model prediction
    if amount_input > 100000:
        st.error("⚠️ High Risk: This transaction is likely fraudulent.")
    else:
        st.success("✅ Low Risk: This transaction seems safe.")

# ---- Data Visualization Filters ----
st.sidebar.header("📊 Visualization Filters")
min_amount, max_amount = st.sidebar.slider("Transaction Amount Range (KES)", float(df["Amount (KES)"].min()), float(df["Amount (KES)"].max()), (1000.0, 100000.0))
month_filter = st.sidebar.multiselect("Month(s)", sorted(df["Transaction Month"].unique()), default=sorted(df["Transaction Month"].unique()))
type_filter = st.sidebar.multiselect("Transaction Type", df["Transaction Type"].unique(), default=df["Transaction Type"].unique())
channel_filter = st.sidebar.multiselect("Transaction Channel", df["Transaction Channel"].unique(), default=df["Transaction Channel"].unique())

# ---- Apply Visualization Filters ----
filtered_df = df[
    (df["Amount (KES)"] >= min_amount) &
    (df["Amount (KES)"] <= max_amount) &
    (df["Transaction Month"].isin(month_filter)) &
    (df["Transaction Type"].isin(type_filter)) &
    (df["Transaction Channel"].isin(channel_filter))
]

st.header("📋 Filtered Transactions")
st.write(filtered_df)

# ---- Line Graph by Day ----
st.header("📈 Transactions by Day")
daily_counts = filtered_df.groupby('Transaction Day').size()
st.line_chart(daily_counts)

# ---- Statistics ----
st.sidebar.subheader("📌 Statistics Summary")
st.sidebar.write("**Transaction Type Distribution**")
st.sidebar.write(filtered_df["Transaction Type"].value_counts())

st.sidebar.write("**Transaction Channel Distribution**")
st.sidebar.write(filtered_df["Transaction Channel"].value_counts())

# ---- Bar Charts ----
st.header("📊 Transaction Type Distribution")
st.bar_chart(filtered_df["Transaction Type"].value_counts())

st.header("📊 Transaction Channel Distribution")
st.bar_chart(filtered_df["Transaction Channel"].value_counts())

# ---- Footer ----
st.markdown("---")
st.markdown("""
**Created by James Ndungu**  
📧 Email: [jamesndungu.dev@gmail.com](mailto:jamesndungu.dev@gmail.com)  
📞 Phone: +254796593045  
🔗 GitHub: [James' GitHub](https://github.com/jimmie585)
""")
