import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from ai_engine import StudyEngine, WorkEngine, HealthEngine
from scheduler import start_scheduler
from data_manager import save_data, load_data
import google.generativeai as genai

# ---------------- CONFIG ---------------- #
st.set_page_config(page_title="AI Productivity System", layout="wide")

# Gemini Setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
gemini_model = genai.GenerativeModel("gemini-pro")

# ---------------- SESSION INIT ---------------- #
if "data" not in st.session_state:
    st.session_state.data = load_data()

if "scheduler_started" not in st.session_state:
    start_scheduler(st.session_state)
    st.session_state.scheduler_started = True

# ---------------- NAVIGATION ---------------- #
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to:", ["Study", "Work", "Health", "Dashboard"])

# ===================== STUDY SECTION ===================== #
if section == "Study":
    st.header("📚 Study Planner")

    module = st.text_input("Module Name")
    exam_date = st.date_input("Exam Date")
    topics = st.text_area("Topics (comma separated)")
    daily_hours = st.number_input("Daily Study Hours", min_value=1, max_value=12)

    if st.button("Generate Study Plan"):
        try:
            topic_list = [t.strip() for t in topics.split(",")]
            engine = StudyEngine()
            plan = engine.generate_plan(
                module,
                exam_date,
                topic_list,
                daily_hours
            )

            st.session_state.data["study_plan"] = plan
            save_data(st.session_state.data)

            st.success("Study Plan Generated Successfully!")
            st.json(plan)

            feedback = gemini_model.generate_content(
                f"Provide motivational academic feedback for this plan: {plan}"
            )
            st.info(feedback.text)

        except Exception as e:
            st.error(f"Error: {e}")

# ===================== WORK SECTION ===================== #
elif section == "Work":
    st.header("💼 Work Planner")

    tasks = st.text_area("Tasks (comma separated)")
    priorities = st.text_area("Priorities (match order, comma separated)")

    if st.button("Generate Work Blocks"):
        try:
            task_list = [t.strip() for t in tasks.split(",")]
            priority_list = [int(p.strip()) for p in priorities.split(",")]

            engine = WorkEngine()
            plan = engine.generate_focus_blocks(task_list, priority_list)

            st.session_state.data["work_plan"] = plan
            save_data(st.session_state.data)

            st.success("Work Plan Generated!")
            st.json(plan)

        except Exception as e:
            st.error(f"Error: {e}")

# ===================== HEALTH SECTION ===================== #
elif section == "Health":
    st.header("🏥 Health Tracker")

    hydration_goal = st.number_input("Hydration Goal (glasses/day)", 1, 20)
    exercise_time = st.number_input("Exercise Minutes per Day", 10, 180)
    sleep_hours = st.number_input("Sleep Hours per Night", 4, 12)

    if st.button("Save Health Goals"):
        st.session_state.data["health"] = {
            "hydration_goal": hydration_goal,
            "exercise_time": exercise_time,
            "sleep_hours": sleep_hours
        }
        save_data(st.session_state.data)
        st.success("Health Goals Saved!")

# ===================== DASHBOARD ===================== #
elif section == "Dashboard":
    st.header("📊 Analytics Dashboard")

    data = st.session_state.data

    # Completed vs Missed (Mock Example)
    completed = data.get("completed_tasks", 5)
    missed = data.get("missed_tasks", 2)

    fig1 = plt.figure()
    plt.bar(["Completed", "Missed"], [completed, missed])
    plt.title("Completed vs Missed Tasks")
    st.pyplot(fig1)

    # Productivity Trend
    trend = data.get("productivity_trend", [2, 4, 6, 5, 7])
    fig2 = plt.figure()
    plt.plot(trend)
    plt.title("Productivity Trend")
    st.pyplot(fig2)

    # Hydration Chart
    hydration = data.get("hydration_log", [3, 5, 4, 6])
    fig3 = plt.figure()
    plt.plot(hydration)
    plt.title("Hydration Tracking")
    st.pyplot(fig3)

st.markdown("---")
st.caption("AI Productivity System | Streamlit Cloud Ready")
