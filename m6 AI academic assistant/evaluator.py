# evaluator.py

def evaluate_answer(question, answer):
    score = 0

    if "Definition" in answer:
        score += 1
    if "Example" in answer:
        score += 1
    if len(answer) > 200:
        score += 1

    return {
        "structure_score": score,
        "max_score": 3
    }