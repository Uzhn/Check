FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY check_task/ .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]