FROM python:3.6-alpine

ENV FLASK_APP webnews.py
ENV FLASK_DEBUG 1
ENV SECRET_KEY fake
ENV X_RAPID_API_KEY fake
ENV DATABASE_URL sqlite:///app/backend.db
ENV PRODUCTION_MODE no

RUN apk update && apk add --no-cache curl tzdata

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

RUN chown -R fcuser:fcuser ./
USER fcuser

EXPOSE 5000
ENTRYPOINT ["./start.sh"]