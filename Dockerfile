FROM python:3.9

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$PATH:$JAVA_HOME/bin"

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src

CMD ["python", "src/main.py"]
