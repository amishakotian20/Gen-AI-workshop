# llm.py

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_response(prompt):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # ✅ updated model
        messages=[
            {"role": "system", "content": "You are an academic AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content