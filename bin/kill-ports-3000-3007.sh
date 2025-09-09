#!/usr/bin/env bash
set -euo pipefail

start=3000
end=3007

found_any=false
for port in $(seq "$start" "$end"); do
  if command -v lsof >/dev/null 2>&1; then
    pids=$(lsof -ti tcp:"$port" 2>/dev/null || true)
  else
    pids=""
  fi

  if [ -n "${pids:-}" ]; then
    echo "Port $port -> PIDs: $pids (SIGTERM)"
    kill $pids 2>/dev/null || true
    sleep 0.2

    still=""
    if command -v lsof >/dev/null 2>&1; then
      still=$(lsof -ti tcp:"$port" 2>/dev/null || true)
    fi
    if [ -n "$still" ]; then
      echo "Port $port still in use -> PIDs: $still (SIGKILL)"
      kill -9 $still 2>/dev/null || true
    fi

    found_any=true
  fi
done

if ! $found_any; then
  echo "No processes found on ports ${start}-${end}."
fi
