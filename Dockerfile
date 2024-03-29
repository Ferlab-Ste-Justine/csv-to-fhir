FROM python:3.9-slim-buster

WORKDIR /app
ENV PYTHONPATH /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY /app ./app
COPY defaults/qa.yml .
COPY defaults/staging.yml .
COPY defaults/prod.yml .

ENTRYPOINT [ "python3", "/app/app/main.py"]
#CMD ["-f", "qa.yml"]