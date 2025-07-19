import asyncio
import pandas as pd
from binance import AsyncClient, BinanceSocketManager
from config import ASSETS, TIMEFRAMES

class RealTimeData:
    def __init__(self):
        self.data_buffer = {}
        self.client = None
        
    async def start(self):
        self.client = await AsyncClient.create()
        bm = BinanceSocketManager(self.client)
        
        # Создаем сокеты для всех пар и таймфреймов
        streams = []
        for asset in ASSETS:
            for tf in TIMEFRAMES:
                stream_name = f"{asset.lower()}@kline_{tf}"
                streams.append(stream_name)
        
        # Подключаемся ко всем потокам одновременно
        async with bm.multiplex_socket(streams) as ms:
            while True:
                try:
                    res = await ms.recv()
                    stream = res['stream']
                    data = res['data']['k']
                    
                    # Парсим данные
                    candle = {
                        'timestamp': data['t'],
                        'open': float(data['o']),
                        'high': float(data['h']),
                        'low': float(data['l']),
                        'close': float(data['c']),
                        'volume': float(data['v']),
                        'closed': data['x']
                    }
                    
                    # Обновляем буфер
                    key = f"{data['s']}_{data['i']}"
                    if key not in self.data_buffer:
                        self.data_buffer[key] = []
                    
                    self.data_buffer[key].append(candle)
                    
                    # Сохраняем только последние 200 свечей
                    if len(self.data_buffer[key]) > 200:
                        self.data_buffer[key] = self.data_buffer[key][-200:]
                
                except Exception as e:
                    print(f"Data error: {str(e)}")
    
    def get_data(self, asset, timeframe):
        """Получение данных для конкретного актива и таймфрейма"""
        key = f"{asset}_{timeframe}"
        if key in self.data_buffer and self.data_buffer[key]:
            return pd.DataFrame(self.data_buffer[key])
        return None
