FROM python:3.9-slim-buster

WORKDIR /app
ENV PYTHONPATH /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY /app ./app
COPY default/nanuq.yml .

ENTRYPOINT [ "python3", "/app/app/main.py"]
CMD ["-f", "nanuq.yml"]