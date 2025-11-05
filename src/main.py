import sys
import os
# Добавляем src в путь импортов
sys.path.append(os.path.dirname(__file__))

from bot.bio_rhythm_engine import BioRhythmEngine
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    bot = BioRhythmEngine()
    print("🚀 BioRhythmEngine Bot запускается...")
    bot.run()

if __name__ == "__main__":
    main()