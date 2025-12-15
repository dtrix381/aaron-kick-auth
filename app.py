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
        "https://kick.com/oauth/authorize"
        "?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        "&scope=user:read"
    )
    return redirect(auth_url)

@app.route("/auth/kick/callback")
def kick_callback():
    code = request.args.get("code")
    return jsonify({"code": code})

