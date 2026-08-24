import os
import logging.config
from dataclasses import dataclass


@dataclass(frozen=True)
class EnvironmentConfig:
    name: str
    base_url: str
    api_base_url: str
    user_id: str


DEFAULT_BROWSER = "chrome"
DEFAULT_HEADLESS = False
DEFAULT_ENV = "qa"

ENDPOINTS = {
    "get_matches": "/matches",
    "reset_balance": "/reset-balance",
    "get_balance": "/balance",
    "place_bet": "/place-bet"
}

ENVIRONMENTS = {
    "dev": EnvironmentConfig(
        name="dev",
        base_url="https://dev.example.com",
        api_base_url="https://api.dev.example.com",
        user_id="",
    ),
    "qa": EnvironmentConfig(
        name="qa",
        base_url="https://qae-assignment-tau.vercel.app/",
        api_base_url="https://qae-assignment-tau.vercel.app/api",
        user_id="",
    ),
    "prod": EnvironmentConfig(
        name="prod",
        base_url="https://example.com",
        api_base_url="https://api.example.com",
        user_id="",
    ),
}


def get_environment_config(env_name: str | None = None) -> EnvironmentConfig:
    env_name = env_name or os.environ.get("TEST_ENV", DEFAULT_ENV)
    return ENVIRONMENTS.get(env_name.lower(), ENVIRONMENTS[DEFAULT_ENV])


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
