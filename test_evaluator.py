from utils.evaluator import evaluate_answer


question = "What is the difference between a list and a tuple in Python?"

answer = """
A list is mutable, which means we can change it after creating it.
A tuple is immutable, so we cannot change it after creating it.
"""

result = evaluate_answer(question, answer)

print(result)