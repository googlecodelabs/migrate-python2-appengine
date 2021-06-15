FROM python:3-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT exec gunicorn -b :$PORT -w 2 main:app
