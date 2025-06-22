#!/bin/bash
# File: monitor.sh
# Description: Collects system metrics and logs them to a JSON file every 60 seconds

LOG_FILE="/var/log/linux_monitor/metrics.json"
mkdir -p $(dirname "$LOG_FILE")
touch "$LOG_FILE"

while true; do

  TIMESTAMP=$(TZ='Africa/Johannesburg' date -u +"%Y-%m-%dT%H:%M:%SZ")
  CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
  MEM_USED=$(free -m | awk '/Mem:/ { print $3 }')
  MEM_TOTAL=$(free -m | awk '/Mem:/ { print $2 }')
  MEM_PERCENT=$((100 * MEM_USED / MEM_TOTAL))
  DISK=$(df -h / | awk 'NR==2 { print $5 }' | tr -d '%')
  
  echo "{ \"timestamp\": \"$TIMESTAMP\", \"cpu\": $CPU, \"memory\": $MEM_PERCENT, \"disk\": $DISK }" >> "$LOG_FILE"

  # Threshold alerts (simple example)
  if (( $(echo "$CPU > 80" | bc -l) )); then
    echo "[ALERT] High CPU usage: $CPU% at $TIMESTAMP" | mail -s "High CPU Alert" sacramentobaka@email.com
  fi
  if (( MEM_PERCENT > 90 )); then
    echo "[ALERT] High Memory usage: $MEM_PERCENT% at $TIMESTAMP" | mail -s "High Memory Alert" sacramentobaka@email.com
  fi
  if (( DISK > 90 )); then
    echo "[ALERT] High Disk usage: $DISK% at $TIMESTAMP" | mail -s "High Disk Alert" sacramentobaka@email.com
  fi

  sleep 60
done
