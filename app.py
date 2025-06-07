# ps_remote_api - Flask-based command server

from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# אחסון פשוט בקובץ (אפשר להחליף ל-DB)
COMMANDS_FILE = "commands.json"

# טען פקודות קיימות אם יש
if not os.path.exists(COMMANDS_FILE):
    with open(COMMANDS_FILE, "w") as f:
        json.dump({}, f)

def load_commands():
    with open(COMMANDS_FILE, "r") as f:
        return json.load(f)

def save_commands(data):
    with open(COMMANDS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# === נקודת קבלת פקודה למחשב מסוים ===
@app.route("/get-command", methods=["GET"])
def get_command():
    hostname = request.args.get("hostname")
    if not hostname:
        return jsonify({"error": "Missing hostname"}), 400
    data = load_commands()
    command = data.pop(hostname, None)
    save_commands(data)  # הסר אחרי שליחה
    return jsonify({"command": command})

# === נקודת קבלת תוצאה מה-Agent ===
@app.route("/report-result", methods=["POST"])
def report_result():
    content = request.json
    print("[RESULT]", json.dumps(content, indent=2))
    return "OK"

# === שליחת פקודה למחשב ===
@app.route("/send-command", methods=["POST"])
def send_command():
    content = request.json
    hostname = content.get("hostname")
    command = content.get("command")
    if not hostname or not command:
        return jsonify({"error": "Missing hostname or command"}), 400
    data = load_commands()
    data[hostname] = command
    save_commands(data)
    return jsonify({"status": "command set"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    app.run(host="0.0.0.0", port=port)
