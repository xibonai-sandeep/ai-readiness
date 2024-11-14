import streamlit as st
from openai_helper import generate_questions

def app():
    st.header("AI Readiness Assessment")

    if "company_info" not in st.session_state or not st.session_state.company_info:
        st.warning("Please fill out the Company Information first.")
        return

    if "questions" not in st.session_state:
        try:
            with st.spinner("Generating questions..."):
                st.session_state.questions = generate_questions(
                    st.session_state.company_info["industry"],
                    st.session_state.company_info["size"],
                    st.session_state.company_info["country"],
                )
            # Debugging: Print the structure of questions
            print("Generated questions:", st.session_state.questions)
        except Exception as e:
            st.error(f"An error occurred while generating questions: {str(e)}")
            st.write("Please try again or contact support if the issue persists.")
            st.session_state.questions = []

    if not st.session_state.questions:
        st.warning("No questions were generated. Please try again or contact support.")
        return

    if "answers" not in st.session_state:
        st.session_state.answers = {}

    progress_bar = st.progress(0)

    for i, question_data in enumerate(st.session_state.questions):
        if not isinstance(question_data, dict) or "question_text" not in question_data:
            st.error(f"Invalid question data for question {i+1}")
            continue

        st.subheader(f"Question {i+1}")
        st.write(question_data["question_text"])
        st.info(question_data.get("explanation", "No explanation available"))
        st.write(f"**Impact:** {question_data.get('impact_level', 'Not specified')}")

        question_type = question_data.get("type", "").lower()
        if question_type == "scale":
            answer = st.slider(
                "Rate your agreement (1: Strongly Disagree, 5: Strongly Agree)",
                1,
                5,
                key=f"q{i}",
            )
        elif question_type == "multiple-choice":
            options = question_data.get("options", [])
            if options:
                answer = st.selectbox("Select one option:", options, key=f"q{i}")
            else:
                st.error(f"Error: No options provided for question {i+1}")
                answer = ""
        else:  # open-ended
            answer = st.text_area("Your answer:", key=f"q{i}")

        st.session_state.answers[f"q{i}"] = answer

        progress = (i + 1) / len(st.session_state.questions)
        progress_bar.progress(progress)

    if st.button("Submit Assessment"):
        if len(st.session_state.answers) == len(st.session_state.questions):
            st.success("Assessment completed. Please proceed to the Results page.")
        else:
            st.warning("Please answer all questions before submitting.")

    # Add a debug section
    if st.checkbox("Show Debug Information"):
        st.write("Session State:")
        st.write(st.session_state)
        st.write("Questions:")
        st.write(st.session_state.questions)
        st.write("Answers:")
        st.write(st.session_state.answers)