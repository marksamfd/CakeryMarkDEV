# ----------- backend api Dockerfile -----------
FROM python:3.10

RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    gcc \
    && apt-get clean


WORKDIR /app

# app folder
COPY . /app

# Copy .env file
COPY app/.env /app/.env

#  dependencies explicitly (flassgger haad many issues so let it like this)
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN pip install Flask flasgger==0.9.7.1

# packs
RUN pip list

# port 5000
EXPOSE 5000

# Environment Variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# run
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]

# build the image then make a container