# Use the official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn psycopg2-binary

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run the Django app via Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bank_reconciliation.wsgi:application"]
