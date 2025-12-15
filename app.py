from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Kick OAuth Service Running"

@app.route("/auth/kick/callback")
def kick_callback():
    return "Kick OAuth callback received"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
