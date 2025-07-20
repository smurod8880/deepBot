import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 10 самых прибыльных активов
ASSETS = [
    "BTCUSDT", "ETHUSDT", "XRPUSDT", 
    "SOLUSDT", "ADAUSDT", "DOGEUSDT",
    "DOTUSDT", "LINKUSDT", "MATICUSDT",
    "AVAXUSDT"
]

# 7 оптимальных таймфреймов
TIMEFRAMES = [
    "1m", "5m", "15m",
    "30m", "1h", "4h", "1d"
]

MIN_CONFIDENCE = 90
ANALYSIS_INTERVAL = 10  # Анализ каждые 10 секунд
