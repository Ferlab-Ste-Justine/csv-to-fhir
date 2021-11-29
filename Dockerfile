FROM python:3.9-slim-buster

WORKDIR /app
ENV PYTHONPATH /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY /app ./app
COPY examples/part1.yml .
COPY examples/part2.yml .

ENTRYPOINT [ "python3", "/app/app/main.py"]
CMD ["-f", "part1.yml", "-f", "part2.yml"]