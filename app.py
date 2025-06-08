# Agent Status Tracker - Flask API

# This code tracks PowerShell agents by their hostname and shows their last seen time. Agents that have not been active for over 7 days are removed. Agents seen in the last 2 minutes are considered "connected".

```python
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from threading import Lock

app = Flask(__name__)

agents = {}
agents_lock = Lock()

@app.route('/report-agent', methods=['POST'])
def report_agent():
    hostname = request.json.get("hostname")
    if not hostname:
        return jsonify({"error": "Missing hostname"}), 400

    with agents_lock:
        agents[hostname] = datetime.utcnow()

    return jsonify({"status": "OK"})

@app.route('/get-agents', methods=['GET'])
def get_agents():
    now = datetime.utcnow()
    connected = []
    disconnected = []

    with agents_lock:
        # Clean up agents not seen for more than 7 days
        old = [h for h, t in agents.items() if now - t > timedelta(days=7)]
        for h in old:
            del agents[h]

        for h, t in agents.items():
            status = "connected" if now - t < timedelta(minutes=2) else "disconnected"
            entry = {"hostname": h, "last_seen": t.isoformat() + "Z", "status": status}
            if status == "connected":
                connected.append(entry)
            else:
                disconnected.append(entry)

    return jsonify({"connected": connected, "disconnected": disconnected})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### ✅ Usage Notes
- Agents should send a POST request to `/report-agent` every minute:

```powershell
Invoke-RestMethod -Uri "https://ps-remote-api.onrender.com/report-agent" -Method Post -Body @{hostname=$env:COMPUTERNAME} | Out-Null
```

- You can get agent status at:
```powershell
Invoke-RestMethod "https://ps-remote-api.onrender.com/get-agents"
```
