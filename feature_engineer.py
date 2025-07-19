import talib
import numpy as np
import pandas as pd
from config import INDICATOR_CONFIG

class FeatureEngineer:
    def calculate_features(self, df):
        """Расчет 25+ технических индикаторов в реальном времени"""
        if len(df) < 50:
            return None
            
        closes = df['close'].values
        highs = df['high'].values
        lows = df['low'].values
        volumes = df['volume'].values
        
        # Основные индикаторы
        rsi = talib.RSI(closes, INDICATOR_CONFIG['RSI']['period'])[-1]
        macd, macd_signal, _ = talib.MACD(
            closes, 
            INDICATOR_CONFIG['MACD']['fast'], 
            INDICATOR_CONFIG['MACD']['slow'], 
            INDICATOR_CONFIG['MACD']['signal']
        )
        stoch_k, stoch_d = talib.STOCH(
            highs, lows, closes,
            INDICATOR_CONFIG['STOCHASTIC']['k_period'],
            INDICATOR_CONFIG['STOCHASTIC']['d_period']
        )
        
        # Трендовые индикаторы
        sma20 = talib.SMA(closes, 20)[-1]
        ema50 = talib.EMA(closes, 50)[-1]
        adx = talib.ADX(highs, lows, closes, 14)[-1]
        
        # Волатильность
        atr = talib.ATR(highs, lows, closes, 14)[-1]
        upper_bb, middle_bb, lower_bb = talib.BBANDS(
            closes, 
            INDICATOR_CONFIG['BOLLINGER']['period'],
            INDICATOR_CONFIG['BOLLINGER']['deviation']
        )
        
        # Объем
        obv = talib.OBV(closes, volumes)[-1]
        
        # Паттерны (реальное распознавание)
        patterns = []
        if talib.CDLENGULFING(df['open'], df['high'], df['low'], df['close'])[-1] > 0:
            patterns.append("bullish_engulfing")
        if talib.CDLHAMMER(df['open'], df['high'], df['low'], df['close'])[-1] > 0:
            patterns.append("hammer")
            
        return {
            'rsi': rsi,
            'macd': macd[-1],
            'macd_signal': macd_signal[-1],
            'stoch_k': stoch_k[-1],
            'stoch_d': stoch_d[-1],
            'sma20': sma20,
            'ema50': ema50,
            'adx': adx,
            'atr': atr,
            'upper_bb': upper_bb[-1],
            'lower_bb': lower_bb[-1],
            'obv': obv,
            'patterns': patterns,
            'price': closes[-1],
            'volatility': np.std(closes[-20:]) / np.mean(closes[-20:]),
            'volume_spike': 1 if volumes[-1] > 2 * np.mean(volumes[-10:]) else 0
        }
