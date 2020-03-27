#!/bin/sh

# this script is used to boot a Docker container

source venv/bin/activate

nohup python scheduler.py start-flower &

exec python scheduler.py start-worker
