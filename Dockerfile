# ----------- backend api Dockerfile -----------
    FROM python:3.10

    RUN apt-get update && apt-get install -y \
        libpq-dev \
        build-essential \
        gcc \
        && apt-get clean
    
    WORKDIR /app
    
    COPY . /app
    
    # Install dependencies
    RUN pip install --upgrade pip
    COPY requirements.txt /app/
    RUN pip install -r requirements.txt
    RUN pip install gunicorn Flask flasgger==0.9.7.1
    
    # list installed packages
    RUN pip list
    
    # Expose port
    EXPOSE 5000
    
    # environment variables
    ENV FLASK_APP=run.py
    ENV FLASK_ENV=production
    
    
    CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
    