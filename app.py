from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# YOUR API-key Hugging Face
HUGGINGFACE_API_KEY = ""
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

@app.route("/")
def home():
    return render_template("front.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.json
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "Введите текст для обработки"}), 400

        payload = {
            "inputs": text,
            "parameters": {"max_new_tokens": 200, "temperature": 0.7}
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            summary = result[0]["generated_text"]
            return jsonify({"summary": summary})
        else:
            return jsonify({"error": "Ошибка запроса", "details": response.json()}), response.status_code

    except Exception as e:
        return jsonify({"error": "Произошла ошибка", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
