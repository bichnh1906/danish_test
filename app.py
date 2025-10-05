import streamlit as st
import json
import random

# Load bilingual questions from JSON file
with open("bilingual_questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Filter valid questions
valid_questions = [
    q for q in questions
    if all(k in q for k in ("question_dk", "question_en", "options_dk", "options_en", "answer_dk"))
]

# Initialize session state
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
    st.session_state.questions = []
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.answers = []

# Start quiz
st.title("🇩🇰 Medborgerskabsprøven Quiz 🇬🇧")
if not st.session_state.quiz_started:
    st.markdown("This is a bilingual Danish-English quiz to practice for the Medborgerskabsprøven test.")
    if st.button("Start Quiz"):
        st.session_state.quiz_started = True
        st.session_state.questions = random.sample(valid_questions, 25)
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.answers = []

# Display quiz
if st.session_state.quiz_started and st.session_state.current_index < 25:
    q = st.session_state.questions[st.session_state.current_index]
    st.markdown(f"**Question {st.session_state.current_index + 1} of 25**")
    st.markdown(f"**🇩🇰 Danish:** {q['question_dk']}")
    st.markdown(f"**🇬🇧 English:** {q['question_en']}")

    options = list(q["options_dk"].keys())
    selected = st.radio(
        "Choose your answer:",
        options=options,
        format_func=lambda x: f"{x}: {q['options_dk'][x]} / {q['options_en'].get(x, '')}"
    )

    if st.button("Submit Answer"):
        st.session_state.answers.append(selected)
        correct = q["answer_dk"]
        if selected == correct:
            st.session_state.score += 1
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. Correct answer is {correct}: {q['options_dk'][correct]} / {q['options_en'].get(correct, '')}")
        st.session_state.current_index += 1

# Final result
if st.session_state.quiz_started and st.session_state.current_index >= 25:
    st.markdown("---")
    st.subheader("Quiz Completed!")
    st.markdown(f"**Your Score: {st.session_state.score} / 25**")
    if st.session_state.score >= 20:
        st.success("🎉 You passed the test!")
    else:
        st.error("❌ You did not pass. Try again!")

    if st.button("Restart Quiz"):
        st.session_state.quiz_started = False
