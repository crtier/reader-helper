from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

HUGGINGFACE_API_KEY = "replace with your API-key"
MODEL_NAME = "facebook/bart-large-cnn"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

@app.route("/")
def home():
    return render_template("front.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.json
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        response = requests.post(API_URL, headers=headers, json={"inputs": text})

        if response.status_code == 200:
            result = response.json()
            summary = result[0]["summary_text"]
            return jsonify({"summary": summary})
        else:
            return jsonify({"error": "Failed to fetch summary", "details": response.json()}), response.status_code

    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
