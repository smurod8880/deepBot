import asyncio
import numpy as np
from data_manager import RealTimeData
from feature_engineer import FeatureEngineer
from model_ensemble import HybridModel
from telegram_bot import send_signal
from config import ASSETS, TIMEFRAMES, MIN_CONFIDENCE, VOLATILE_PAIRS

class SignalGenerator:
    def __init__(self):
        self.data_manager = RealTimeData()
        self.feature_engineer = FeatureEngineer()
        self.model = HybridModel()
        self.active = True
    
    async def start(self):
        """Запуск генерации сигналов"""
        asyncio.create_task(self.data_manager.start())
        await asyncio.sleep(5)  # Ожидание инициализации данных
        
        while self.active:
            try:
                for asset in ASSETS:
                    # Для высоковолатильных пар используем 1m, для остальных 5m
                    timeframes = ["1m"] if asset in VOLATILE_PAIRS else ["5m"]
                    
                    for timeframe in timeframes:
                        df = self.data_manager.get_data(asset, timeframe)
                        if df is None or len(df) < 50:
                            continue
                        
                        # Получаем дополнительные данные
                        orderbook = self.data_manager.get_orderbook(asset)
                        ticker = self.data_manager.get_ticker(asset)
                        
                        features = self.feature_engineer.calculate_features(df, orderbook, ticker)
                        if not features:
                            continue
                        
                        prediction = self.model.predict(features)
                        
                        if prediction['confidence'] >= MIN_CONFIDENCE:
                            signal = {
                                'asset': asset,
                                'timeframe': timeframe,
                                'price': features['price'],
                                **prediction
                            }
                            await send_signal(signal)
                
                await asyncio.sleep(3)  # Проверка каждые 3 секунды
            
            except Exception as e:
                print(f"Signal generation error: {str(e)}")
