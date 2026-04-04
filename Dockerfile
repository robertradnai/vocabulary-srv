FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY vocabulary_srv ./vocabulary_srv
COPY tmp/vocabulary ./vocabulary

ENV FLASK_APP="vocabulary_srv:create_app()"
ENV FLASK_ENV=production

CMD gunicorn -w 4 -b 0.0.0.0:$PORT "$FLASK_APP"
