import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")

client = genai.Client(api_key=API_KEY)


def generate_interview_questions(
    job_role,
    experience,
    key_skills,
    num_questions
):

    prompt = f"""
You are an expert technical interviewer.

Generate {num_questions} interview questions.

Job Role:
{job_role}

Experience Level:
{experience}

Key Skills:
{key_skills}

The questions MUST be based primarily on the Key Skills provided above.

Requirements:
- Questions must be relevant to the job role.
- Questions must match the candidate's experience level.
- Focus strongly on the listed key skills.
- Include conceptual, practical, and scenario-based questions.
- Avoid unrelated topics.
- Do not provide answers.
- Return only the interview questions.
- Number each question clearly.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text