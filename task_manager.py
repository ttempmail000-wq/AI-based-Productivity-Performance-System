import pandas as pd
import os

FILE_NAME = "tasks.csv"

# ---------------- CREATE CSV ----------------
def initialize_file():

    if not os.path.exists(FILE_NAME):

        df = pd.DataFrame(columns=[
            "Task_Name",
            "Category",
            "Start_Date",
            "End_Date",
            "Start_Time",
            "End_Time",
            "Status"
        ])

        df.to_csv(FILE_NAME, index=False)

# ---------------- LOAD TASKS ----------------
def load_tasks():

    initialize_file()

    return pd.read_csv(FILE_NAME)

# ---------------- SAVE TASKS ----------------
def save_tasks(df):

    df.to_csv(FILE_NAME, index=False)

# ---------------- ADD TASK ----------------
def add_task(
    task_name,
    category,
    start_date,
    end_date,
    start_time,
    end_time
):

    df = load_tasks()

    new_task = {
        "Task_Name": task_name,
        "Category": category,
        "Start_Date": start_date,
        "End_Date": end_date,
        "Start_Time": start_time,
        "End_Time": end_time,
        "Status": "Pending"
    }

    df = pd.concat(
        [df, pd.DataFrame([new_task])],
        ignore_index=True
    )

    save_tasks(df)

# ---------------- UPDATE STATUS ----------------
def update_status(task_name, status):

    df = load_tasks()

    df.loc[
        df["Task_Name"] == task_name,
        "Status"
    ] = status

    save_tasks(df)

# ---------------- DELETE TASK ----------------
def delete_task(task_name):

    df = load_tasks()

    df = df[
        df["Task_Name"] != task_name
    ]

    save_tasks(df)

# ---------------- GET PENDING TASKS ----------------
def get_pending_tasks():

    df = load_tasks()

    return df[
        df["Status"] == "Pending"
    ]

# ---------------- ANALYTICS ----------------
def get_analytics():

    df = load_tasks()

    total_tasks = len(df)

    completed_tasks = len(
        df[df["Status"] == "Completed"]
    )

    pending_tasks = len(
        df[df["Status"] == "Pending"]
    )

    completion_percentage = (
        (completed_tasks / total_tasks) * 100
        if total_tasks > 0 else 0
    )

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "completion_percentage": completion_percentage
    }