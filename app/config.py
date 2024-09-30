import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAGERDUTY_API_KEY = os.getenv('PAGERDUTY_API_KEY')