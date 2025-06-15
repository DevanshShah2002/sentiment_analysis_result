import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(layout="wide")
# --- Load Data ---
st.title("📈 Pest Control Customer Review Analytics")

df = pd.read_csv("result.csv")
df['Date'] = pd.to_datetime(df['Date'])

# --- Inline Customer Filter (no sidebar) ---
customers = df['FirstName'].unique()
selected_customer = st.selectbox("Select Customer", options=["All"] + list(customers))
filtered_df = df if selected_customer == "All" else df[df['FirstName'] == selected_customer]

# --- Helper Color Map ---
sentiment_colors = {"positive": "blue", "negative": "green", "neutral": "red"}

# --- Create 2 columns for side-by-side graphs ---
col1, col2 = st.columns(2)

with col1:
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

with col2:
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

# You can add other plots below or arrange more columns as needed.

# --- Overall sentiment summary ---
st.subheader("Overall sentiment")
summary = pd.read_csv('summary.csv')
summary = summary if selected_customer == "All" else summary[summary['FirstName'] == selected_customer]

fig = go.Figure(data=[go.Table(
    header=dict(
        values=list(summary.columns),
        fill_color='white',
        align='left',
        font=dict(color='black', size=14),
        height=30
    ),
    cells=dict(
        values=[summary[col] for col in summary.columns],
        fill_color='white',
        align='left',
        font=dict(color='black', size=11),
        height=25,
        # Fix column widths (in pixels)
        # Note: this sets widths relative to whole table width, so adjust accordingly
        # You can try 'columnwidth' attribute but not officially supported
    )
)])
fig.update_layout(height=1000)
# Display table in Streamlit
st.plotly_chart(fig, use_container_width=True)
