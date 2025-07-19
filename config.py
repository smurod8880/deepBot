import os

# Binance WebSocket
WEBSOCKET_URL = "wss://stream.binance.com:9443/stream"

# Торговые параметры
ASSETS = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "DOTUSDT", "XRPUSDT"]
TIMEFRAMES = ["1m", "5m"]
VOLATILE_PAIRS = ["BTCUSDT", "ETHUSDT"]  # Высоковолатильные пары
MIN_CONFIDENCE = 90

# Конфигурация индикаторов (без изменений)
INDICATOR_CONFIG = {
    'RSI': {'period': 14},
    'MACD': {'fast': 12, 'slow': 26, 'signal': 9},
    'STOCHASTIC': {'k_period': 14, 'd_period': 3},
    'BOLLINGER': {'period': 20, 'deviation': 2}
}

# Telegram (без изменений)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
