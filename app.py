from flask import Flask, jsonify, request
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return "Hej fra min online server! 🎉"

@app.route("/rapport", methods=["GET", "POST"])
def rapport():
    if request.method == "POST":
        data = request.get_json(force=True)
        tal = data.get("tal", [])
        total = sum(int(x) for x in tal)
        return jsonify({
            "status": "ok",
            "beregning": f"sum({tal})",
            "resultat": total
        })
    else:
        total = sum(i * i for i in range(1, 1001))
        return jsonify({
            "status": "ok",
            "beregning": "sum(i^2) for i=1..1000",
            "resultat": total
        })

# NYT ENDPOINT: /cluster
@app.route("/cluster", methods=
