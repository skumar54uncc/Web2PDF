# Use Python base image
FROM python:3.10-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgtk-3-0 \
    libnss3 \
    libasound2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxfixes3 \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    libglu1-mesa \
    libwayland-client0 \
    libwayland-cursor0 \
    libwayland-egl1 \
    libnotify4 \
    libu2f-udev \
    xdg-utils \
    fonts-liberation \
    wget \
    xvfb \
    unzip

# Set working directory
WORKDIR /app

# Copy app code
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Playwright dependencies and browser
RUN playwright install --with-deps

# Expose port (DO uses this)
EXPOSE 5000

# Run the app with Gunicorn using virtual display
CMD xvfb-run gunicorn run:app -c gunicorn_config.py