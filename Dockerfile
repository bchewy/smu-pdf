# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 5000 for Streamlit
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the Streamlit application
CMD ["streamlit", "run", "main.py", "--server.port", "5000", "--server.address", "0.0.0.0"] 