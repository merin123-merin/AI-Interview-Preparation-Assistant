from utils.gemini import client


def evaluate_answer(question, answer):
    prompt = f"""
You are an AI interview evaluator.

Evaluate the candidate's answer to the interview question below.

Interview Question:
{question}

Candidate's Answer:
{answer}

Give your evaluation in this format:

Score: X/10

What you did well:
- ...

What could be improved:
- ...

Suggested better answer:
...

Keep the feedback clear, helpful, and suitable for a beginner.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text