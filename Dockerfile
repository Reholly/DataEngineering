# Используем официальный образ Apache Airflow
FROM apache/airflow:2.5.0-python3.8

# Устанавливаем необходимые пакеты для установки Java
USER root

# Устанавливаем Java (например, OpenJDK 11)
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем пользователя обратно на airflow
USER airflow

# Устанавливаем переменные окружения
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"
COPY requirements.txt .
RUN pip install -r requirements.txt