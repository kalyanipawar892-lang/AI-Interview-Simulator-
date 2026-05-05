import streamlit as st
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Interview Simulator", layout="wide")

st.title("🎤 AI Interview Simulator")
st.write("Practice interviews with smart evaluation")

# -------- QUESTIONS --------
QUESTIONS = {

    "HR": [
        "Tell me about yourself.",
        "Why should we hire you?",
        "What are your strengths and weaknesses?",
        "Where do you see yourself in 5 years?",
        "Why do you want to work for our company?",
        "Tell me about a challenge you faced.",
        "How do you handle pressure?",
        "What motivates you?",
        "Describe a failure and what you learned.",
        "Are you a team player?"
    ],

    "Data Analyst": [
        "Explain a data analysis project you worked on.",
        "What is SQL?",
        "What is a JOIN in SQL?",
        "Difference between INNER JOIN and LEFT JOIN.",
        "What is data cleaning?",
        "What is data visualization?",
        "What is Excel used for in data analysis?",
        "Explain Power BI or Tableau.",
        "What is a primary key?",
        "What is normalization?",
        "What is data wrangling?",
        "Explain mean, median, and mode.",
        "What is standard deviation?",
        "What is correlation?",
        "Difference between structured and unstructured data.",
        "What is ETL process?",
        "What is data pipeline?",
        "Explain a dashboard you created.",
        "What tools have you used for analysis?",
        "How do you handle missing data?"
    ],

    "Python Developer": [
        "What is Python?",
        "What are data types in Python?",
        "Difference between list and tuple.",
        "What is a dictionary?",
        "Explain OOP concepts.",
        "What is inheritance?",
        "What is polymorphism?",
        "What are decorators?",
        "What is lambda function?",
        "What is exception handling?",
        "What is a module and package?",
        "What is virtual environment?",
        "What is list comprehension?",
        "Difference between deep copy and shallow copy.",
        "What is multithreading?",
        "What is GIL in Python?",
        "Explain file handling in Python.",
        "What is pandas?",
        "What is numpy?",
        "Explain a Python project you built."
    ]
}

# -------- SIDEBAR --------
st.sidebar.title("⚙️ Settings")
role = st.sidebar.selectbox("Select Role", list(QUESTIONS.keys()))

# -------- SESSION --------
if "question" not in st.session_state:
    st.session_state.question = random.choice(QUESTIONS[role])

if "scores" not in st.session_state:
    st.session_state.scores = []

if "asked" not in st.session_state:
    st.session_state.asked = []

# -------- QUESTION --------
st.subheader("💬 Question")
st.write(st.session_state.question)

# -------- ANSWER --------
answer = st.text_area("✍️ Your Answer", height=150)

# -------- EVALUATION --------
def evaluate_answer(ans):
    ans = ans.lower()
    score = 0
    feedback = []

    if len(ans) > 80:
        score += 3
    else:
        feedback.append("Answer is too short")

    if any(word in ans for word in ["project", "experience", "example"]):
        score += 3
    else:
        feedback.append("Add real examples/projects")

    if any(word in ans for word in ["python", "sql", "data", "analysis"]):
        score += 2
    else:
        feedback.append("Include technical keywords")

    if any(word in ans for word in ["first", "second", "finally"]):
        score += 2
    else:
        feedback.append("Structure your answer properly")

    return score, feedback

# -------- SUBMIT --------
if st.button("Submit Answer"):
    if answer.strip() == "":
        st.warning("Write your answer first")
    else:
        score, feedback = evaluate_answer(answer)
        st.session_state.scores.append(score)

        st.subheader("📊 Evaluation")

        if score >= 8:
            st.success("🔥 Excellent Answer")
        elif score >= 5:
            st.warning("⚠️ Good but can improve")
        else:
            st.error("❌ Weak answer")

        st.write(f"Score: {score}/10")

        st.subheader("📌 Feedback")
        if feedback:
            for f in feedback:
                st.write(f"👉 {f}")
        else:
            st.write("Great answer!")

# -------- NEXT QUESTION (NO REPEAT) --------
if st.button("Next Question"):
    available = list(set(QUESTIONS[role]) - set(st.session_state.asked))

    if not available:
        st.session_state.asked = []
        available = QUESTIONS[role]

    q = random.choice(available)
    st.session_state.question = q
    st.session_state.asked.append(q)

    st.experimental_rerun()

# -------- DASHBOARD --------
st.subheader("📊 Performance Dashboard")

if st.session_state.scores:
    fig, ax = plt.subplots()
    ax.plot(st.session_state.scores, marker='o')
    ax.set_title("Your Scores Over Time")
    ax.set_xlabel("Attempts")
    ax.set_ylabel("Score")
    st.pyplot(fig)
else:
    st.write("No data yet")
