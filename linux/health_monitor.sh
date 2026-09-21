#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$SCRIPT_DIR/logs"
LOG_FILE="$SCRIPT_DIR/logs/system_health_$(date +%Y-%m-%d_%H-%M-%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "=============================="
echo "    SYSTEM HEALTH MONITOR"
echo "=============================="

# Basic System Information
echo "Hostname   : $(hostname)"
echo "Date       : $(date)"
echo "Uptime     : $(uptime -p)"

echo "=============================="

# CPU Usage
echo "CPU Usage:"

CPU_USAGE=$(top -bn1 | awk -F',' '/Cpu\(s\)/ {
        for (i = 1; i <= NF; i++){
                if ($i ~ /id/){
                        gsub(/[^0-9.]/, "", $i)
                        print 100 - $i
                }
        }
}')

CPU_USAGE=${CPU_USAGE%.*}

echo "CPU Usage: $CPU_USAGE%"

if [ "$CPU_USAGE" -gt 80 ]; then
        echo "WARNING: CPU Usage is above 80%!"
else
        echo "CPU Usage is normal"
fi

echo "=============================="


# Memory Usage
echo "Memory Usage:"

free -h

# Memory Warning
MEMORY_USAGE=$(free | awk '/Mem:/ {printf "%.0f", $3/$2 * 100}')

echo "Memory Usage: $MEMORY_USAGE%"

if [ "$MEMORY_USAGE" -gt 80 ]; then
        echo "WARNING: Memory Usage is above 80%"
else
        echo "Memory Usage is normal"
fi

echo "=============================="


# Disk Usage
echo "Disk Usage:"

df -h /

# Disk Warning
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')

if [ "$DISK_USAGE" -gt 80 ]; then
        echo "WARNING: Disk Usage is above 80%!"
else
        echo "Disk Usage is normal"
fi

echo "=============================="


# Logged-in Users
echo "Logged-in Users:"

w

echo "=============================="