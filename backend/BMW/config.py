from os import getenv
from pathlib import Path

from pydantic import BaseModel
from BMW.utils import console


class Config(BaseModel):
    GLOBAL_FREE_COUNT: int = 300


# load config


def load_config() -> Config:
    config_path = Path(getenv("CONFIG_PATH", "config.json"))
    if config_path.is_file():
        try:
            with open(config_path) as f:
                # console.log("load config from file")
                return Config.model_validate_json(f.read())
        except ValueError as e:
            console.log(f"[yellow]{config_path} is not a valid Config")
            console.print_exception()
    console.log(f"[green]Use default config.")
    config = Config()
    with open(config_path, "w") as f:
        console.log(f"[yellow]Write default config into {config_path}")
        f.write(config.model_dump_json(indent=4))
    return config

def save_config(config: Config):
    config_path = Path(getenv("CONFIG_PATH", "config.json"))
    with open(config_path, "w") as f:
        f.write(config.model_dump_json(indent=4))


config: Config = load_config()
console.log(f"[green]successfully load config")
