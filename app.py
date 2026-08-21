import streamlit as st
import re
import hashlib
import html
import base64

from utils.gemini import generate_interview_questions
from utils.evaluator import evaluate_answer
from utils.speech import transcribe_audio


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Interview Preparation Assistant",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# LOAD BACKGROUND IMAGE
# =========================================================

background_image = "background.jpg"

try:
    with open(background_image, "rb") as img_file:
        encoded_image = base64.b64encode(
            img_file.read()
        ).decode()
except FileNotFoundError:
    encoded_image = ""


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background-image:
            linear-gradient(
                rgba(245, 249, 253, 0.60),
                rgba(245, 249, 253, 0.60)
            ),
            url("data:image/jpeg;base64,{encoded_image}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}


    .block-container {{
        padding-top: 2rem;
        padding-left: 4rem;
        padding-right: 4rem;
    }}


    h1,
    h2,
    h3 {{
        color: #17365D;
    }}


    .main-title {{
        font-size: 50px;
        font-weight: 700;
        color: #17365D;
        margin-bottom: 5px;
    }}


    .subtitle {{
        font-size: 19px;
        color: #555555;
        margin-bottom: 25px;
    }}


    .section-title {{
        font-size: 28px;
        font-weight: 650;
        color: #17365D;
        margin-top: 10px;
        margin-bottom: 15px;
    }}


    .faq-hint {{
        position: fixed;
        top: 21px;
        left: 47px;
        z-index: 999999;

        display: inline-block;

        background-color: #e8f0fe;
        color: #17365D;

        padding: 6px 12px;

        border-radius: 4px;

        border: 1px solid #b7c9e8;

        font-size: 9px;
        font-weight: 600;

        margin: 0;

        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }}


    body:has(
        section[data-testid="stSidebar"][aria-expanded="true"]
    ) .faq-hint {{
        display: none !important;
    }}


    .question-card {{
        background-color: #eef3f8;

        border: 1px solid #d5dee8;

        border-radius: 10px;

        padding: 15px 18px;

        margin-bottom: 10px;

        font-size: 16px;

        line-height: 1.7;

        color: #17365D;

        white-space: normal;

        overflow-wrap: anywhere;

        word-break: normal;
    }}


    .selected-question-box {{
        background-color: rgba(232, 240, 254, 0.96);

        border: 1px solid #b7c9e8;

        border-left: 5px solid #17365D;

        border-radius: 8px;

        padding: 16px 20px;

        margin-top: 10px;

        margin-bottom: 20px;

        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);

        width: 100%;

        box-sizing: border-box;
    }}


    .selected-question-title {{
        color: #17365D;

        font-size: 16px;

        font-weight: 700;

        margin-bottom: 8px;
    }}


    .selected-question-text {{
        color: #333333;

        font-size: 15px;

        line-height: 1.7;

        overflow-wrap: anywhere;

        word-break: normal;

        white-space: normal;
    }}


    section[data-testid="stSidebar"] {{
        background-color: rgba(248, 250, 252, 0.96);
    }}


    .guide-box {{
        background-color: #eef4fb;

        border: 1px solid #cbd9e8;

        border-radius: 10px;

        padding: 15px;

        margin-bottom: 15px;
    }}


    textarea {{
        line-height: 1.6 !important;
    }}


    .final-feedback-box {{
        background-color: rgba(255, 255, 255, 0.94);

        border: 1px solid #cbd9e8;

        border-left: 5px solid #17365D;

        border-radius: 10px;

        padding: 20px;

        margin-top: 15px;

        line-height: 1.7;

        color: #333333;

        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }}


    .progress-text {{
        color: #17365D;

        font-size: 14px;

        font-weight: 600;

        margin-bottom: 8px;
    }}


    .footer {{
        text-align: center;

        color: #777777;

        font-size: 13px;

        margin-top: 30px;

        padding: 15px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

/* =========================================================
   MOBILE RESPONSIVE DESIGN
   ========================================================= */

@media screen and (max-width: 768px) {

    .block-container {
        padding-top: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-bottom: 2rem !important;
    }

    .main-title {
        font-size: 30px !important;
        line-height: 1.2 !important;
        margin-bottom: 8px !important;
    }

    .subtitle {
        font-size: 15px !important;
        line-height: 1.5 !important;
        margin-bottom: 15px !important;
    }

    .section-title {
        font-size: 22px !important;
        line-height: 1.3 !important;
        margin-top: 8px !important;
        margin-bottom: 12px !important;
    }

    .question-card {
        padding: 12px 14px !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
        margin-bottom: 8px !important;
    }

    .selected-question-box {
        padding: 12px 14px !important;
    }

    .selected-question-title {
        font-size: 14px !important;
    }

    .selected-question-text {
        font-size: 14px !important;
        line-height: 1.6 !important;
    }

    .final-feedback-box {
        padding: 14px !important;
        font-size: 14px !important;
    }

    .progress-text {
        font-size: 13px !important;
    }

    .footer {
        font-size: 11px !important;
        margin-top: 20px !important;
        padding: 10px !important;
    }

    /* Make buttons easier to tap */
    .stButton > button {
        width: 100% !important;
        min-height: 45px !important;
        font-size: 14px !important;
    }

    /* Make text areas comfortable on phones */
    textarea {
        font-size: 15px !important;
    }

}


# =========================================================
# GUIDE LABEL
# =========================================================

st.markdown(
    """
    <div class="faq-hint">
        👉 Click <strong>&gt;&gt;</strong> to open the User Guide
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "questions" not in st.session_state:
    st.session_state["questions"] = []

if "current_question_index" not in st.session_state:
    st.session_state["current_question_index"] = 0

if "feedback" not in st.session_state:
    st.session_state["feedback"] = ""

if "answer_evaluated" not in st.session_state:
    st.session_state["answer_evaluated"] = False

if "answer_version" not in st.session_state:
    st.session_state["answer_version"] = 0

if "voice_version" not in st.session_state:
    st.session_state["voice_version"] = 0

if "voice_text" not in st.session_state:
    st.session_state["voice_text"] = ""

if "processed_audio_hash" not in st.session_state:
    st.session_state["processed_audio_hash"] = None

if "completed_answers" not in st.session_state:
    st.session_state["completed_answers"] = {}

if "final_feedback" not in st.session_state:
    st.session_state["final_feedback"] = ""


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("### 📖 How to Use")

    st.markdown(
        """
        **1️⃣ Enter your Job Role**

        Example: Python Developer

        **2️⃣ Select Experience Level**

        • Fresher  
        • 0–2 years  
        • 2–5 years  
        • 5+ years

        **3️⃣ Choose Number of Questions**

        Select the number of interview questions.

        **4️⃣ Generate Questions**

        Click **🚀 Generate Questions**.

        **5️⃣ Answer the Question**

        Type your answer or record it using your microphone.

        **6️⃣ Evaluate Your Answer**

        Click **🔍 Evaluate My Answer**.

        **7️⃣ Next Question**

        After evaluation, click **➡️ Next Question**.

        **8️⃣ Complete All Questions**

        Continue until all questions are completed.

        **9️⃣ Final Feedback**

        Generate your overall AI interview report.
        """
    )

    st.divider()

    st.markdown("### 💡 Tip")

    st.info(
        "You can edit the text produced from your voice recording "
        "before submitting it for evaluation."
    )

    st.divider()

    st.caption(
        "Practice • Improve • Get interview-ready"
    )


# =========================================================
# MAIN TITLE
# =========================================================

st.markdown(
    '<div class="main-title">'
    '🤖 AI Interview Preparation Assistant'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Practice. Improve. Get interview-ready.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# GENERATE QUESTIONS
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📋 Generate Interview Questions'
    '</div>',
    unsafe_allow_html=True
)


job_role = st.text_input(
    "💼 Job Role",
    placeholder="Example: Python Developer"
)


experience = st.selectbox(
    "📈 Experience Level",
    [
        "Fresher",
        "0–2 years",
        "2–5 years",
        "5+ years"
    ]
)

# =========================================================
# KEY SKILLS
# =========================================================

key_skills = st.text_input(
    "🛠️ Key Skills",
    placeholder="Example: Python, SQL, Machine Learning, REST API"
)




num_questions = st.slider(
    "🔢 Number of Questions",
    min_value=1,
    max_value=10,
    value=5,
    key="num_questions_slider"

)


# =========================================================
# GENERATE BUTTON
# =========================================================

if st.button("🚀 Generate Questions",key="generate_questions_button"):

    if not job_role.strip():

        st.warning(
            "Please enter a job role."
        )

    else:

        skills_for_prompt = key_skills.strip()

        if not skills_for_prompt:
            skills_for_prompt = (
                "No specific skills provided. "
                "Focus on the selected job role."
            )

        with st.spinner(
            "🤖 Generating interview questions..."
        ):

            try:

                questions_text = generate_interview_questions(
                    job_role.strip(),
                    experience,
                    key_skills.strip(),
                    num_questions

                )

                questions = []
                seen_questions = set()

                for line in questions_text.split("\n"):

                    question = line.strip()

                    if not question:
                        continue

                    question = question.replace(
                        "**",
                        ""
                    )

                    question = re.sub(
                        r"^\s*(?:[-•*]\s*|\d+\s*[\.\):-]\s*)",
                        "",
                        question
                    ).strip()

                    question = re.sub(
                        r"^\s*\d+\s*[\.\):-]\s*",
                        "",
                        question
                    ).strip()

                    if not question:
                        continue

                    question_key = question.lower()

                    if question_key not in seen_questions:

                        seen_questions.add(
                            question_key
                        )

                        questions.append(
                            question
                        )

                questions = questions[:num_questions]

                if questions:

                    st.session_state["questions"] = questions

                    # Start from Question 1
                    st.session_state[
                        "current_question_index"
                    ] = 0

                    # Reset answer
                    st.session_state[
                        "answer_version"
                    ] += 1

                    # Reset voice
                    st.session_state[
                        "voice_version"
                    ] += 1

                    st.session_state[
                        "voice_text"
                    ] = ""

                    st.session_state[
                        "processed_audio_hash"
                    ] = None

                    # Reset feedback
                    st.session_state[
                        "feedback"
                    ] = ""

                    # Reset evaluation status
                    st.session_state[
                        "answer_evaluated"
                    ] = False

                    # Reset completed answers
                    st.session_state[
                        "completed_answers"
                    ] = {}

                    # Reset final feedback
                    st.session_state[
                        "final_feedback"
                    ] = ""

                    st.success(
                        "Questions generated successfully!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "No questions were generated. "
                        "Please try again."
                    )

            except Exception as e:

                st.error(
                    f"Could not generate questions: {e}"
                )


# =========================================================
# INTERVIEW SECTION
# =========================================================

if st.session_state["questions"]:

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '📝 Interview Questions'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # DISPLAY ALL GENERATED QUESTIONS
    # =====================================================

    for i, question in enumerate(
        st.session_state["questions"],
        start=1
    ):

        st.markdown(
            f"""
            <div class="question-card">
                <strong>{i}.</strong> {html.escape(question)}
            </div>
            """,
            unsafe_allow_html=True
        )


    st.divider()


    # =====================================================
    # CURRENT QUESTION
    # =====================================================

    total_questions = len(
        st.session_state["questions"]
    )


    current_question_index = st.session_state[
        "current_question_index"
    ]


    # Safety check
    if current_question_index >= total_questions:

        current_question_index = total_questions - 1

        st.session_state[
            "current_question_index"
        ] = current_question_index


    current_question = st.session_state[
        "questions"
    ][current_question_index]


    safe_current_question = html.escape(
        current_question
    )


    # =====================================================
    # DISPLAY CURRENT QUESTION
    # =====================================================

    st.info(
    f"📝 Question {current_question_index + 1} of {total_questions}\n\n"
    f"{current_question}"
)


    # =====================================================
    # PROGRESS
    # =====================================================

    completed = len(
        st.session_state["completed_answers"]
    )


    progress_value = completed / total_questions


    st.markdown(
        '<div class="progress-text">'
        f'📊 Interview Progress: '
        f'{completed}/{total_questions} questions completed'
        '</div>',
        unsafe_allow_html=True
    )


    st.progress(
        progress_value
    )


    # =====================================================
    # ANSWER SECTION
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '✍️ Answer the Question'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # VOICE ANSWER
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '🎙️ Answer Using Your Voice'
        '</div>',
        unsafe_allow_html=True
    )


    st.write(
        "Record your answer and convert it to text. "
        "You can edit the transcription before evaluation."
    )


    # =====================================================
    # CLEAR VOICE
    # =====================================================

    if st.button(
        "🗑️ Clear Voice Recording",
        key=f"clear_voice_{current_question_index}"
    ):

        st.session_state[
            "voice_version"
        ] += 1

        st.session_state[
            "answer_version"
        ] += 1

        st.session_state[
            "voice_text"
        ] = ""

        st.session_state[
            "processed_audio_hash"
        ] = None

        st.session_state[
            "feedback"
        ] = ""

        st.session_state[
            "answer_evaluated"
        ] = False

        st.rerun()


    # =====================================================
    # AUDIO RECORDER
    # =====================================================

    audio_file = st.audio_input(
        "🎤 Record your answer",
        key=f"audio_{current_question_index}_{st.session_state['voice_version']}"
    )


    # =====================================================
    # PROCESS AUDIO
    # =====================================================

    if audio_file is not None:

        try:

            audio_bytes = audio_file.getvalue()

            audio_hash = hashlib.md5(
                audio_bytes
            ).hexdigest()


            if (
                st.session_state[
                    "processed_audio_hash"
                ]
                != audio_hash
            ):

                with st.spinner(
                    "🎧 Converting your voice to text..."
                ):

                    transcribed_text = transcribe_audio(
                        audio_file
                    )


                if transcribed_text:

                    st.session_state[
                        "voice_text"
                    ] = transcribed_text


                    st.session_state[
                        "answer_version"
                    ] += 1


                    st.session_state[
                        "processed_audio_hash"
                    ] = audio_hash


                    st.session_state[
                        "feedback"
                    ] = ""


                    st.session_state[
                        "answer_evaluated"
                    ] = False


                    st.success(
                        "Voice converted to text successfully!"
                    )


                    st.rerun()


                else:

                    st.warning(
                        "No speech was detected. "
                        "Please record again."
                    )


                    st.session_state[
                        "processed_audio_hash"
                    ] = audio_hash


        except Exception as e:

            st.error(
                f"Could not transcribe the audio: {e}"
            )


    st.divider()


    # =====================================================
    # TEXT ANSWER
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '📝 Your Answer'
        '</div>',
        unsafe_allow_html=True
    )


    st.write(
        "Type your answer here:"
    )


    answer_key = (
        f"answer_{current_question_index}_"
        f"{st.session_state['answer_version']}"
    )


    answer = st.text_area(
        "",
        value=st.session_state["voice_text"],
        height=220,
        placeholder="Write your interview answer here...",
        key=answer_key
    )


    # =====================================================
    # EVALUATE ANSWER
    # =====================================================

    st.divider()


    if not st.session_state["answer_evaluated"]:

        if st.button(
            "🔍 Evaluate My Answer",
            key=f"evaluate_{current_question_index}"
        ):

            if not answer.strip():

                st.warning(
                    "Please type an answer or record "
                    "a voice answer first."
                )

            else:

                with st.spinner(
                    "🤖 AI is evaluating your answer..."
                ):

                    try:

                        feedback = evaluate_answer(
                            current_question,
                            answer.strip()
                        )


                        # Save feedback
                        st.session_state[
                            "feedback"
                        ] = feedback


                        # Save completed answer
                        st.session_state[
                            "completed_answers"
                        ][current_question_index] = {

                            "question":
                                current_question,

                            "answer":
                                answer.strip(),

                            "feedback":
                                feedback
                        }


                        # Mark evaluated
                        st.session_state[
                            "answer_evaluated"
                        ] = True


                        st.success(
                            "Evaluation completed!"
                        )


                        st.rerun()


                    except Exception as e:

                        st.error(
                            f"Could not evaluate your answer: {e}"
                        )


    # =====================================================
    # DISPLAY AI FEEDBACK
    # =====================================================

    if st.session_state.get("feedback"):

        st.divider()


        st.markdown(
            '<div class="section-title">'
            '📊 AI Feedback'
            '</div>',
            unsafe_allow_html=True
        )


        st.markdown(
            '<div class="final-feedback-box">',
            unsafe_allow_html=True
        )


        st.write(
            st.session_state["feedback"]
        )


        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    # =====================================================
    # NEXT QUESTION
    # =====================================================

    if st.session_state["answer_evaluated"]:

        st.divider()


        if current_question_index < total_questions - 1:

            if st.button(
                "➡️ Next Question",
                key=f"next_{current_question_index}"
            ):

                # Move to next question
                st.session_state[
                    "current_question_index"
                ] = current_question_index + 1


                # Reset answer state
                st.session_state[
                    "answer_version"
                ] += 1


                # Reset voice
                st.session_state[
                    "voice_version"
                ] += 1


                st.session_state[
                    "voice_text"
                ] = ""


                st.session_state[
                    "processed_audio_hash"
                ] = None


                # Clear old feedback
                st.session_state[
                    "feedback"
                ] = ""


                # Mark new question as not evaluated
                st.session_state[
                    "answer_evaluated"
                ] = False


                st.rerun()


        else:

            st.success(
                "🎉 You have completed all interview questions!"
            )


    # =====================================================
    # FINAL INTERVIEW FEEDBACK
    # =====================================================

    completed_questions = len(
        st.session_state["completed_answers"]
    )


    if (
        total_questions > 0
        and
        completed_questions == total_questions
    ):

        st.divider()


        st.markdown(
            '<div class="section-title">'
            '🏆 Final Interview Feedback'
            '</div>',
            unsafe_allow_html=True
        )


        st.write(
            "You have completed all questions. "
            "Generate your overall AI interview report."
        )


        if st.button(
            "🎯 Generate Final Interview Feedback",
            key="final_feedback_button"
        ):

            # =============================================
            # COMBINE ALL ANSWERS
            # =============================================

            interview_history = ""


            for i in range(total_questions):

                result = st.session_state[
                    "completed_answers"
                ][i]


                interview_history += f"""

Question {i + 1}:
{result["question"]}

Candidate Answer:
{result["answer"]}

Individual AI Feedback:
{result["feedback"]}

--------------------------------------------------

"""


            # =============================================
            # FINAL PROMPT
            # =============================================

            final_prompt = f"""
You are an expert interview coach.

Analyze the candidate's complete interview performance.

Below are all the interview questions, candidate answers,
and individual feedback:

{interview_history}

Provide a professional final interview assessment.

Include the following sections:

1. Overall Score
Give a score out of 100.

2. Interview Readiness
Choose one:
- Excellent
- Good
- Average
- Needs Improvement

3. Overall Performance
Give a short summary of the candidate's performance.

4. Key Strengths
Mention the candidate's strongest qualities.

5. Areas for Improvement
Mention the most important weaknesses to work on.

6. Technical Knowledge
Assess the candidate's understanding of the technical topics.

7. Communication Skills
Assess clarity, structure, confidence and conciseness.

8. Problem-Solving Skills
Assess how effectively the candidate approaches problems.

9. Answer Quality
Mention whether answers were relevant, complete and well structured.

10. Recommendations
Give practical steps the candidate can take to improve.

11. Final Assessment
Give an encouraging but honest final assessment.

IMPORTANT:
- Avoid repeating the same observation in multiple sections.
- Keep each section focused on its own purpose.
- Do not repeat the same strengths or weaknesses unnecessarily.
- Keep the report clear, professional and easy to read.
"""


            # =============================================
            # GENERATE FINAL FEEDBACK
            # =============================================

            try:

                with st.spinner(
                    "🤖 Analyzing your complete interview performance..."
                ):

                    final_feedback = evaluate_answer(
                        "Complete Interview Performance",
                        final_prompt
                    )


                st.session_state[
                    "final_feedback"
                ] = final_feedback


                st.rerun()


            except Exception as e:

                st.error(
                    f"Could not generate final feedback: {e}"
                )


    # =====================================================
    # DISPLAY FINAL REPORT
    # =====================================================

    if st.session_state.get(
        "final_feedback"
    ):

        st.divider()


        st.markdown(
            '<div class="section-title">'
            '🎯 Your Final AI Interview Report'
            '</div>',
            unsafe_allow_html=True
        )


        st.markdown(
            '<div class="final-feedback-box">',
            unsafe_allow_html=True
        )


        st.write(
            st.session_state[
                "final_feedback"
            ]
        )


        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        🤖 AI Interview Preparation Assistant

        

        Practice • Improve • Get interview-ready

    </div>
    """,
    unsafe_allow_html=True
)