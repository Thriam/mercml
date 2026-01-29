import streamlit as st
import requests
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("🏡 Real Estate Agent Dashboard")

# Load DB
def load_data():
    conn = sqlite3.connect("housing.db")
    df = pd.read_sql_query("SELECT * FROM predictions", conn)
    conn.close()
    # Ensure numeric columns are properly typed
    numeric_cols = ["Square_Footage","Bedrooms","Bathrooms","Age","Garage_Spaces","Lot_Size",
                    "Floors","Neighborhood_Rating","Condition","School_Rating","Has_Pool",
                    "Renovated","Distance_To_Center_KM","Days_On_Market","Predicted_Price","Sold_Within_Week"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    return df

df = load_data()

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Comparisons", "Trends", "Records", "New Entry"])

# -------------------------------
# Tab 1: Overview
# -------------------------------
with tab1:
    st.subheader("📌 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Price", f"${df['Predicted_Price'].mean():,.0f}")
    col2.metric("Avg Days on Market", f"{df['Days_On_Market'].mean():.1f}")
    col3.metric("% Sold in Week", f"{(df['Sold_Within_Week'].mean()*100):.1f}%")
    col4.metric("Avg Sq Ft", f"{df['Square_Footage'].mean():.0f}")

# -------------------------------
# Tab 2: Comparisons
# -------------------------------
with tab2:
    st.subheader("📊 Price vs Square Footage")
    fig, ax = plt.subplots()
    sns.scatterplot(x="Square_Footage", y="Predicted_Price", hue="Sold_Within_Week", data=df, ax=ax)
    st.pyplot(fig)

    st.subheader("📊 Price vs Lot Size")
    fig, ax = plt.subplots()
    sns.scatterplot(x="Lot_Size", y="Predicted_Price", hue="Neighborhood_Rating", data=df, ax=ax)
    st.pyplot(fig)

    st.subheader("📊 Days on Market vs Neighborhood Rating")
    fig, ax = plt.subplots()
    sns.boxplot(x="Neighborhood_Rating", y="Days_On_Market", data=df, ax=ax)
    st.pyplot(fig)

    st.subheader("📊 Condition vs Sold Within Week")
    fig, ax = plt.subplots()
    sns.countplot(x="Condition", hue="Sold_Within_Week", data=df, ax=ax)
    st.pyplot(fig)

# -------------------------------
# Tab 3: Trends
# -------------------------------
with tab3:
    st.subheader("📈 Price vs Distance to Center")
    fig, ax = plt.subplots()
    sns.lineplot(x="Distance_To_Center_KM", y="Predicted_Price", data=df, ax=ax)
    st.pyplot(fig)

    st.subheader("📈 Days on Market vs Age of House")
    fig, ax = plt.subplots()
    sns.lineplot(x="Age", y="Days_On_Market", data=df, ax=ax)
    st.pyplot(fig)

# -------------------------------
# Tab 4: Records
# -------------------------------
with tab4:
    st.subheader("📋 Saved Predictions")
    st.dataframe(df)

    record_id = st.selectbox("Select Record ID to Update/Delete", df["id"].unique())
    if record_id:
        record = df[df["id"] == record_id].iloc[0]
        updated_entry = {}
        for col in ["Square_Footage","Bedrooms","Bathrooms","Age","Garage_Spaces","Lot_Size",
                    "Floors","Neighborhood_Rating","Condition","School_Rating","Has_Pool",
                    "Renovated","Location_Type","Distance_To_Center_KM","Days_On_Market"]:
            updated_entry[col] = st.text_input(col, value=record[col])

        if st.button("Update Record"):
            response = requests.put(f"http://127.0.0.1:5000/update/{record_id}", json=updated_entry)
            st.success(response.json()["message"])

        if st.button("Delete Record"):
            response = requests.delete(f"http://127.0.0.1:5000/delete/{record_id}")
            st.success(response.json()["message"])

# -------------------------------
# Tab 5: New Entry
# -------------------------------
with tab5:
    st.subheader("➕ Add New Entry")

    new_entry = {}
    for col in ["Square_Footage","Bedrooms","Bathrooms","Age","Garage_Spaces","Lot_Size",
                "Floors","Neighborhood_Rating","Condition","School_Rating","Has_Pool",
                "Renovated","Location_Type","Distance_To_Center_KM","Days_On_Market"]:
        if col == "Location_Type":
            new_entry[col] = st.selectbox(col, ["Suburban","Urban","Rural"])
        elif col in ["Has_Pool","Renovated"]:
            new_entry[col] = st.selectbox(col, [0,1])
        else:
            new_entry[col] = st.number_input(col)

    if st.button("Predict & Save"):
        response = requests.post("http://127.0.0.1:5000/predict", json=new_entry)
        result = response.json()
        st.success(f"Predicted Price: ${result['Predicted_Price']:.2f}")
        st.info(f"Sold Within Week: {'Yes' if result['Sold_Within_Week']==1 else 'No'}")

        # Refresh data after saving
        df = load_data()
        st.dataframe(df)
