import asyncio
from data_manager import RealTimeData
from feature_engineer import FeatureEngineer
from model_ensemble import HybridModel
from telegram_bot import send_signal
from config import ASSETS, TIMEFRAMES, MIN_CONFIDENCE

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
                    for timeframe in TIMEFRAMES:
                        df = self.data_manager.get_data(asset, timeframe)
                        if df is None or len(df) < 50:
                            continue
                        
                        features = self.feature_engineer.calculate_features(df)
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
                
                await asyncio.sleep(10)  # Проверка каждые 10 секунд
            
            except Exception as e:
                print(f"Signal generation error: {str(e)}")
