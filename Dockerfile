FROM python:3.9-slim

WORKDIR /app

# Set environment variables for matplotlib
ENV MPLCONFIGDIR=/tmp/matplotlib
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create matplotlib config directory
RUN mkdir -p /tmp/matplotlib

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set permissions
RUN chmod -R 755 /app
RUN chmod -R 777 /tmp/matplotlib

# Expose ports
EXPOSE 7860 3001

# Run the application
CMD ["python", "app.py"]