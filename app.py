from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Hej fra min online server! 🎉"

# NYT ENDPOINT: /rapport
# Nu tillader vi både GET (browser) og POST (når vi senere sender data)
@app.route("/rapport", methods=["GET", "POST"])
def rapport():
    # Hvis det er et POST-kald med data
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
        # Simpel GET demo-beregning
        total = sum(i * i for i in range(1, 1001))
        return jsonify({
            "status": "ok",
            "beregning": "sum(i^2) for i=1..1000",
            "resultat": total
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
