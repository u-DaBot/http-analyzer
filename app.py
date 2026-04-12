from flask import Flask, request, jsonify, render_template
from DA_1 import download

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "No URL"}), 400

    if not url.startswith("http"):
        url = "https://" + url

    try:
        steps = download(url)
        return jsonify({"steps": steps})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)