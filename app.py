import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import os
from streamlit_autorefresh import st_autorefresh

# ---------------- IMPORT MODULES ----------------
from analytics import show_analytics
from feedback import generate_feedback
from reminders import show_reminders

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Productivity System",
    layout="wide"
)

# ---------------- AUTO REFRESH ----------------
st_autorefresh(interval=1000, key="refresh")

# ---------------- TITLE ----------------
st.title("AI-Based Productivity & Performance System")

# ---------------- CSV FILE ----------------
FILE_NAME = "tasks.csv"

if not os.path.exists(FILE_NAME):
    df_init = pd.DataFrame(columns=[
        "Task_Name",
        "Category",
        "Start_Date",
        "End_Date",
        "Start_Time",
        "End_Time",
        "Status"
    ])
    df_init.to_csv(FILE_NAME, index=False)

# ---------------- LOAD DATA ----------------
df = pd.read_csv(FILE_NAME)

# ---------------- SESSION STATE INIT ----------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "focus_mode" not in st.session_state:
    st.session_state.focus_mode = False

# Sync df → session_state (safe conversion)
if len(st.session_state.tasks) == 0 and len(df) > 0:
    for _, row in df.iterrows():
        try:
            st.session_state.tasks.append({
                "Task": row["Task_Name"],
                "Category": row["Category"],
                "Start": datetime.now(),
                "End": datetime.now(),
                "Completed": False
            })
        except:
            pass

now = datetime.now()

# ---------------- SIDEBAR ----------------
st.sidebar.header("Schedule New Session")

task_name = st.sidebar.text_input("Task Name")

category = st.sidebar.selectbox(
    "Category",
    ["Study", "Work", "Health", "Personal", "other"]
)

start_date = st.sidebar.date_input("Start Date", date.today())
end_date = st.sidebar.date_input("End Date", date.today())

start_time = st.sidebar.text_input("Start Time (Example: 9:30 AM)", "9:00 AM")
end_time = st.sidebar.text_input("End Time (Example: 11:30 AM)", "10:00 AM")

# ---------------- ADD SESSION ----------------
if st.sidebar.button("Add Session"):

    new_task = {
        "Task_Name": task_name,
        "Category": category,
        "Start_Date": start_date.strftime("%d/%m/%Y (%a)"),
        "End_Date": end_date.strftime("%d/%m/%Y (%a)"),
        "Start_Time": start_time,
        "End_Time": end_time,
        "Status": "Pending"
    }

    df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)

    st.sidebar.success("Session Added Successfully")
    st.rerun()

# ---------------- DISPLAY TASKS ----------------
st.subheader("Scheduled Sessions")

if len(df) > 0:
    st.dataframe(df, use_container_width=True)
else:
    st.info("No Sessions Added Yet")

# ---------------- FOCUS MODE ----------------

st.subheader("🎯 Focus Mode")

# ENTER BUTTON
if not st.session_state.get("focus_mode", False):

    if st.button("🎯 Enter Focus Mode"):
        st.session_state.focus_mode = True
        st.rerun()

# FOCUS MODE ACTIVE
if st.session_state.get("focus_mode", False):

    st.markdown("---")

    current_time = datetime.now()

    active_session = None

    for _, row in df.iterrows():

        if row["Status"] == "Completed":
            continue

        try:

            start_datetime = datetime.combine(
                datetime.today(),
                datetime.strptime(
                    row["Start_Time"],
                    "%I:%M %p"
                ).time()
            )

            end_datetime = datetime.combine(
                datetime.today(),
                datetime.strptime(
                    row["End_Time"],
                    "%I:%M %p"
                ).time()
            )

            # ACTIVE SESSION
            if start_datetime <= current_time <= end_datetime:
                active_session = row
                break

        except:
            pass

    # ---------------- ACTIVE SESSION ----------------
    if active_session is not None:

        st.success("🔥 LIVE SESSION")

        st.markdown(
            f"## {active_session['Task_Name']}"
        )

        st.write(
            f"Category: {active_session['Category']}"
        )

        st.write(
            f"Time: "
            f"{active_session['Start_Time']} → "
            f"{active_session['End_Time']}"
        )

        # LIVE CLOCK
        st.markdown(
            f"### Current Time: "
            f"{current_time.strftime('%I:%M:%S %p')}"
        )

        # REMAINING TIME
        remaining = (
            end_datetime - current_time
        )

        total_seconds = int(
            remaining.total_seconds()
        )

        hours = total_seconds // 3600
        minutes = (
            (total_seconds % 3600) // 60
        )

        seconds = total_seconds % 60

        st.info(
            f"⏳ Remaining Time: "
            f"{hours}h {minutes}m {seconds}s"
        )

    else:

        st.warning(
            "No active session currently."
        )

    # EXIT BUTTON
    if st.button("❌ Exit Focus Mode"):
        st.session_state.focus_mode = False
        st.rerun()
# ---------------- MANAGE SESSIONS ----------------
st.header("⚙ Manage Scheduled Sessions")

if len(df) > 0:

    task_options = [
        f"{row['Task_Name']} ({row['Start_Time']} → {row['End_Time']})"
        for _, row in df.iterrows()
    ]

    selected_task = st.selectbox("Select Session", task_options)
    selected_index = task_options.index(selected_task)

    task = df.iloc[selected_index]

    st.markdown("---")

    col1, col2, col3 = st.columns([6, 2, 2])

    with col1:

        st.markdown(f"## {task['Task_Name']}")
        st.write(f"**Category:** {task['Category']}")
        st.write(f"**Date:** {task['Start_Date']} → {task['End_Date']}")
        st.write(f"**Time:** {task['Start_Time']} → {task['End_Time']}")

        if task["Status"] == "Completed":
            st.success("Completed")
        else:
            st.warning("Pending")

    with col2:
        if st.button("✏ Edit Session"):
            st.session_state.edit_index = selected_index

    with col3:
        if st.button("🟢 Mark Completed"):
            df.loc[selected_index, "Status"] = "Completed"
            df.to_csv(FILE_NAME, index=False)
            st.success("Marked Completed")
            st.rerun()

        if st.button("🗑 Delete Session"):
            df = df.drop(df.index[selected_index]).reset_index(drop=True)
            df.to_csv(FILE_NAME, index=False)
            st.success("Session Deleted")
            st.rerun()

else:
    st.info("No sessions available.")

# ---------------- EDIT SECTION ----------------

if "edit_index" in st.session_state:

    idx = st.session_state.edit_index

    edit_task = df.iloc[idx]

    st.subheader("✏ Edit Session")

    new_name = st.text_input(
        "Task Name",
        value=edit_task["Task_Name"]
    )

    category_list = [
        "Study",
        "Fitness",
        "Work",
        "Personal",
        "Other"
    ]

    current_category = edit_task["Category"]

    if current_category not in category_list:
        current_category = "Other"

    new_category = st.selectbox(
        "Category",
        category_list,
        index=category_list.index(current_category)
    )

    # DATE
    new_date = st.date_input(
        "Session Date",
        value=datetime.strptime(
            edit_task["Start_Date"].split(" ")[0],
            "%d/%m/%Y"
        ).date()
    )

    # START TIME
    new_start_time = st.time_input(
        "Start Time",
        value=datetime.strptime(
            edit_task["Start_Time"].replace(": ", ":").strip(),
            "%I:%M %p"
        ).time()
    )

    # END TIME
    new_end_time = st.time_input(
        "End Time",
        value=datetime.strptime(
            edit_task["End_Time"].replace(": ", ":").strip(),
            "%I:%M %p"
        ).time()
    )

    # SAVE BUTTON
    if st.button("Save Changes"):

        df.loc[idx, "Task_Name"] = new_name
        df.loc[idx, "Category"] = new_category
        df.loc[idx, "Start_Date"] = new_date.strftime("%d/%m/%Y (%a)")
        df.loc[idx, "End_Date"] = new_date.strftime("%d/%m/%Y (%a)")
        df.loc[idx, "Start_Time"] = new_start_time.strftime("%I:%M %p")
        df.loc[idx, "End_Time"] = new_end_time.strftime("%I:%M %p")

        df.to_csv(FILE_NAME, index=False)

        st.success("Session Updated Successfully")

        del st.session_state.edit_index

        st.rerun()
# else:
#     st.info("No sessions available.")

# ---------------- REMINDERS ----------------
show_reminders(df)

# ---------------- ANALYTICS ----------------
show_analytics(df)

# ---------------- AI FEEDBACK ----------------
generate_feedback(df)