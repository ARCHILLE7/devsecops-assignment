from flask import Flask, request, jsonify
import sqlite3
import subprocess
import hashlib
import os
import shlex
import ast




app = Flask(__name__)


# SECRET HARDCODÉ (mauvaise pratique)
# Solution 1 
SECRET_KEY = os.getenv("SECRET_KEY" , "API-KEY-123456")

# Logging non sécurisé
# Solution 2 + Solution 3 
# logging.basicConfig(level=logging.DEBUG)


#     # SQL Injection
#     conn = sqlite3.connect("users.db")
#     cursor = conn.cursor()
#     query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
#     cursor.execute(query)


#     if cursor.fetchone():
#         return {"status": "authenticated"}
#     return {"status": "denied"}


@app.route("/auth", methods=["POST"])
def auth():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password_hash))

    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify({"status": "success", "user": username})

    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

# Solution 4 
@app.route("/exec", methods=["POST"])
def exec_cmd():
    # cmd = request.json.get("cmd")
    # # Command Injection
    # output = subprocess.check_output(cmd, shell=True)
    # return {"output": output.decode()}
    data = request.get_json()
    host = data.get("host", "")
    if not host.replace(".", "").isalnum():
        return jsonify({"error": "Invalid host"}), 400
    cmd = ["ping", "-c", "1", host]
    try:
        output = subprocess.check_output(cmd, timeout=3)
        return jsonify({"output": output.decode()})
    except subprocess.CalledProcessError:
        return jsonify({"error": "Ping failed"}), 500

#  Solution 5 
@app.route("/deserialize", methods=["POST"])
def deserialize():
    # data = request.data
    # # Désérialisation dangereuse
    # obj = pickle.loads(data)
    # return {"object": str(obj)}
    data = request.get_json()
    return {"object": data}


# Solution 6
@app.route("/encrypt", methods=["POST"])
def encrypt():
    # text = request.json.get("text", "")
    # Chiffrement faible
    # hashed = hashlib.md5(text.encode()).hexdigest()
    # return {"hash": hashed}

    data = request.get_json()
    pwd = data.get("password")  
    hashed = hashlib.sha256(pwd.encode()).hexdigest()
    return jsonify({"sha256": hashed})

# Solution 7
@app.route("/file", methods=["POST"])
def read_file():
    # filename = request.json.get("filename")
    # # Path Traversal
    # with open(filename, "r") as f:
    #     return {"content": f.read()}
    data = request.get_json()
    filename = data.get("filename")

    BASE_DIR = "files"
    safe_path = os.path.join(BASE_DIR, os.path.basename(filename))

    if not os.path.isfile(safe_path):
        return jsonify({"error": "File not found"}), 404

    with open(safe_path, "r") as f:
        content = f.read()

    return jsonify({"content": content})


# Solution 8
@app.route("/debug", methods=["GET"])
def debug():
    
    return jsonify({"debug": False}), 403

# Solution 9
@app.route("/log", methods=["GET"])
def log_data():
    # data = request.json
    # # Log Injection
    # logging.info(f"User input: {data}")
    # return {"status": "logged"}
    return jsonify({"status": "Logged"})

# Solution 10 
if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(host="0.0.0.0", port=5000, debug=False)