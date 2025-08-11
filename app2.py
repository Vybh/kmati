import streamlit as st
import pandas as pd
import json
from datetime import datetime
import altair as alt

products = pd.read_csv("combined_products_cleaned2.csv")
sales = pd.read_csv("sales.csv")
with open("customers.json", "r", encoding="utf-8") as f:
    customers = json.load(f)
customers_df = pd.DataFrame(customers)
with open("sales_items.json","r", encoding="utf-8") as k:
    sales1 = json.load(k)
sales1_df = pd.DataFrame(sales1)

sales["date"] = pd.to_datetime(sales["date"])

st.title("Dashboard System")

plot_choice = st.sidebar.radio("Choice:", ["BarPlot", "LinePlot", "AreaPlot", "ScatterPlot"])

if plot_choice == "BarPlot":
    st.header("BarPlot to Visualise Total Sales by Month")
    df_grouped = sales.groupby(pd.Grouper(key="date", freq="M"))["amount"].sum().reset_index()
    df_grouped["Month"] = df_grouped["date"].dt.strftime("%b %Y")
    st.bar_chart(df_grouped.set_index("Month")["amount"], x_label="Month", y_label="Revenue")

elif plot_choice == "LinePlot":
    st.header("Quarterly Sales Trends for Top 5 Categories")
    merged = sales1_df.merge(sales, on="sale_id").merge(products, on="product_id")
    top_categories = merged.groupby("main_category")["amount"].sum().nlargest(5).index
    filtered = merged[merged["main_category"].isin(top_categories)]
    filtered["Quarter"] = filtered["date"].dt.to_period("Q").dt.to_timestamp()
    quarterly_sales = filtered.groupby(["Quarter", "main_category"])["amount"].sum().reset_index()
    chart = alt.Chart(quarterly_sales).mark_line(point=True).encode(
        x="Quarter:T",
        y="amount:Q",
        color="main_category:N",
        tooltip=["Quarter", "main_category", "amount"]
    ).properties(width=700, height=400)
    st.altair_chart(chart, use_container_width=True)

elif plot_choice == "AreaPlot":
    st.header("Quarterly Spending by Gender")
    merged_gender = sales.merge(customers_df, on="customer_id")
    merged_gender["Quarter"] = merged_gender["date"].dt.to_period("Q").dt.to_timestamp()
    quarterly_gender = merged_gender.groupby(["Quarter", "gender"])["amount"].sum().reset_index()
    chart = alt.Chart(quarterly_gender).mark_area(opacity=0.6).encode(
        x="Quarter:T",
        y="amount:Q",
        color="gender:N",
        tooltip=["Quarter", "gender", "amount"]
    ).properties(width=700, height=400)
    st.altair_chart(chart, use_container_width=True)

elif plot_choice == "ScatterPlot":
    st.header("Price vs Rating by Category")
    products_clean = products.dropna(subset=["rating"])
    chart = alt.Chart(products_clean).mark_circle(size=60, opacity=0.6).encode(
        x="price:Q",
        y="rating:Q",
        color="main_category:N",
        tooltip=["product_name", "price", "rating", "main_category"]
    ).properties(width=700, height=400)
    st.altair_chart(chart, use_container_width=True)
