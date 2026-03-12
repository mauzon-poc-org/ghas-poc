import sqlite3
import subprocess
from flask import Flask, request

app = Flask(__name__)

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    conn = sqlite3.connect('db.sqlite3')
    # SQL Injection - CodeQL vai detectar isso
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return conn.execute(query).fetchall()

@app.route('/ping')
def ping():
    host = request.args.get('host')
    # Command Injection - CodeQL vai detectar isso
    result = subprocess.run(f"ping -c 1 {host}", shell=True)
    return str(result)
