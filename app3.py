import streamlit as st
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Interview Simulator", layout="wide")

# -------- TITLE --------
st.title("🎤 AI Interview Simulator")

st.markdown("""
<div style='text-align: center; color: gray; font-size:16px;'>
Developed by <b>Kalyani Pawar</b>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.write("Practice interviews with smart evaluation")

# -------- QUESTIONS --------
QUESTIONS = {

    "HR": [
        "Tell me about yourself.",
        "Why should we hire you?",
        "What are your strengths and weaknesses?",
        "Where do you see yourself in 5 years?",
        "How do you handle pressure?"
    ],

    "Data Analyst": [
        "Explain a data analysis project.",
        "What is SQL?",
        "What is data cleaning?",
        "What is data visualization?",
        "What is a JOIN in SQL?"
    ],

    "Python Developer": [
        "What is Python?",
        "Explain OOP concepts.",
        "What is a list vs tuple?",
        "What is exception handling?",
        "What is a function in Python?"
    ]
}

# -------- SIDEBAR --------
st.sidebar.title("⚙️ Settings")
role = st.sidebar.selectbox("Select Role", list(QUESTIONS.keys()))

# -------- SESSION STATE --------
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

# -------- EVALUATION FUNCTION --------
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
        feedback.append("Add real examples")

    if any(word in ans for word in ["python", "sql", "data", "analysis"]):
        score += 2
    else:
        feedback.append("Add technical keywords")

    if any(word in ans for word in ["first", "second", "finally"]):
        score += 2
    else:
        feedback.append("Structure your answer better")

    return score, feedback

# -------- SUBMIT --------
if st.button("Submit Answer"):
    if answer.strip() == "":
        st.warning("Please write your answer first")
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

# -------- NEXT QUESTION --------
if st.button("Next Question"):
    available = list(set(QUESTIONS[role]) - set(st.session_state.asked))

    if not available:
        st.session_state.asked = []
        available = QUESTIONS[role]

    q = random.choice(available)
    st.session_state.question = q
    st.session_state.asked.append(q)

    st.rerun()

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
