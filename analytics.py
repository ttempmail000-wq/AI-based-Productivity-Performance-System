import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- ANALYTICS DASHBOARD ----------------
def show_analytics(df):

    st.subheader("Performance Analytics")

    if len(df) == 0:

        st.info("No task data available")

        return

    # ---------------- DATE CONVERSION ----------------
    try:

        df["Parsed_Date"] = pd.to_datetime(
            df["Start_Date"],
            format="%d/%m/%Y (%a)"
        )

    except:

        st.warning("Date format issue detected")

        return

    # ---------------- FILTER OPTION ----------------
    analysis_type = st.selectbox(
        "Select Analytics View",
        ["Daily", "Weekly", "Monthly"]
    )

    # ---------------- DAILY ----------------
    if analysis_type == "Daily":

        grouped_df = (
            df.groupby("Parsed_Date")
            .agg({
                "Task_Name": "count",
                "Status": lambda x:
                    (x == "Completed").sum()
            })
            .reset_index()
        )

        grouped_df.columns = [
            "Date",
            "Total_Tasks",
            "Completed_Tasks"
        ]

    # ---------------- WEEKLY ----------------
    elif analysis_type == "Weekly":

        df["Week"] = (
            df["Parsed_Date"]
            .dt.to_period("W")
            .astype(str)
        )

        grouped_df = (
            df.groupby("Week")
            .agg({
                "Task_Name": "count",
                "Status": lambda x:
                    (x == "Completed").sum()
            })
            .reset_index()
        )

        grouped_df.columns = [
            "Week",
            "Total_Tasks",
            "Completed_Tasks"
        ]

    # ---------------- MONTHLY ----------------
    else:

        df["Month"] = (
            df["Parsed_Date"]
            .dt.to_period("M")
            .astype(str)
        )

        grouped_df = (
            df.groupby("Month")
            .agg({
                "Task_Name": "count",
                "Status": lambda x:
                    (x == "Completed").sum()
            })
            .reset_index()
        )

        grouped_df.columns = [
            "Month",
            "Total_Tasks",
            "Completed_Tasks"
        ]

    # ---------------- COMPLETION % ----------------
    grouped_df["Completion_Percentage"] = (
        grouped_df["Completed_Tasks"]
        / grouped_df["Total_Tasks"]
    ) * 100

    # ---------------- DATASET DISPLAY ----------------
    st.markdown("### Dataset View")

    st.dataframe(
        grouped_df,
        use_container_width=True
    )

    # ---------------- LINE CHART ----------------
    st.markdown("### Productivity Trend")

    x_column = grouped_df.columns[0]

    fig1 = px.line(
        grouped_df,
        x=x_column,
        y="Completion_Percentage",
        markers=True,
        title=f"{analysis_type} Productivity Trend"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # ---------------- BAR CHART ----------------
    st.markdown("### Task Completion Analysis")

    fig2 = px.bar(
        grouped_df,
        x=x_column,
        y=[
            "Total_Tasks",
            "Completed_Tasks"
        ],
        barmode="group",
        title=f"{analysis_type} Task Analysis"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # ---------------- PIE CHART ----------------
    st.markdown("### Overall Status Distribution")

    status_counts = (
        df["Status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    fig3 = px.pie(
        status_counts,
        names="Status",
        values="Count",
        title="Task Status Distribution"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )