FROM mcr.microsoft.com/devcontainers/python:3.12

WORKDIR /workspace

# Copy and pre-install dependencies so the image layer is cached
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
