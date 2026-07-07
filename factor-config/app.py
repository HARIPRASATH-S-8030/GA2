from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
import yaml
import os

app = FastAPI()

# Replace with the exact origin specified in your assignment if different.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEFAULTS = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}


def to_bool(value):
    return str(value).strip().lower() in {"true", "1", "yes", "on"}


def convert(key, value):
    if key in ("port", "workers"):
        return int(value)
    if key == "debug":
        return to_bool(value)
    return str(value)


def load_config():
    config = DEFAULTS.copy()

    # YAML layer
    if os.path.exists("config.development.yaml"):
        with open("config.development.yaml", "r") as f:
            yaml_data = yaml.safe_load(f) or {}
        for k, v in yaml_data.items():
            config[k] = convert(k, v)

    # .env layer
    env_data = dotenv_values(".env")

    mapping = {
        "APP_PORT": "port",
        "APP_WORKERS": "workers",
        "NUM_WORKERS": "workers",
        "APP_DEBUG": "debug",
        "APP_LOG_LEVEL": "log_level",
        "APP_API_KEY": "api_key",
    }

    for env_key, cfg_key in mapping.items():
        if env_key in env_data:
            config[cfg_key] = convert(cfg_key, env_data[env_key])

    # OS Environment Variables
    for env_key, cfg_key in mapping.items():
        if env_key in os.environ:
            config[cfg_key] = convert(cfg_key, os.environ[env_key])

    return config


@app.get("/effective-config")
def effective_config(set: list[str] = Query(default=[])):
    config = load_config()

    # CLI overrides
    for item in set:
        if "=" in item:
            key, value = item.split("=", 1)
            if key in config:
                config[key] = convert(key, value)

    # Mask secret
    config["api_key"] = "****"

    return config