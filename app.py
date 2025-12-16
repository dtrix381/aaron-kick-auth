from flask import Flask, redirect, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Kick OAuth Service Running"

@app.route("/healthz")
def health():
    return "ok"

@app.route("/auth/kick/login")
def kick_login():
    client_id = os.environ["KICK_CLIENT_ID"]
    redirect_uri = "https://aaron-kick-auth.onrender.com/auth/kick/callback"

    auth_url = (
        "https://id.kick.com/oauth/authorize"
        "?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        "&scope=user:read"
    )
    return redirect(auth_url)

@app.route("/auth/kick/callback")
def kick_callback():
    print("✅ Kick callback hit")
    print("Query params:", request.args)

    code = request.args.get("code")
    if not code:
        return "No code provided", 400

    client_id = os.environ["KICK_CLIENT_ID"]
    client_secret = os.environ["KICK_CLIENT_SECRET"]
    redirect_uri = "https://aaron-kick-auth.onrender.com/auth/kick/callback"

    # ✅ Updated token URL
    token_url = "https://kick.com/oauth/token"

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    resp = requests.post(token_url, data=data, headers=headers)
    if resp.status_code != 200:
        return f"Token exchange failed: {resp.text}", 400

    token_data = resp.json()

    print("=== KICK OAUTH TOKEN ===")
    print(token_data)
    print("========================")

    return "Kick OAuth successful! You can close this page."


