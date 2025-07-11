# Use official Python image
FROM python:3.10-slim

# Install system dependencies for Chromium
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 \
    libxss1 libasound2 libatk-bridge2.0-0 libcups2 libdbus-1-3 \
    libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libxrandr2 \
    libappindicator1 libgtk-3-0 libxshmfence1 libgbm1 fonts-liberation \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all code to container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    playwright install chromium

# Expose port
EXPOSE 5000

# Start the app with Gunicorn
CMD ["gunicorn", "run:app", "-c", "gunicorn_config.py"]