#!/usr/bin/env bash

apt-get update && apt-get install -y \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libharfbuzz0b \
    libdrm2 \
    libxext6 \
    libxfixes3 \
    libxrender1 \
    libxi6 \
    libdbus-1-3 \
    libfontconfig1 \
    libglu1-mesa \
    libwayland-client0 \
    libwayland-cursor0 \
    libwayland-egl1 \
    libnotify4 \
    libu2f-udev \
    libvulkan1 \
    xdg-utils \
    fonts-liberation

playwright install chromium
