FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y libaio1

RUN pip install --no-cache-dir -r requirements.txt

COPY .env /app/.env

CMD ["python", "src/main.py"]
