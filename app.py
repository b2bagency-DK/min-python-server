from flask import Flask, jsonify, request
import threading, time, uuid

app = Flask(__name__)

jobs = {}  # gemmer status og resultater

def tung_beregning(job_id, tal):
    time.sleep(5)  # simulerer en tung beregning (5 sekunders vent)
    resultat = sum(i*i for i in range(1, tal+1))
    jobs[job_id] = {"status": "done", "resultat": resultat}

@app.route("/")
def home():
    return "Hej fra min online server! 🎉"

@app.route("/rapport", methods=["POST"])
def start_job():
    data = request.get_json() or {}
    tal = data.get("tal", 10000)

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "running"}

    t = threading.Thread(target=tung_beregning, args=(job_id, tal))
    t.start()

    return jsonify({"status": "accepted", "job_id": job_id})

@app.route("/status/<job_id>", methods=["GET"])
def job_status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
