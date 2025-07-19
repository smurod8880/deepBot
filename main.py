import asyncio
from signal_generator import SignalGenerator
from data_manager import RealTimeData

async def main():
    print("🚀 Starting QuotexSignalNet v1.0")
    
    # Инициализация менеджера данных
    data_manager = RealTimeData()
    asyncio.create_task(data_manager.start())
    
    # Инициализация генератора сигналов
    generator = SignalGenerator()
    await generator.start()

if __name__ == "__main__":
    asyncio.run(main())
