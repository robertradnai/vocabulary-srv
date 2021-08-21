FROM python:3.8

ARG COMMIT_HASH=main

WORKDIR /app

RUN pip install gunicorn

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY vocabulary_srv vocabulary_srv
COPY setup.py setup.py
RUN pip install -e .

ENV FLASK_APP="vocabulary_srv:create_app()"
ENV FLASK_ENV=production

CMD gunicorn -w 4 -b 127.0.0.1:$PORT "$FLASK_APP"
