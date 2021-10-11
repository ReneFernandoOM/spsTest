FROM python:slim


COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn


COPY app app
COPY migrations migrations
COPY app_entry.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app_entry.py


EXPOSE 8090
ENTRYPOINT ["./boot.sh"]