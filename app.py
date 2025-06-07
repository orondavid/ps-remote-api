from flask import Flask, request, jsonify

app = Flask(__name__)
commands = {}

@app.route("/set-command", methods=["POST"])
def set_command():
    hostname = request.form.get("hostname")
    command = request.form.get("command")
    if hostname and command:
        commands[hostname] = command
        return jsonify(status="OK")
    return jsonify(status="Missing parameters"), 400

@app.route("/get-command", methods=["GET"])
def get_command():
    hostname = request.args.get("hostname")
    command = commands.get(hostname, "")
    return jsonify(command=command)

@app.route("/set-result", methods=["POST"])
def set_result():
    hostname = request.form.get("hostname")
    result = request.form.get("result")
    print(f"[{hostname}] Result: {result}")
    return jsonify(status="OK")

@app.route("/get-result", methods=["GET"])
def get_result():
    hostname = request.args.get("hostname")
    return jsonify(result=f"Simulated result for {hostname}")
