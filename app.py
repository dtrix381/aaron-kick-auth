import os
import base64
import requests
from flask import Flask, redirect, request, jsonify

app = Flask(__name__)

KICK_CLIENT_ID = os.getenv("KICK_CLIENT_ID")
KICK_CLIENT_SECRET = os.getenv("KICK_CLIENT_SECRET")
REDIRECT_URI = "https://aaron-kick-auth.onrender.com/auth/kick/callback"

AUTH_URL = "https://id.kick.com/oauth/authorize"
TOKEN_URL = "https://id.kick.com/oauth/token"


@app.route("/")
def home():
    return "Kick OAuth Service Running"


@app.route("/auth/kick/login")
def kick_login():
    params = {
        "client_id": KICK_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "user:read channel:read"
    }

    query = "&".join([f"{k}={v}" for k, v in params.items()])
    return redirect(f"{AUTH_URL}?{query}")


@app.route("/auth/kick/callback")
def kick_callback():
    code = request.args.get("code")

    if not code:
        return "No code received", 400

    credentials = f"{KICK_CLIENT_ID}:{KICK_CLIENT_SECRET}"
    auth_header = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code != 200:
        return jsonify({
            "error": "Token exchange failed",
            "details": response.text
        }), 400

    token_data = response.json()
    return jsonify(token_data)
