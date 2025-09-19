from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Hej fra min online server! 🎉"

# /rapport kan nu modtage data via POST
@app.route("/rapport", methods=["POST"])
def rapport():
    data = request.get_json() or {}

    # læs tal fra input (eller brug standard hvis ikke angivet)
    tal = data.get("tal", 10000)

    # lav en beregning baseret på input
    total = sum(i * i for i in range(1, tal + 1))

    return jsonify({
        "status": "ok",
        "modtaget_tal": tal,
        "resultat": total
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
