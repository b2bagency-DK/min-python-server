from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Hej fra min online server! 🎉"

# NYT ENDPOINT: /rapport
# Simpel demo-beregning så vi kan teste, at endpointet virker.
# (Vi gør det “rigtigt” med baggrundsjob senere.)
@app.route("/rapport", methods=["GET"])
def rapport():
    # lille, men synlig beregning
    total = sum(i * i for i in range(1, 10001))  # 1^2 + 2^2 + ... + 10000^2
    return jsonify({
        "status": "ok",
        "beregning": "sum(i^2) for i=1..10000",
        "resultat": total
    })

if __name__ == "__main__":
    # Render kører via 'python app.py', så dette er fint til lokal kørsel også.
    app.run(host="0.0.0.0", port=10000)
