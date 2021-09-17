FROM python:3.8

COPY requirements.txt .
COPY config.json .

RUN pip install -r requirements.txt

COPY src/ ./src
COPY stockfish .

CMD [ "python", "src/main.py"]
