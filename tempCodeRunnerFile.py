import streamlit as st
import pandas as pd
from datetime import date
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI-Based Productivity System",
    layout="wide"
)

st.title("AI-Based Productivity & Performance System")

# ---------------- CSV FILE SETUP ----------------
FILE_NAME = "tasks.csv"

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=[
        "Task_ID",
        "Task_Name",
        "Category",
        "Priority",
        "Start_Date",
        "Due_Date",
        "Estimated_Time",
        "Completion_Status",
        "Progress_Percentage",
        "Delay_Status"
    ])
    df.to_csv(FILE_NAME, index=False)

# ---------------- LOAD DATA ----------------
df = pd.read_csv(FILE_NAME)

# ---------------- SIDEBAR ----------------
st.sidebar.header("Add New Task")

task_name = st.sidebar.text_input("Task Name")

category = st.sidebar.selectbox(
    "Category",
    ["Study", "Health", "Personal", "Work"]
)

priority = st.sidebar.selectbox(
    "Priority",
    ["Low", "Medium", "High"]
)

start_date = st.sidebar.date_input(
    "Start Date",
    date.today()
)

due_date = st.sidebar.date_input(
    "Due Date",
    date.today()
)

estimated_time = st.sidebar.number_input(
    "Estimated Time (Minutes)",
    min_value=1,
    step=1
)

# ---------------- ADD TASK ----------------
if st.sidebar.button("Add Task"):

    task_id = len(df) + 1

    new_task = {
        "Task_ID": task_id,
        "Task_Name": task_name,
        "Category": category,
        "Priority": priority,
        "Start_Date": start_date,
        "Due_Date": due_date,
        "Estimated_Time": estimated_time,
        "Completion_Status": "Pending",
        "Progress_Percentage": 0,
        "Delay_Status": "On-Time"
    }

    df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)

    df.to_csv(FILE_NAME, index=False)

    st.success("Task Added Successfully")

# ---------------- TASK TABLE ----------------
st.subheader("Task Management Dashboard")

if len(df) > 0:

    completed = st.multiselect(
        "Mark Completed Tasks",
        df["Task_Name"]
    )

    df["Completion_Status"] = df["Task_Name"].apply(
        lambda x: "Completed" if x in completed else "Pending"
    )

    df["Progress_Percentage"] = df["Completion_Status"].apply(
        lambda x: 100 if x == "Completed" else 0
    )

    today = pd.to_datetime(date.today())

    df["Delay_Status"] = df.apply(
        lambda row: "Delayed"
        if (
            pd.to_datetime(row["Due_Date"]) < today
            and row["Completion_Status"] == "Pending"
        )
        else "On-Time",
        axis=1
    )

    df.to_csv(FILE_NAME, index=False)

    st.dataframe(df)

    # ---------------- ANALYTICS ----------------
    total_tasks = len(df)
    completed_tasks = len(df[df["Completion_Status"] == "Completed"])
    delayed_tasks = len(df[df["Delay_Status"] == "Delayed"])

    completion_percentage = (
        (completed_tasks / total_tasks) * 100
        if total_tasks > 0 else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tasks", total_tasks)
    col2.metric("Completed Tasks", completed_tasks)
    col3.metric("Completion %", f"{completion_percentage:.1f}%")

    st.subheader("Delayed Tasks")

    st.write(delayed_tasks)

    # ---------------- AI FEEDBACK ----------------
    st.subheader("AI-Based Feedback")

    if completion_percentage >= 80:
        st.success("Excellent productivity and consistency.")
    elif completion_percentage >= 50:
        st.warning("Good progress. Try reducing delayed tasks.")
    else:
        st.error("Low productivity detected. Improve task consistency.")

else:
    st.info("No tasks added yet.")