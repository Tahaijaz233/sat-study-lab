import os

class Config:
    DB_PATH = os.getenv("DB_PATH", "sat_lab.db")
    APP_NAME = "SAT Study Lab"

config = Config()
