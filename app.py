import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Load datasets
products = pd.read_csv("combined_products_cleaned2.csv")
sales = pd.read_csv("sales.csv")
with open("customers.json", "r", encoding="utf-8") as f:
    customers = json.load(f)
customers_df = pd.DataFrame(customers)

st.title("Amazon Filter System")

dataset_choice = st.sidebar.radio("Choose dataset to explore:", ["Products", "Customers", "Sales", "Sales Items"])

if dataset_choice == "Products":
    st.header("Products Filter")

    m_cat = products["main_category"].dropna().unique()
    s_cat= products["sub_category"].dropna().unique()

    

elif dataset_choice == "Customers":
    st.header("Customers Filter")

    gender = st.selectbox("Gender", ["All", "Male (0)", "Female (1)"])
    age_range = st.slider("Age Range", 18, 70, (18, 70))

    filtered = customers_df.copy()
    if gender == "Male (0)":
        filtered = filtered[filtered["gender"] == 0]
    elif gender == "Female (1)":
        filtered = filtered[filtered["gender"] == 1]

    filtered = filtered[(filtered["age"] >= age_range[0]) & (filtered["age"] <= age_range[1])]
    st.dataframe(filtered)

elif dataset_choice == "Sales":
    st.header("Sales Filter")

    sales["date"] = pd.to_datetime(sales["date"])
    min_date = sales["date"].min()
    max_date = sales["date"].max()

    date_range = st.date_input("Date Range", (min_date, max_date))
    amount_range = st.slider("Amount Range", 0.0, float(sales["amount"].max()), (0.0, float(sales["amount"].max())))
    customer_id = st.text_input("Search by Customer ID (optional)")

    filtered = sales.copy()
    filtered = filtered[(filtered["date"] >= pd.to_datetime(date_range[0])) & (filtered["date"] <= pd.to_datetime(date_range[1]))]
    filtered = filtered[(filtered["amount"] >= amount_range[0]) & (filtered["amount"] <= amount_range[1])]

    if customer_id:
        filtered = filtered[filtered["customer_id"] == int(customer_id)]

    st.dataframe(filtered)

elif dataset_choice == "Sales Items":
    st.header("Product Sales Lookup")
    product_id = st.text_input("Enter Product ID to find all sales")

    if product_id:
        results = sales[sales["product_ids"].str.contains(product_id)]
        st.write(f"Found {len(results)} instances of product ID {product_id} in sales")
        st.dataframe(results)


