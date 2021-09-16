FROM python:2-slim
WORKDIR /app
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT exec gunicorn -b :$PORT -w 2 main:app
