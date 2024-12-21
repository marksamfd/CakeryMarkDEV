FROM python:3.12.0-slim

# backend only 
WORKDIR /app

# 
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

# Environment Variables (Optional for local testing)
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

CMD ["gunicorn", "-b", "0.0.0.0:8000", "run:app"]
