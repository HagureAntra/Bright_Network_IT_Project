"""
Bright Networks IT Project - Traffic Analysis & Bot Mitigation

Overview:
This project analyzes synthetic server log data to detect suspicious or bot-like traffic patterns, such as high request frequency and non-browser user agents. It flags potential bot IPs and outputs them for further action.

How to Run:

1. Make sure Python 3.10 or later is installed.
2. Open a terminal and navigate to this project folder.
3. (Optional) Create and activate a virtual environment.
4. Install required dependencies:
   pip install -r requirements.txt
5. Run the analysis script:
   python analyze_logs.py

What Happens:

- The script reads `synthetic_logs.txt`
- It identifies suspicious traffic based on request frequency and user agent
- It generates a file: `flagged_ips.txt` containing potentially harmful IPs

Included Files:

- analyze_logs.py ................... Main script for traffic analysis
- synthetic_logs.txt ................ Sample log file
- flagged_ips.txt ................... Output list of flagged IPs
- requirements.txt .................. Python libraries needed
- traffic_bot_analysis_report.docx .. Final report with findings and recommendations
- README.txt ........................ This file

Assumptions:

- Synthetic logs are used due to absence of real logs
- Project is designed to be cost-effective for small teams
- The report outlines methods that can scale affordably

Author: [Your Name]
For: Bright Networks - IT & Software Experience Project

"""