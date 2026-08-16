from utils.gemini import generate_interview_questions

questions = generate_interview_questions(
    "Python Developer",
    "Fresher",
    5
)

print(questions)