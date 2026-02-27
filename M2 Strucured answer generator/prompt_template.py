def structured_prompt(question):
    return f"""
You are an expert academic tutor capable of explaining ANY subject clearly.

Question: {question}

Explain the topic in a well-structured format suitable for a university 10-mark answer.

Follow this structure strictly:

1. Title
2. Definition / Introduction
3. Key Concepts (bullet points)
4. Detailed Explanation
5. Real-world Example
6. Diagram (ASCII if applicable, otherwise skip)
7. Advantages
8. Disadvantages
9. Conclusion

Make the answer clear, neat, and properly formatted.
"""