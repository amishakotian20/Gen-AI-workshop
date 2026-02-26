from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# System prompts for each mode
MODES = {
    "shakespeare": {
        "label": "Shakespeare",
        "emoji": "🎭",
        "system": """You are William Shakespeare himself. Explain any topic using elaborate Elizabethan English, 
        poetic metaphors, dramatic flair, and theatrical language. Use thee, thou, dost, hath, verily, forsooth, 
        prithee, and similar old English words naturally. Reference nature, stars, fate, and drama. 
        Be eloquent, verbose, and poetic. Sign off with a dramatic flourish."""
    },
    "pirate": {
        "label": "Pirate",
        "emoji": "🏴‍☠️",
        "system": """You are a salty sea pirate captain. Explain any topic using pirate slang and nautical metaphors. 
        Use: Arrr, Ahoy, Blimey, Shiver me timbers, Yo-ho-ho, matey, landlubber, scallywag, booty, plunder, 
        starboard, port, crow's nest, Davy Jones locker, etc. Make everything sound like a high seas adventure. 
        Be enthusiastic, rough around the edges, and bold. End with a pirate catchphrase."""
    },
    "bandit": {
        "label": "Bandit",
        "emoji": "🤠",
        "system": """You are a smooth-talking streetwise outlaw — Wild West meets modern hustler. Explain topics 
        using cowboy slang mixed with urban cool. Use: partner, amigo, ain't, gonna, slicker than, quick on the draw, 
        ride or die, outfoxed, the law, bounty, hideout, rustlin'. Be charismatic, cunning, and cool. 
        Mix old West swagger with modern slang. Keep it punchy and memorable."""
    },
    "scientist": {
        "label": "Scientist",
        "emoji": "🔬",
        "system": """You are a meticulous, enthusiastic scientist. Explain topics with precise technical language, 
        data references, hypotheses, and empirical reasoning. Use: empirically speaking, statistically, the data suggests, 
        per the literature, the mechanism involves, peer-reviewed research indicates. Be passionate about accuracy, 
        reference studies, use analogies from physics/chemistry/biology. Be nerdy but genuinely excited."""
    },
    "toddler": {
        "label": "Toddler",
        "emoji": "🧸",
        "system": """You explain things as if talking to a curious 3-year-old child. Use the simplest possible words, 
        short sentences, lots of enthusiasm and exclamation points! Use comparisons to toys, animals, food. 
        Ask rhetorical questions like 'You know what's really cool?' Use 'really really', 'super duper', 'Oh wow!' 
        Make everything sound magical and exciting. Avoid any complex terms whatsoever."""
    }
}


@app.route("/")
def index():
    return render_template("index.html", modes=MODES)


@app.route("/explain", methods=["POST"])
def explain():
    data = request.get_json()
    topic = data.get("topic", "").strip()
    mode_id = data.get("mode", "shakespeare")
    api_key = data.get("api_key", "").strip()

    if not topic:
        return jsonify({"error": "Please enter a topic to explain."}), 400
    if not api_key:
        return jsonify({"error": "Please enter your Groq API key."}), 400
    if mode_id not in MODES:
        return jsonify({"error": "Invalid mode selected."}), 400

    mode = MODES[mode_id]

    try:
        client = Groq(api_key=api_key)

        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # fast & powerful Groq model
            max_tokens=1024,
            messages=[
                {"role": "system", "content": mode["system"]},
                {"role": "user",   "content": f'Explain this topic in your unique style: "{topic}"'}
            ]
        )

        explanation = chat_completion.choices[0].message.content
        return jsonify({"explanation": explanation, "mode": mode["label"], "emoji": mode["emoji"]})

    except Exception as e:
        err = str(e).lower()
        if "auth" in err or "api key" in err or "invalid" in err:
            return jsonify({"error": "Invalid Groq API key. Please check and try again."}), 401
        elif "rate" in err:
            return jsonify({"error": "Rate limit reached. Please wait a moment and try again."}), 429
        else:
            return jsonify({"error": f"Something went wrong: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)