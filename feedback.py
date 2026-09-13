import streamlit as st

# ---------------- AI FEEDBACK SYSTEM ----------------
def generate_feedback(df):

    st.subheader("AI-Based Feedback System")

    if len(df) == 0:

        st.info("No task data available for feedback.")

        return

    # ---------------- BASIC COUNTS ----------------
    total_tasks = len(df)

    completed_tasks = len(
        df[df["Status"] == "Completed"]
    )

    pending_tasks = len(
        df[df["Status"] == "Pending"]
    )

    # ---------------- COMPLETION % ----------------
    completion_percentage = (
        (completed_tasks / total_tasks) * 100
        if total_tasks > 0 else 0
    )

    # ---------------- CONSISTENCY SCORE ----------------
    consistency_score = 0

    if completion_percentage >= 80:
        consistency_score = 9

    elif completion_percentage >= 60:
        consistency_score = 7

    elif completion_percentage >= 40:
        consistency_score = 5

    else:
        consistency_score = 3

    # ---------------- PRODUCTIVITY TREND ----------------
    if completion_percentage >= 80:

        productivity_trend = "Highly Productive"

    elif completion_percentage >= 60:

        productivity_trend = "Moderately Productive"

    else:

        productivity_trend = "Needs Improvement"

    # ---------------- MAIN FEEDBACK ----------------
    if completion_percentage >= 80:

        feedback_message = (
            "Excellent consistency and productivity. "
            "You are managing your sessions very effectively."
        )

        st.success(feedback_message)

    elif completion_percentage >= 60:

        feedback_message = (
            "Good progress detected. "
            "Try reducing pending tasks "
            "to improve overall productivity."
        )

        st.warning(feedback_message)

    else:

        feedback_message = (
            "Low productivity trend detected. "
            "Focus mode and better scheduling "
            "can help improve consistency."
        )

        st.error(feedback_message)

    # ---------------- ANALYSIS METRICS ----------------
    st.markdown("### Behavioral Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Consistency Score",
        f"{consistency_score}/10"
    )

    col2.metric(
        "Completion Rate",
        f"{completion_percentage:.1f}%"
    )

    col3.metric(
        "Pending Sessions",
        pending_tasks
    )

    # ---------------- TREND DISPLAY ----------------
    st.markdown("### Productivity Trend")

    if productivity_trend == "Highly Productive":

        st.success(productivity_trend)

    elif productivity_trend == "Moderately Productive":

        st.warning(productivity_trend)

    else:

        st.error(productivity_trend)

    # ---------------- IMPROVEMENT SUGGESTIONS ----------------
    st.markdown("### Improvement Suggestions")

    suggestions = []

    if pending_tasks > completed_tasks:

        suggestions.append(
            "Try completing smaller tasks first "
            "to reduce workload pressure."
        )

    if completion_percentage < 50:

        suggestions.append(
            "Use Focus Mode regularly "
            "to reduce distractions."
        )

    if completion_percentage >= 80:

        suggestions.append(
            "Maintain your current consistency "
            "and scheduling discipline."
        )

    if len(suggestions) == 0:

        suggestions.append(
            "Your performance is balanced and stable."
        )

    for suggestion in suggestions:

        st.info(suggestion)