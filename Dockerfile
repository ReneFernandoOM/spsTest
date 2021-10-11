FROM python:slim

RUN useradd spstest

WORKDIR /home/spstest

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY app_entry.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R spstest:spstest ./
USER spstest

EXPOSE 8090
ENTRYPOINT ["./boot.sh"]