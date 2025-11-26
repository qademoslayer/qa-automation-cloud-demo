from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/api/mock")
def mock():
    return jsonify({"message": "mock working"}), 200

if __name__ == "__main__":
    app.run(port=5001)
