# Dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget curl unzip git \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 \
    libpangocairo-1.0-0 libgtk-3-0 libxshmfence1 \
    libx11-xcb1 libxfixes3 libxext6 libxrender1 libx11-6 \
    libxcb1 libxcb-glx0 libegl1 ca-certificates fonts-liberation && \
    apt-get clean

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install streamlit playwright pillow fpdf
RUN playwright install --with-deps

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
