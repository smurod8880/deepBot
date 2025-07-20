FROM python:3.11-slim

# Установка системных зависимостей с добавлением automake и libtool
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    wget \
    automake \    # Добавлено
    libtool \     # Добавлено
    && rm -rf /var/lib/apt/lists/*

# Исправленная установка TA-Lib
RUN wget https://github.com/TA-Lib/ta-lib/archive/refs/tags/v0.4.0.tar.gz && \
    tar -xzvf v0.4.0.tar.gz && \
    cd ta-lib-0.4.0 && \
    autoreconf -i && \  # Генерация скрипта configure
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf v0.4.0.tar.gz ta-lib-0.4.0

# Остальная часть без изменений
RUN useradd -m appuser
USER appuser
WORKDIR /home/appuser/app

COPY --chown=appuser:appuser . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
