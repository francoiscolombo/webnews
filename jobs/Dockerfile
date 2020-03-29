FROM python:3.6-alpine

ENV NEWS_API_KEY none
ENV JOBS_APP_TOKEN fake
ENV JOBS_APP_NAME jobs
ENV WEBNEWS_API_BASE_URL http://127.0.0.1:5000/api/v1.0
ENV CELERY_BROKER_URL amqp://guest:guest@127.0.0.1:5672//
ENV CELERY_BACKEND_URL rpc://

RUN adduser -D fcuser

WORKDIR /home/fcuser

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY scheduler.py start.sh ./
RUN chmod a+x start.sh

RUN chown -R fcuser:fcuser ./
USER fcuser

EXPOSE 5555
ENTRYPOINT ["./start.sh"]