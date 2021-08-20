FROM python:3.8

ARG COMMIT_HASH=main

RUN pip install gunicorn

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Installing vocabulary_srv from Github (and not from the local project folder)
RUN pip install git+https://github.com/robertradnai/vocabulary-srv.git@$COMMIT_HASH#egg=vocabulary_srv

ENV FLASK_APP="vocabulary_srv:create_app"
ENV FLASK_ENV=production

CMD gunicorn -w 4 -b 127.0.0.1:$PORT "$FLASK_APP"
