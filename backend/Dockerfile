FROM python:3.11-slim

# Install system dependencies including ADB
RUN apt-get update && apt-get install -y \
    adb \
    android-tools-adb \
    libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data/profiles /app/data/screenshots /app/logs

# Expose port
EXPOSE 8000

# Start ADB server and run application
CMD adb start-server && uvicorn main:app --host 0.0.0.0 --port 8000
