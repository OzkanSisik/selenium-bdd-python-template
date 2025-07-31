# Selenium test image with Python and Google Chrome (Selenium Manager will handle ChromeDriver)
FROM python:3.11-slim

# Install system dependencies and essential packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    gnupg \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    libgbm-dev \
    libu2f-udev \
    libdrm2 \
    && rm -rf /var/lib/apt/lists/*

# Download and install Google Chrome from S3 bucket
RUN curl -fsSL -o /tmp/chrome.deb "https://ozkanbucket.s3.eu-central-1.amazonaws.com/google-chrome-stable_current_amd64.deb" && \
    apt-get update && apt-get install -y --no-install-recommends /tmp/chrome.deb && \
    rm /tmp/chrome.deb && rm -rf /var/lib/apt/lists/*

# Print Chrome version for debug
RUN google-chrome --version

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# --- END OF DOCKERFILE --- 