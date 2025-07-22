FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje kodunu ve test dosyalarını container'a kopyala
# Böylece Jenkins pipeline'da testler container içinde çalıştırılabilir
COPY . . 