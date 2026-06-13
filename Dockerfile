FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install pip dependencies if requirements.txt exists
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt || true

# Copy project
COPY . /app

EXPOSE 8000

# Simple development command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]