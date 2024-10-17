from os import getenv
from pathlib import Path

from pydantic import BaseModel
from BMW.utils import console


class Config(BaseModel):
    ACCESS_CONFIG: int = 50
    STAFF_CREATE_USER: int = 30
    NONE_PERMISSION_LEVEL: int = 0
    ALL_PERMISSION_LEVEL: int = 80
    USER_TOKEN_EXPIRE_TIME: int = 12 * 60 * 60 * 24 * 30 

    ACCESS_SYSTEM_AUDITLOG_LEVEL: int = 20
    ADMIN_LEVEL: int = 40

    CASE_AUTH_CODE_EXPIRE_TIME: int = 60 * 5
    MESSAGE_GLOBAL_SEARCH_LEVEL: int = 50

    READ_HALF_IDNUMBER_LEVEL: int = 20
    READ_FULL_IDNUMBER_LEVEL: int = 30
    EDIT_IDNUMBER_LEVEL: int = 40


# load config


def load_config() -> Config:
    config_path = Path(getenv("CONFIG_PATH", "config.json"))
    if config_path.is_file():
        try:
            with open(config_path) as f:
                console.log("load config from file")
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


config: Config = load_config()
console.log(f"[green]successfully load config")
