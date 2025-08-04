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

# Download and install ChromeDriver from S3
RUN curl -fsSL -o /tmp/chromedriver.zip "https://ozkanbucket.s3.eu-central-1.amazonaws.com/chromedriver-linux64.zip" && \
    unzip -j /tmp/chromedriver.zip 'chromedriver-linux64/chromedriver' -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

RUN echo "unzip-j kullanildi - 2024-08-04" > /usr/local/bin/BUILD_MARKER

RUN ls -l /usr/local/bin/

# Create jenkins user with UID 1000 and set up home directory
RUN useradd -m -u 1000 jenkins
# Ensure jenkins owns its home and .local directories
RUN mkdir -p /home/jenkins/.local/share/applications && chown -R jenkins:jenkins /home/jenkins && chmod -R 700 /home/jenkins/.local
# Switch to jenkins user
USER jenkins

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# --- END OF DOCKERFILE --- 