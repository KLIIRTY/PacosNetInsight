From python:3.11-slim
Run apt-get update && apt-get update -y && apt-get install -y \
    libcap-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "app.py"]
