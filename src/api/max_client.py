import aiomax
from aiomax import fsm, buttons
import os
from dotenv import load_dotenv

load_dotenv()


class MaxBot:
    def __init__(self):
        self.token = os.getenv('MAX_BOT_TOKEN')
        self.bot = aiomax.Bot(self.token, default_format="markdown")

    def run(self):
        self.bot.run()