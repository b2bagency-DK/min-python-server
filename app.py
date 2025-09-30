from flask import Flask, jsonify, request
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return "Hej fra min online server! 🎉"

# Demo-endpoint fra før (kan blive)
@app.route("/rapport", methods=["GET", "POST"])
def rapport():
    if request.method == "POST":
        data = request.get_json(force=True)
        tal = data.get("tal", [])
        total = sum(int(x) for x in tal)
        return jsonify({"status": "ok", "beregning": f"sum({tal})", "resultat": total})
    total = sum(i * i for i in range(1, 1001))
    return jsonify({"status": "ok", "beregning": "sum(i^2) for i=1..1000", "resultat": total})

# Simpelt cluster-endpoint (fra før)
@app.route("/cluster", methods=["POST"])
def cluster_simple():
    data = request.get_json(force=True)
    points = np.array(data.get("points", []), dtype=float)
    if points.size == 0:
        return jsonify({"status": "error", "msg": "Ingen data modtaget"}), 400
    kmeans = KMeans(n_clusters=3, random_state=42).fit(points)
    labels = kmeans.labels_.tolist()
    personaer = {}
    for i in range(3):
        mask = (kmeans.labels_ == i)
        center = kmeans.cluster_centers_[i].tolist()
        personaer[f"persona_{i+1}"] = {"center": center, "antal": int(mask.sum())}
    return jsonify({"status": "ok", "personaer": personaer})

# ✅ Nyt: Produktionsagtigt endpoint med labels pr. række + top-forskelle pr. persona
@app.route("/cluster_v2", methods=["POST"])
def cluster_v2():
    """
    Forventet input:
    {
      "feature_names": ["f1","f2","f3"],
      "points": [[...],[...],...],           # samme rækkefølge som feature_names
      "ids": ["row1","row2", ...],           # valgfri; ellers bruger vi indeks
      "k": 3                                 # valgfri; default = 3
    }
    """
    try:
        data = request.get_json(force=True)
        feature_names = data.get("feature_names")
        points = data.get("points")
        ids = data.get("ids")
        k = int(data.get("k", 3))

        if not feature_names or not points:
            return jsonify({"status": "error", "msg": "Kræver 'feature_names' og 'points'"}), 400

        X = np.array(points, dtype=float)  # shape: (n_samples, n_features)
        if X.ndim != 2 or X.shape[1] != len(feature_names):
            return jsonify({"status": "error", "msg": "Shape mismatch mellem feature
