# Linux System Health Monitor

An automation project that monitors a Linux machine's health and delivers a styled report by email.

## What it does

1. A Bash script (`linux/health_monitor.sh`) runs on the Linux VM and checks:
   - CPU usage
   - Memory usage
   - Disk usage
   - Logged-in users
   It prints warnings when CPU, memory or disk usage goes above 80%.
2. A Python script (`python/health_report.py`) running on Windows:
   - Connects to the VM over SSH (Paramiko)
   - Runs the Bash script and captures the output
   - Converts it into a styled HTML report
   - Saves the report locally and emails it as an attachment (SMTP)
3. Windows Task Scheduler runs the Python script daily at 12:30 PM.

## Tech stack

- Bash scripting
- Python 3 (paramiko, smtplib, pathlib)
- HTML / CSS
- Windows Task Scheduler
- VirtualBox (Ubuntu VM)

## Project structure

```
linux/health_monitor.sh    # Runs on the Linux VM
python/health_report.py    # Runs on Windows, builds and emails the report
```

## Setup

1. Copy `linux/health_monitor.sh` to the VM and make it executable:
```
   chmod +x health_monitor.sh
```
2. Install the Python dependency on Windows:
```
   pip install paramiko
```
3. Set these environment variables (never hardcode passwords):
   - `VM_PASSWORD`: SSH password of the VM
   - `GMAIL_APP_PASSWORD`: Gmail App Password used for sending mail
4. Update `hostname`, `username` and the output folder in `health_report.py`.
5. Run:
```
   python health_report.py
```

## Sample report

The report shows the header (server and time), then sections for CPU, Memory, Disk and Logged-in Users, with green badges for normal status and red badges for warnings.

## Author

Muhammad Hasnain