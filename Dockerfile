FROM python:3.8

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

ENV FLASK_APP="vocabulary_srv:create_app(None, '${SCRIPTPATH}/testconfig.py')"
ENV FLASK_ENV=development

CMD ["flask", "init-db"]
CMD ["flask", "run"]