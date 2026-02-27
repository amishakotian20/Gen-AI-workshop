# app.py

from retriever import get_retriever
from agent import academic_agent
from evaluator import evaluate_answer
from llm import generate_response

retriever = get_retriever()

query = input("Ask your academic question: ")

prompt = academic_agent(query, retriever)
answer = generate_response(prompt)

evaluation = evaluate_answer(query, answer)

print("\nAnswer:\n", answer)
print("\nEvaluation:\n", evaluation)