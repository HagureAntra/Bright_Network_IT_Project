from flask import Flask, request, render_template_string, jsonify, render_template, send_from_directory, Response
import pandas as pd
import os
import csv
from io import StringIO
import requests

app = Flask(__name__)

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'log', 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
LATEST_RESULTS = []

# --- Ensure uploads folder exists ---
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Helper to validate file extension ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Log analyzer function ---
def analyze_log(filepath):
    suspicious = []
    try:
        df = pd.read_csv(filepath, sep=None, engine='python')
        print("[DEBUG] Columns detected:", df.columns.tolist())
        ip_counts = df['ip'].value_counts()
        print("[DEBUG] IP counts:\n", ip_counts)
        suspicious = ip_counts[ip_counts > 2].index.tolist()
        print("[DEBUG] Suspicious IPs:", suspicious)
    except Exception as e:
        error_message = f"Error processing log: {e}"
        print("[ERROR]", error_message)
        suspicious.append(error_message)
    return suspicious

# --- Upload form ---
@app.route('/')
def upload_form():
    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Upload Log File</title>
        <link rel="icon" href="/favicon.ico" type="image/x-icon">
        <style>
            body {
                background-color: #121212;
                color: #f0f0f0;
                font-family: 'Segoe UI', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .upload-box {
                background-color: #1e1e1e;
                border: 1px solid #333;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(255, 0, 0, 0.2);
                text-align: center;
                width: 90%;
                max-width: 500px;
            }
            h1 {
                color: #ff6b6b;
                margin-bottom: 30px;
            }
            input[type=file] {
                margin: 20px 0;
                background-color: #2a2a2a;
                border: 1px solid #444;
                padding: 10px;
                color: #f0f0f0;
                border-radius: 6px;
            }
            input[type=submit] {
                background-color: #ff6b6b;
                border: none;
                padding: 10px 20px;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            input[type=submit]:hover {
                background-color: #ff4b4b;
            }
            a {
                color: #ff6b6b;
                display: block;
                margin-top: 20px;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="upload-box">
            <h1>Upload Log File</h1>
            <form method="post" enctype="multipart/form-data" action="/upload">
                <input type="file" name="file" required><br>
                <input type="submit" value="Upload & Analyze">
            </form>
            <a href="/report">View Last Report</a>
        </div>
    </body>
    </html>
    ''')

# --- Upload and analyze log ---
@app.route('/upload', methods=['POST'])
def upload_file():
    global LATEST_RESULTS
    file = request.files['file']
    if file and allowed_file(file.filename):
        from typing import cast

        filename = cast(str, file.filename)  # Tell linter: I'm sure this is a string
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save file safely
        file.save(filepath)

        # Analyze log
        LATEST_RESULTS = analyze_log(filepath)

        return f"Uploaded and analyzed! Found {len(LATEST_RESULTS)} suspicious IPs.<br><a href='/report'>View Report</a>"
    return "Invalid file format. Must be .txt, .log, or .csv"


# --- GeoIP lookup ---
GEOIP_CACHE = {}

def get_geoip(ip):
    if ip in GEOIP_CACHE:
        return GEOIP_CACHE[ip]
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
        data = response.json()
        if data['status'] == 'success':
            location = f"{data['country']} ({data['regionName']})"
        else:
            location = "Unknown"
    except Exception:
        location = "Lookup failed"
    GEOIP_CACHE[ip] = location
    return location

# --- Report page ---
@app.route('/report')
def show_report():
    enriched_results = []
    for ip in LATEST_RESULTS:
        location = get_geoip(ip)
        enriched_results.append(f"{ip} — {location}")
    return render_template('report.html', results=enriched_results)

# --- CSV Download ---
@app.route('/download/csv')
def download_csv():
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Suspicious IPs'])
    for ip in LATEST_RESULTS:
        cw.writerow([ip])
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=suspicious_ips.csv"}
    )

# --- API Endpoint ---
@app.route('/api/report')
def api_report():
    return jsonify({"suspicious_ips": LATEST_RESULTS})

# --- Favicon ---
@app.route('/favicon.ico')
def favicon():
    icon_path = os.path.join(app.root_path, 'favicon.ico')
    if os.path.exists(icon_path):
        return send_from_directory(
            app.root_path,
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )
    else:
        return "Favicon not found", 404

# --- Start App ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
