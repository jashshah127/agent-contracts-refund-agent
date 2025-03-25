# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python app
COPY sample_tracer.py .

# Run the tracer app
CMD ["python", "sample_tracer.py"]
