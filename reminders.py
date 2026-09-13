import streamlit as st
from datetime import datetime

# ---------------- REMINDER SYSTEM ----------------
def show_reminders(df):

    st.subheader("⏰ Live Session Reminders")

    if len(df) == 0:
        st.info("No scheduled sessions available.")
        return

    now = datetime.now()

    active_found = False

    # ---------------- CHECK ALL TASKS ----------------
    for _, row in df.iterrows():

        try:

            if row["Status"] == "Completed":
                continue

            task_name = row["Task_Name"]

            # Convert time strings into datetime objects
            start_time = datetime.strptime(
                row["Start_Time"],
                "%I:%M %p"
            )

            end_time = datetime.strptime(
                row["End_Time"],
                "%I:%M %p"
            )

            current_time = datetime.strptime(
                now.strftime("%I:%M %p"),
                "%I:%M %p"
            )

            # ---------------- SESSION STARTING SOON ----------------
            minutes_until_start = (
                start_time - current_time
            ).total_seconds() / 60

            if 0 <= minutes_until_start <= 10:

                st.warning(
                    f"📢 '{task_name}' starts in "
                    f"{int(minutes_until_start)} minutes!"
                )

                active_found = True

            # ---------------- ACTIVE SESSION ----------------
            if start_time <= current_time <= end_time:

                remaining = (
                    end_time - current_time
                )

                remaining_seconds = int(
                    remaining.total_seconds()
                )

                hours = remaining_seconds // 3600
                minutes = (
                    (remaining_seconds % 3600) // 60
                )

                seconds = remaining_seconds % 60

                st.success(
                    f"🔥 LIVE: {task_name}"
                )

                st.info(
                    f"⏳ Remaining Time: "
                    f"{hours}h {minutes}m {seconds}s"
                )

                active_found = True

            # ---------------- SESSION ENDING SOON ----------------
            minutes_until_end = (
                end_time - current_time
            ).total_seconds() / 60

            if 0 <= minutes_until_end <= 10:

                st.info(
                    f"⌛ '{task_name}' ends in "
                    f"{int(minutes_until_end)} minutes."
                )

                active_found = True

        except Exception as e:

            st.warning(
                f"Invalid time format in task: {task_name}"
            )

    # ---------------- NO ACTIVE REMINDER ----------------
    if active_found == False:

        st.info(
            "No active reminders currently."
        )