import asyncio
import json
import websockets
import pandas as pd
from config import ASSETS, TIMEFRAMES

class RealTimeData:
    def __init__(self):
        self.data_buffer = {}
        self.ws_connection = None
        self.streams = self.generate_streams()
        
    def generate_streams(self):
        """Генерация потоков данных для всех активов и таймфреймов"""
        streams = []
        for asset in ASSETS:
            # Добавляем тикерные данные
            streams.append(f"{asset.lower()}@ticker")
            # Добавляем свечные данные для всех 7 таймфреймов
            for tf in TIMEFRAMES:
                streams.append(f"{asset.lower()}@kline_{tf}")
            # Добавляем данные стакана
            streams.append(f"{asset.lower()}@depth20")
        return streams

    async def connect(self):
        """Установка соединения с Binance WebSocket"""
        url = f"wss://stream.binance.com:9443/stream?streams={'/'.join(self.streams)}"
        while True:
            try:
                async with websockets.connect(url) as self.ws_connection:
                    print("✅ WebSocket подключен к Binance")
                    while True:
                        message = await self.ws_connection.recv()
                        await self.process_message(json.loads(message))
            except Exception as e:
                print(f"WebSocket error: {e}, переподключение через 5 сек...")
                await asyncio.sleep(5)

    async def process_message(self, message):
        """Обработка входящих сообщений"""
        # ... (остальной код без изменений)
