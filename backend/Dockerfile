FROM python:3.6-alpine

RUN adduser -D fcuser

WORKDIR /home/fcuser

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY webnews.py config.py start.sh ./
RUN chmod a+x start.sh

ENV FLASK_APP webnews.py

RUN chown -R fcuser:fcuser ./
USER fcuser

EXPOSE 5000
ENTRYPOINT ["./start.sh"]