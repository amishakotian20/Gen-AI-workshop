# agent.py

def academic_agent(query, retriever):

    # NEW LangChain way
    docs = retriever.invoke(query)

    formatted_context = "\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an academic assistant.

Use the context below to answer the question clearly and academically.

Context:
{formatted_context}

Question:
{query}

Provide:
- Definition
- Explanation
- Example
- Conclusion
"""

    return prompt