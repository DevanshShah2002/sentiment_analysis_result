# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Load Data ---
st.title("📈 Pest Control Customer Review Analytics")

df = pd.read_csv("result.csv")

df['Date'] = pd.to_datetime(df['Date'])

# --- Sidebar Filters ---
customers = df['FirstName'].unique()
selected_customer = st.sidebar.selectbox("Select Customer", options=["All"] + list(customers))
filtered_df = df if selected_customer == "All" else df[df['FirstName'] == selected_customer]

# --- Helper Color Map ---
sentiment_colors = {"positive": "blue", "negative": "green", "neutral": "red"}

# ---------------------- PLOT 1: Customer Sentiment Trend Over Time ----------------------
st.subheader("1. 📊 Customer Sentiment Trend Over Time")

fig1 = px.line(
    filtered_df,
    x="Date",
    y="score",
    color="FirstName" if selected_customer == "All" else None,
    markers=True,
    title="Customer score Trend Over Time",
    hover_data=["Review", "sentiment", "suggestions"],
    color_discrete_sequence=px.colors.qualitative.Set1
)
st.plotly_chart(fig1, use_container_width=True)

# ---------------------- PLOT 2: Monthly Sentiment Summary ----------------------
st.subheader("2. 📆 Monthly Sentiment Summary")

monthly_summary = (
    filtered_df.groupby([pd.Grouper(key='Date', freq='ME'), 'sentiment'])
    .size().reset_index(name='Count')
)

fig2 = px.bar(
    monthly_summary,
    x="Date",
    y="Count",
    color="sentiment",
    color_discrete_map=sentiment_colors,
    barmode="group",
    title="Monthly Count of Each Sentiment Type"
)
st.plotly_chart(fig2, use_container_width=True)


# ---------------------- PLOT 3: Suggestions Frequency ----------------------
st.subheader("3. 💡 Suggestions Frequency")

suggestion_count = filtered_df["suggestions"].value_counts().reset_index()
suggestion_count.columns = ["suggestions", "count"]

fig3 = px.bar(
    suggestion_count,
    x="suggestions",
    y="count",
    color="suggestions",
    title="Frequency of Suggestions Given"
)
st.plotly_chart(fig3, use_container_width=True)


# ---------------------- PLOT 4: Rating Distribution ----------------------
st.subheader("4. ⭐ Rating Distribution")

fig4 = px.histogram(
    filtered_df,
    x="Rating",
    color="sentiment",
    nbins=10,
    color_discrete_map=sentiment_colors,
    title="Distribution of Ratings"
)
st.plotly_chart(fig4, use_container_width=True)

# ---------------------- PLOT 5: Sentiment vs Suggestions ----------------------
st.subheader("5. 🔗 Relation Between Sentiment and Suggestions")

sentiment_suggestion = (
    filtered_df.groupby(['sentiment', 'suggestions']).size().reset_index(name="count")
)

fig5 = px.bar(
    sentiment_suggestion,
    x="sentiment",
    y="count",
    color="suggestions",
    barmode="group",
    color_discrete_sequence=px.colors.qualitative.Plotly,
    title="How Sentiment Relates to Suggestions Given"
)
fig5.update_traces(marker_line_width=1, marker_line_color="black")
st.plotly_chart(fig5, use_container_width=True)

# ---------------------- Overall sentiment ----------------------
st.subheader("Overall sentiment")
summary= pd.read_csv('summary.csv')
st.dataframe(summary)