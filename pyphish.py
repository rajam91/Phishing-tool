from flask import Flask, request, render_template, redirect
import csv
from datetime import datetime
import hashlib
import uuid

# app = Flask(__name__)
app = Flask(__name__, template_folder='templates')


ENGAGEMENT_ID = "phishing-tool-01"

@app.route('/')
def home():
    print(f"[{datetime.now()}] Visit from {request.remote_addr}")
    return render_template('mail.html')


@app.route('/submit', methods=['POST'])
def submit():
    username_present = 'username' in request.form
    password_present = 'password' in request.form

    user_agent = request.headers.get('User-Agent', 'unknown')
    ip_address = request.remote_addr
    timestamp = datetime.now().isoformat()

    evidence_string = f"{ip_address}{user_agent}{timestamp}"
    evidence_hash = hashlib.sha256(evidence_string.encode()).hexdigest()

    event = [
        str(uuid.uuid4()),
        ENGAGEMENT_ID,
        ip_address,
        user_agent,
        timestamp,
        username_present,
        password_present,
        evidence_hash
    ]

    with open('pentest_results.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(event)

    print(f"[PENTEST] Form submission captured from {ip_address}")

    return redirect("/thank-you")

@app.route('/thank-you')
def thank_you():
    return "This was part of a security test."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
