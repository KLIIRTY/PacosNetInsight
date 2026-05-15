FROM python:3.11-slim

# Install system dependencies for Prophet and networking tools
RUN apt-get update && apt-get install -y \
    libcap-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit default port
EXPOSE 8501

# Run the Streamlit dashboard
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
