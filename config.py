import os

# Binance API
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Торговые параметры
ASSETS = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "LTCUSDT", "ADAUSDT"]
TIMEFRAMES = ["1m", "5m", "15m"]
MIN_CONFIDENCE = 90  # Минимальная точность сигнала

# Конфигурация индикаторов
INDICATOR_CONFIG = {
    'RSI': {'period': 14},
    'MACD': {'fast': 12, 'slow': 26, 'signal': 9},
    'STOCHASTIC': {'k_period': 14, 'd_period': 3},
    'BOLLINGER': {'period': 20, 'deviation': 2}
}
