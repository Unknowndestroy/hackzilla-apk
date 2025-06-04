# server.py

from flask import Flask, request, jsonify

app = Flask(__name__)

# İlk başta hiçbir komut yok, saf gibi.
current_command = {
    "lock_screen": False,
    "message": ""
}

@app.route("/get_command", methods=["GET"])
def get_command():
    """
    Telefon her çektiğinde burası atanacak.
    Eğer lock_screen True ise ekranı full kapla, mesajı bas.
    """
    return jsonify(current_command)

@app.route("/set_command", methods=["POST"])
def set_command():
    """
    Sen GUI'den gönderdiğinde burası çalışır.
    JSON bekler: {"lock_screen": bool, "message": "string"}
    """
    data = request.get_json()
    if data is None:
        return jsonify({"status": "error", "msg": "JSON at la amk!"}), 400

    # Gelen verileri güncelle
    lock = data.get("lock_screen")
    msg = data.get("message")

    # Hatalı gönderme kontrolü
    if lock is None or not isinstance(lock, bool):
        return jsonify({"status": "error", "msg": "lock_screen yanlış türde!"}), 400
    if msg is None or not isinstance(msg, str):
        return jsonify({"status": "error", "msg": "message yanlış türde!"}), 400

    current_command["lock_screen"] = lock
    current_command["message"] = msg

    return jsonify({"status": "success", "command": current_command})

if __name__ == "__main__":
    # Host her yerden erişilsin diye 0.0.0.0, port 5000 sabit
    app.run(host="0.0.0.0", port=5000)
