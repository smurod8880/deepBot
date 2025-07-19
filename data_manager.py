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
            # Добавляем свечные данные
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
        stream = message.get('stream')
        data = message.get('data')
        
        if not stream or not data:
            return
        
        # Обработка тикерных данных
        if 'ticker' in stream:
            asset = stream.split('@')[0].upper()
            self.process_ticker_data(asset, data)
        
        # Обработка свечных данных
        elif 'kline' in stream:
            parts = stream.split('@')[0].split('_')
            asset = parts[0].upper()
            timeframe = parts[1] if len(parts) > 1 else '1m'
            self.process_kline_data(asset, timeframe, data)
        
        # Обработка данных стакана
        elif 'depth' in stream:
            asset = stream.split('@')[0].upper()
            self.process_orderbook_data(asset, data)

    def process_ticker_data(self, asset, data):
        """Обработка данных тикера в реальном времени"""
        ticker_key = f"{asset}_TICKER"
        self.data_buffer.setdefault(ticker_key, {})
        
        self.data_buffer[ticker_key] = {
            'price': float(data['c']),
            'change': float(data['P']),
            'volume': float(data['v']),
            'timestamp': data['E']
        }

    def process_kline_data(self, asset, timeframe, data):
        """Обработка свечных данных"""
        k = data['k']
        key = f"{asset}_{timeframe}"
        
        candle = {
            'timestamp': k['t'],
            'open': float(k['o']),
            'high': float(k['h']),
            'low': float(k['l']),
            'close': float(k['c']),
            'volume': float(k['v']),
            'closed': k['x']
        }
        
        if key not in self.data_buffer:
            self.data_buffer[key] = []
        
        # Обновление буфера
        if self.data_buffer[key] and self.data_buffer[key][-1]['timestamp'] == k['t']:
            self.data_buffer[key][-1] = candle
        else:
            self.data_buffer[key].append(candle)
        
        # Сохраняем только последние 200 свечей
        if len(self.data_buffer[key]) > 200:
            self.data_buffer[key] = self.data_buffer[key][-200:]

    def process_orderbook_data(self, asset, data):
        """Обработка данных стакана"""
        orderbook_key = f"{asset}_ORDERBOOK"
        self.data_buffer.setdefault(orderbook_key, {})
        
        self.data_buffer[orderbook_key] = {
            'bids': [(float(price), float(qty)) for price, qty in data['bids']],
            'asks': [(float(price), float(qty)) for price, qty in data['asks']],
            'timestamp': data['E']
        }

    def get_data(self, asset, timeframe):
        """Получение данных для конкретного актива и таймфрейма"""
        key = f"{asset}_{timeframe}"
        if key in self.data_buffer and self.data_buffer[key]:
            return pd.DataFrame(self.data_buffer[key])
        return None
    
    def get_orderbook(self, asset):
        """Получение стакана для актива"""
        key = f"{asset}_ORDERBOOK"
        return self.data_buffer.get(key, None)
    
    def get_ticker(self, asset):
        """Получение тикерных данных"""
        key = f"{asset}_TICKER"
        return self.data_buffer.get(key, None)

    async def start(self):
        """Запуск сбора данных"""
        await self.connect()
