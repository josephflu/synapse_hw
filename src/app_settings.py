import os
from dotenv import load_dotenv


class AppSettings:
    openai_apikey = None

    @staticmethod
    def load():
        app = AppSettings()
        app.openai_apikey = os.getenv("OPENAI_API_KEY")
        return app

load_dotenv()
APP_SETTINGS = AppSettings.load()
