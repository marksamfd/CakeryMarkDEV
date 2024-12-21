FROM python:3.12-slim

# ---- backend ----
WORKDIR /app

COPY . /app

COPY app/.env /app/.env

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_ENV=development


CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
