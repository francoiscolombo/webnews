#!/bin/sh

# this script is used to boot a Docker container

source venv/bin/activate

while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done

flask auth add webnews.jobs
flask auto add webnews.frontend

exec gunicorn -b :5000 --access-logfile - --error-logfile - webnews:app