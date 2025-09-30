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
@app.route("/cluster", methods=["POST"])
def cluster():
    try:
        data = request.get_json(force=True)
        # Forventet format: { "points": [[x1, y1], [x2, y2], ...] }
        points = np.array(data.get("points", []))
        if len(points) == 0:
            return jsonify({"status": "error", "msg": "Ingen data modtaget"}), 400

        # Lav 3 klynger
        kmeans = KMeans(n_clusters=3, random_state=42).fit(points)
        labels = kmeans.labels_.tolist()

        # Byg persona-resuméer
        personaer = {}
        for i in range(3):
            cluster_points = points[np.array(labels) == i]
            center = kmeans.cluster_centers_[i].tolist()
            personaer[f"persona_{i+1}"] = {
                "center": center,
                "antal": len(cluster_points)
            }

        return jsonify({"status": "ok", "personaer": personaer})

    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
