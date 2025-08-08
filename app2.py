import streamlit as st
import pandas as pd
import json
from datetime import datetime

products = pd.read_csv("combined_products_cleaned2.csv")
sales = pd.read_csv("sales.csv")
with open("customers.json", "r", encoding="utf-8") as f:
    customers = json.load(f)
customers_df = pd.DataFrame(customers)
with open("sales_items.json","r", encoding="utf-8") as k:
    sales1= json.load(k)
sales1_df = pd.DataFrame(sales1)

st.title("Dashboard System")

plot_choice = st.sidebar.radio("Choice:", ["BarPlot", "LinePlot", "AreaPlot", "ScatterPlot"])

if plot_choice == "BarPlot":
    st.header("BarPlot to Visualise Total Sales by Month")

    sales["date"] = pd.to_datetime(sales["date"])
    df_grouped = sales.groupby(pd.Grouper(key="date", freq="M"))["amount"].sum()

    st.bar_chart(df_grouped, x_label="Month", y_label="Revenue")
