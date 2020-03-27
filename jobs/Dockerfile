FROM python:3.6-alpine

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