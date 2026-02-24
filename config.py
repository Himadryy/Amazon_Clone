import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "a-super-secret-key-for-the-project"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "sqlite:///amazon_clone.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CURRENCY_SYMBOLS = {
        "USD": "$",
        "INR": "₹",
        "EUR": "€",
        "JPY": "¥",
        "GBP": "£",
    }

    CURRENCY_RATES = {
        "USD": 1.0,
        "INR": 83.0,
        "EUR": 0.85,
        "JPY": 110.0,
        "GBP": 0.73,
    }

    LANGUAGES = {
        "en_US": "English",
        "es_MX": "Español",
        "fr_CA": "Français",
        "de_DE": "Deutsch",
        "ja_JP": "日本語",
    }


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
