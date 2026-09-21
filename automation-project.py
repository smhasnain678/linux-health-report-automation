import paramiko
from pathlib import Path
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import html
import os


# Linux machine details
hostname = "192.168.56.103"
username = "muhammad-hasnain"
password = os.environ["VM_PASSWORD"]

# Windows folder where report will be saved
output_folder = Path(r"J:\smhasnain\Al-Nafi\DCCS\Python Deep Dive\Automation-Project\Linux-Reports")
output_folder.mkdir(parents=True, exist_ok=True)

# Report filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
report_file = output_folder / f"linux_health_{timestamp}.html"

# SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def build_html_report(output, hostname, timestamp):

    # Escape original output
    safe_output = html.escape(output)

    # ---------- Section headings ----------
    safe_output = safe_output.replace(
        "CPU Usage:\n",
        '<span class="section-title">CPU Usage</span>'
    )
    safe_output = safe_output.replace(
        "Memory Usage:\n",
        '<span class="section-title">Memory Usage</span>'
    )
    safe_output = safe_output.replace(
        "Disk Usage:\n",
        '<span class="section-title">Disk Usage</span>'
    )
    safe_output = safe_output.replace(
        "Logged-in Users:\n",
        '<span class="section-title">Logged-in Users</span>'
    )

    # ---------- Normal messages (green) ----------
    safe_output = safe_output.replace(
        "CPU Usage is normal",
        '<span class="normal-text">✓ CPU Usage is normal</span>'
    )
    safe_output = safe_output.replace(
        "Memory Usage is normal",
        '<span class="normal-text">✓ Memory Usage is normal</span>'
    )
    safe_output = safe_output.replace(
        "Disk Usage is normal",
        '<span class="normal-text">✓ Disk Usage is normal</span>'
    )

    # ---------- Warnings (red) ----------
    safe_output = safe_output.replace(
        "WARNING: CPU Usage is above 80%!",
        '<span class="warning-text">⚠ WARNING: CPU Usage is above 80%!</span>'
    )
    safe_output = safe_output.replace(
        "WARNING: Memory Usage is above 80%",
        '<span class="warning-text">⚠ WARNING: Memory Usage is above 80%</span>'
    )
    safe_output = safe_output.replace(
        "WARNING: Disk Usage is above 80%!",
        '<span class="warning-text">⚠ WARNING: Disk Usage is above 80%!</span>'
    )

    # ---------- Main title ----------
    safe_output = safe_output.replace(
        "SYSTEM HEALTH MONITOR",
        '<span class="monitor-title">SYSTEM HEALTH MONITOR</span>'
    )

    html_report = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Linux System Health Report</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 40px 20px;
    font-family: Arial, Helvetica, sans-serif;
    background: #f3f4f6;
    color: #111827;
}}

.container {{
    max-width: 1100px;
    margin: auto;
}}

/* ===== HEADER ===== */

.header {{
    background: linear-gradient(135deg, #111827, #1f2937);
    color: white;
    padding: 35px;
    border-radius: 16px;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}}

.header h1 {{
    margin: 0 0 15px 0;
    font-size: 32px;
    color: #facc15;          /* yellow heading */
}}

.header p {{
    margin: 6px 0;
    color: #d1d5db;
    font-size: 15px;
}}

/* ===== REPORT BOX ===== */

.report {{
    background: #ffffff;
    border-radius: 16px;
    padding: 30px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
}}

/* ===== MAIN TITLE ===== */

.monitor-title {{
    display: block;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    color: #22c55e;
    margin-bottom: 10px;
}}

/* ===== SECTION HEADINGS ===== */

.section-title {{
    display: block;
    font-size: 18px;
    font-weight: bold;
    color: #facc15;
    border-left: 4px solid #facc15;
    padding-left: 10px;
    margin: 8px 0;
}}

/* ===== NORMAL (GREEN) ===== */

.normal-text {{
    display: inline-block;
    color: #15803d;
    background: #dcfce7;
    font-weight: bold;
    padding: 6px 12px;
    border-radius: 6px;
}}

/* ===== WARNING (RED) ===== */

.warning-text {{
    display: inline-block;
    color: #ffffff;
    background: #dc2626;
    font-weight: bold;
    padding: 6px 12px;
    border-radius: 6px;
}}

/* ===== RAW OUTPUT ===== */

pre {{
    background: #111827;
    color: #e5e7eb;
    padding: 25px;
    border-radius: 12px;
    overflow-x: auto;
    white-space: pre-wrap;
    line-height: 1.6;
    font-size: 14px;
}}

/* ===== RESPONSIVE ===== */

@media (max-width: 700px) {{
    body {{ padding: 20px 10px; }}
    .header {{ padding: 25px; }}
    .header h1 {{ font-size: 26px; }}
    .report {{ padding: 20px; }}
}}

</style>
</head>

<body>
<div class="container">

    <div class="header">
        <h1>Linux System Health Report</h1>
        <p><b>Server:</b> {hostname}</p>
        <p><b>Report Generated:</b> {timestamp}</p>
    </div>

    <div class="report">
        <pre>{safe_output}</pre>
    </div>

</div>
</body>
</html>
"""

    return html_report

    return html_report

try:
    print("Connecting to Linux machine...")

    ssh.connect(
        hostname=hostname,
        username=username,
        password=password,
        timeout=10
    )

    print("Connected successfully")

    # Run health_monitor.sh on Linux
    command = (
        "cd /home/muhammad-hasnain/System-Health-Monitor && "
        "./health_monitor.sh"
    )

    stdin, stdout, stderr = ssh.exec_command(command)

    # Read command output
    output = stdout.read().decode("utf-8")
    error = stderr.read().decode("utf-8")

    # Add report information
    final_report = (
        f"[Report fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
        f"from {hostname}]\n\n"
        f"{output}"
    )

    # If Linux command produced an error, add it to report
    if error:
        final_report += "\n\n===== ERROR =====\n"
        final_report += error

    # Save report on Windows
    #report_file.write_text(final_report, encoding="utf-8")
    html_report = build_html_report(
        output,
        hostname,
        timestamp
    )

    report_file.write_text(html_report, encoding="utf-8")

    print(f"Report saved successfully:")
    print(report_file)

    # Send report by email
    msg = MIMEMultipart()
    my_mail = "devopsautomation076@gmail.com"
    mail_password = os.environ["GMAIL_APP_PASSWORD"]
    msg['Subject'] = f"Linux System Health Report - {timestamp}"
    msg['From'] = my_mail
    msg['To'] = my_mail
    body = """
    <html>
    <body>
        <h2>Linux System Health Report</h2>
        <p>Hi Team,</p>
        <p>
            This is an automated Linux System Health Report
            generated using Python.
        </p>
        <p>
            The complete system health report is attached
            with this email.
        </p>
        <br>
        <p>
            <b>Server:</b> 192.168.56.103<br>
            <b>Report Time:</b> %s
        </p>
        <p>Regards,<br>
        <b>DevOps Automation</b></p>
    </body>
    </html>
    """ % timestamp
    msg.attach(MIMEText(body, 'html'))
    # Attachment section
    with open(report_file, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{report_file.name}"')
        msg.attach(part)
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_mail, password=mail_password)
    connection.send_message(msg)
    connection.close()
    print("Mail has been sent")



finally:
    ssh.close()
    print("SSH connection closed")