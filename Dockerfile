FROM python:3-alpine

ENV PYTHONUNBUFFERED=1
COPY src/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
WORKDIR /app
COPY src/ .
COPY templates/ ./templates

CMD ["python", "/app/app.py"]
