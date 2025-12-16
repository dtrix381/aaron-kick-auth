from flask import Flask, redirect, request
import os
import requests

app = Flask(__name__)

KICK_CLIENT_ID = os.environ.get("KICK_CLIENT_ID")
KICK_CLIENT_SECRET = os.environ.get("KICK_CLIENT_SECRET")
KICK_REDIRECT_URI = "https://aaron-kick-auth.onrender.com/auth/kick/callback"

@app.route("/")
def home():
    return "Kick OAuth Service Running"

@app.route("/healthz")
def health():
    return "ok"

@app.route("/auth/kick/login")
def kick_login():
    if not KICK_CLIENT_ID:
        return "Missing KICK_CLIENT_ID", 500

    auth_url = (
        "https://id.kick.com/oauth/authorize"
        "?response_type=code"
        f"&client_id={KICK_CLIENT_ID}"
        f"&redirect_uri={KICK_REDIRECT_URI}"
        "&scope=user:read"
    )

    print("🔗 Redirecting to:", auth_url)
    return redirect(auth_url)


@app.route("/auth/kick/callback")
def kick_callback():
    print("✅ Kick callback hit")
    print("🔎 Query params:", dict(request.args))

    code = request.args.get("code")
    if not code:
        return "❌ No code provided", 400

    if not KICK_CLIENT_SECRET:
        return "❌ Missing KICK_CLIENT_SECRET", 500

    token_url = "https://kick.com/oauth/token"

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": KICK_CLIENT_ID,
        "client_secret": KICK_CLIENT_SECRET,
        "redirect_uri": KICK_REDIRECT_URI,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    resp = requests.post(token_url, data=data, headers=headers, timeout=10)

    if resp.status_code != 200:
        print("❌ Token exchange failed:", resp.text)
        return f"Token exchange failed: {resp.text}", 400

    token_data = resp.json()

    print("\n=== ✅ KICK OAUTH TOKEN RECEIVED ===")
    print(token_data)
    print("=================================\n")

    return "✅ Kick OAuth successful! You can close this page."
