FROM python:3.11-slim

# Create working directory
WORKDIR /code

# Copy requirements.txt
COPY ./requirements.txt /code/requirements.txt

# Install Python dependencies
RUN apt update -y
RUN apt install build-essential pkgconf -y
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application files
COPY ./icon_rhizome_dev /code/icon_rhizome_dev

# Start application
CMD ["gunicorn", "icon_rhizome_dev.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]