import os
os.environ["FLASK_APP"] = "main.py"

from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hej fra min online server! 🎉"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

