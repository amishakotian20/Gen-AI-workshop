import os
from flask import Flask, request
from dotenv import load_dotenv
import litellm
from prompt_template import structured_prompt

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Structured Answer Generator</title>
    </head>
    <body style="font-family: Arial; margin: 40px;">
        <h2>📘 AI Structured Answer Generator</h2>
        <form action="/generate" method="get">
            <label><b>Enter ANY Question:</b></label><br><br>
            <input type="text" name="question" size="70" required>
            <br><br>
            <input type="submit" value="Generate Answer">
        </form>
        <br>
        <p><b>Examples:</b></p>
        <ul>
            <li>Explain A* Search Algorithm</li>
            <li>What is Machine Learning?</li>
            <li>Explain DBMS Normalization</li>
            <li>What is Quantum Computing?</li>
        </ul>
    </body>
    </html>
    """

@app.route("/generate", methods=["GET"])
def generate_answer():
    question = request.args.get("question")

    if not question or question.strip() == "":
        return """
        <h3>❌ Please enter a valid question.</h3>
        <a href="/">⬅ Go Back</a>
        """

    try:
        response = litellm.completion(
            model="groq/llama-3.1-8b-instant",  # ✅ Updated working model
            api_key=os.getenv("GROQ_API_KEY"),
            messages=[
                {"role": "system", "content": "You are an expert tutor for all subjects."},
                {"role": "user", "content": structured_prompt(question)}
            ],
            temperature=1.2
        )

        answer = response["choices"][0]["message"]["content"]

        return f"""
        <html>
        <head>
            <title>Structured Answer</title>
        </head>
        <body style="font-family: Arial; margin: 40px;">
            <h2>📘 Structured Answer Generator</h2>
            <h3>Question:</h3>
            <p><b>{question}</b></p>
            <hr>
            <h3>Structured Explanation:</h3>
            <pre style="white-space: pre-wrap; font-size: 16px; line-height: 1.6;">
{answer}
            </pre>
            <br>
            <a href="/">⬅ Ask Another Question</a>
        </body>
        </html>
        """

    except Exception as e:
        return f"""
        <h3>❌ Error Occurred:</h3>
        <pre>{str(e)}</pre>
        <br>
        <a href="/">⬅ Go Back</a>
        """

if __name__ == "__main__":
    app.run(debug=True)