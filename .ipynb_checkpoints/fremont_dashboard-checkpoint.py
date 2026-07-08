import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

st.title("Fremont Bridge Bicycle Counter Dashboard")

st.write(
    "This interactive dashboard presents the main visual findings from the Fremont Bridge Bicycle Counter analysis."
)

df = pd.read_csv("Fremont_Bridge_Bicycle_Counter.csv")

df = df.dropna()
df["Date"] = pd.to_datetime(df["Date"])

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month_name()
df["Month Number"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day_name()
df["Day Number"] = df["Date"].dt.dayofweek
df["Hour"] = df["Date"].dt.hour

st.subheader("Key Metrics")

total_cyclists = int(df["Fremont Bridge Sidewalks, south of N 34th St Total"].sum())

busiest_month = (
    df.groupby("Month")["Fremont Bridge Sidewalks, south of N 34th St Total"]
    .sum()
    .idxmax()
)

busiest_day = (
    df.groupby("Day")["Fremont Bridge Sidewalks, south of N 34th St Total"]
    .sum()
    .idxmax()
)

busiest_hour = (
    df.groupby("Hour")["Fremont Bridge Sidewalks, south of N 34th St Total"]
    .sum()
    .idxmax()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Cyclists", total_cyclists)
col2.metric("Busiest Month", busiest_month)
col3.metric("Busiest Day", busiest_day)
col4.metric("Busiest Hour", str(busiest_hour) + ":00")

st.subheader("Select a Visualisation")

chart_choice = st.selectbox(
    "Choose a visualisation",
    [
        "Cyclist Traffic by Year",
        "Cyclist Traffic by Month",
        "Cyclist Traffic by Day of the Week",
        "Cyclist Traffic by Hour",
        "Cyclist Traffic by Sidewalk"
    ]
)

if chart_choice == "Cyclist Traffic by Year":
    st.subheader("How Has Cyclist Traffic Changed Over Time?")

    st.info(
        "Note: The dataset begins in October 2012 and currently contains only partial-year data for 2025. "
        "As a result, the total cyclist counts for 2012 and 2025 are lower than those of the complete years "
        "and should be interpreted with caution when making annual comparisons."
    )

    yearly_counts = (
        df.groupby("Year")["Fremont Bridge Sidewalks, south of N 34th St Total"]
        .sum()
        / 1000
    )

    year_colors = []

    for year in yearly_counts.index:
        if year == yearly_counts.idxmax():
            year_colors.append("gold")
        elif year in [2020, 2021]:
            year_colors.append("red")
        elif year in [2012, 2025]:
            year_colors.append("mediumpurple")
        else:
            year_colors.append("steelblue")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        yearly_counts.index,
        yearly_counts.values,
        color="steelblue",
        linewidth=2
    )

    ax.scatter(
        yearly_counts.index,
        yearly_counts.values,
        color=year_colors,
        s=80,
        zorder=5
    )

    ax.set_title("Total Cyclists by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Cyclists (thousands)")
    ax.set_xticks(yearly_counts.index)
    ax.grid(True)

    legend_elements = [
        Patch(facecolor="gold", label="Highest Annual Traffic"),
        Patch(facecolor="red", label="COVID-19 Decline"),
        Patch(facecolor="mediumpurple", label="Partial-Year Data"),
        Patch(facecolor="steelblue", label="Other Years")
    ]

    ax.legend(handles=legend_elements)

    plt.tight_layout()

    st.pyplot(fig)

    st.info(
        "Annual cyclist traffic increased steadily from 2012 to 2019 before declining sharply in 2020 and 2021. "
        "This decline coincides with the COVID-19 pandemic, when public health restrictions and changes to commuting patterns likely reduced cyclist traffic. "
        "From 2022 onwards, cyclist numbers showed a gradual recovery, although they had not yet returned to the 2019 peak."
    )

elif chart_choice == "Cyclist Traffic by Month":
    st.subheader("Which Months Record the Highest Cyclist Traffic?")

    monthly_counts = (
        df.groupby(["Month Number", "Month"])
        ["Fremont Bridge Sidewalks, south of N 34th St Total"]
        .sum()
        .reset_index()
        .sort_values("Month Number")
    )

    monthly_counts["Total (thousands)"] = (
        monthly_counts["Fremont Bridge Sidewalks, south of N 34th St Total"] / 1000
    )

    month_colors = []

    monthly_counts_sorted = monthly_counts.sort_values(
        "Fremont Bridge Sidewalks, south of N 34th St Total",
        ascending=False
    )

    top_month = monthly_counts_sorted.iloc[0]["Month"]
    second_third_months = monthly_counts_sorted.iloc[1:3]["Month"].tolist()

    for month in monthly_counts["Month"]:
        if month == top_month:
            month_colors.append("gold")
        elif month in second_third_months:
            month_colors.append("orange")
        else:
            month_colors.append("steelblue")

    fig, ax = plt.subplots(figsize=(10, 5))

    monthly_counts.plot(
        x="Month",
        y="Total (thousands)",
        kind="bar",
        color=month_colors,
        ax=ax
    )

    ax.set_title("Total Cyclists by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Cyclists (thousands)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y")

    legend_elements = [
        Patch(facecolor="gold", label="Highest Month"),
        Patch(facecolor="orange", label="2nd and 3rd Highest Months"),
        Patch(facecolor="steelblue", label="Other Months")
    ]

    ax.legend(handles=legend_elements)

    plt.tight_layout()

    st.pyplot(fig)

    st.info(
        "Cyclist traffic was highest during the summer months, particularly July and August, while the lowest levels were recorded during the winter months. "
        "This suggests that seasonal factors, such as warmer weather and longer daylight hours, may encourage increased cycling activity."
    )

elif chart_choice == "Cyclist Traffic by Day of the Week":
    st.subheader("Which Days of the Week Are the Busiest?")

    daily_counts = (
        df.groupby(["Day Number", "Day"])
        ["Fremont Bridge Sidewalks, south of N 34th St Total"]
        .sum()
        .reset_index()
        .sort_values("Day Number")
    )

    daily_counts["Total (thousands)"] = (
        daily_counts["Fremont Bridge Sidewalks, south of N 34th St Total"] / 1000
    )

    day_colors = []

    daily_counts_sorted = daily_counts.sort_values(
        "Fremont Bridge Sidewalks, south of N 34th St Total",
        ascending=False
    )

    top_day = daily_counts_sorted.iloc[0]["Day"]
    second_third_days = daily_counts_sorted.iloc[1:3]["Day"].tolist()

    for day in daily_counts["Day"]:
        if day == top_day:
            day_colors.append("gold")
        elif day in second_third_days:
            day_colors.append("orange")
        else:
            day_colors.append("steelblue")

    fig, ax = plt.subplots(figsize=(10, 5))

    daily_counts.plot(
        x="Day",
        y="Total (thousands)",
        kind="bar",
        color=day_colors,
        ax=ax
    )

    ax.set_title("Total Cyclists by Day of the Week")
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Total Cyclists (thousands)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y")

    legend_elements = [
        Patch(facecolor="gold", label="Highest Day"),
        Patch(facecolor="orange", label="2nd and 3rd Highest Days"),
        Patch(facecolor="steelblue", label="Other Days")
    ]

    ax.legend(handles=legend_elements)

    plt.tight_layout()

    st.pyplot(fig)

    st.info(
        "Weekdays consistently recorded higher cyclist volumes than weekends, with Tuesday, Wednesday and Thursday being the busiest days. "
        "This pattern suggests that the bridge is used heavily for commuting, although the dataset does not identify the specific reasons for these travel patterns."
    )

elif chart_choice == "Cyclist Traffic by Hour":
    st.subheader("How Does Cyclist Traffic Change Throughout the Day?")

    hourly_counts = (
        df.groupby("Hour")["Fremont Bridge Sidewalks, south of N 34th St Total"]
        .sum()
        / 1000
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        hourly_counts.index,
        hourly_counts.values,
        color="steelblue",
        marker="o",
        label="Hourly Traffic"
    )

    ax.scatter(
        17,
        hourly_counts.loc[17],
        color="gold",
        s=120,
        zorder=5,
        label="Highest Peak (5 PM)"
    )

    ax.scatter(
        8,
        hourly_counts.loc[8],
        color="orange",
        s=120,
        zorder=5,
        label="Morning Peak (8 AM)"
    )

    ax.set_title("Total Cyclists by Hour")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Total Cyclists (thousands)")
    ax.set_xticks(hourly_counts.index)
    ax.grid(True)

    ax.legend()

    plt.tight_layout()

    st.pyplot(fig)

    st.info(
        "Two distinct peaks in cyclist activity were observed throughout the day, occurring at approximately 8:00 AM and 5:00 PM, with the evening peak being the highest. "
        "These times align with typical morning and evening commuting periods, indicating that commuter travel is a major contributor to overall cyclist traffic."
    )

elif chart_choice == "Cyclist Traffic by Sidewalk":
    st.subheader("Which Sidewalk Records More Cyclist Traffic?")

    sidewalk_counts = (
        df[[
            "Fremont Bridge Sidewalks, south of N 34th St Cyclist West Sidewalk",
            "Fremont Bridge Sidewalks, south of N 34th St Cyclist East Sidewalk"
        ]]
        .sum()
        / 1000
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    sidewalk_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Total Cyclists by Sidewalk")
    ax.set_xlabel("Sidewalk")
    ax.set_ylabel("Total Cyclists (thousands)")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["West", "East"], rotation=0)
    ax.grid(axis="y")

    plt.tight_layout()

    st.pyplot(fig)

    st.info(
        "The East sidewalk recorded a higher total cyclist volume than the West sidewalk across the dataset. "
        "This indicates an imbalance in cyclist usage between the two pathways, although the dataset does not provide sufficient information to explain the underlying cause."
    )