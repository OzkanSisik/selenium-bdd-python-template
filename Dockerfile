# Selenium test image with Python, Chrome, and ChromeDriver (best practice)
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

# Add Google Chrome's official signing key and repository (using signed-by)
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux-signing-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
RUN apt-get update && apt-get install -y --no-install-recommends google-chrome-stable && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver (try major version, fallback to latest)
RUN set -eux; \
    CHROME_VERSION=$(google-chrome --version | grep -Eo '[0-9]+' | head -1); \
    CHROMEDRIVER_VERSION=$(curl -fsSL --retry 3 --retry-connrefused "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}" || curl -fsSL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE") && \
    curl -fsSL "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" -o /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# Print Chrome and ChromeDriver versions for debug
RUN google-chrome --version && chromedriver --version

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# --- END OF DOCKERFILE --- 