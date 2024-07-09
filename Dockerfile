# Use the official Python image as a base image
FROM --platform=$BUILDPLATFORM python:3.12-alpine as base

LABEL version="1.2.1"

# Set up a build stage for installing dependencies
FROM base as builder
COPY requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt

# Set up the final stage
FROM base
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app

# Add /root/.local/bin to PATH
ENV PATH="/root/.local/bin:${PATH}"
ENV PYTHONPATH="/app"

# Set the entrypoint
CMD uvicorn src.main:app --host 0.0.0.0 --port 8000