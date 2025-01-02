from time import time
from pathlib import Path

from rich.console import Console
from datetime import datetime
import pytz


def get_date_string():
    tz_utc_8 = pytz.timezone("Asia/Taipei")
    current_datetime_utc_8 = datetime.now(tz_utc_8)
    return current_datetime_utc_8.strftime("%Y-%m-%d %H:%M:%S")


console = Console()


EDIT_BLACKLIST = ["_id", "type", "collection_name"]
FILTER_WHITELIST = ["_id", "type"]


def unix_timestamp_ms() -> int:
    return int(time() * 1000)


def has_duplicates(lst):
    return len(lst) != len(set(lst))

def get_human_duration_simple(duration: int) -> str:
    year = duration // (365 * 24 * 3600 * 1000)
    duration -= year * (365 * 24 * 3600 * 1000)
    year_string = f"{year}年" if year else ""
    if year_string:
        return year_string

    day = duration // (24 * 3600 * 1000)
    duration -= day * (24 * 3600 * 1000)
    day_string = f"{day}天" if day else ""
    if day_string:
        return day_string

    hour = duration // (3600 * 1000)
    duration -= hour * (3600 * 1000)
    hour_string = f"{hour}小時" if hour else ""
    if hour_string:
        return hour_string

    minute = duration // (60 * 1000)
    duration -= minute * (60 * 1000)
    minute_string = f"{minute}分鐘" if minute else ""
    if minute_string:
        return minute_string

    second = duration / 1000
    second_string = f"{second}秒" if second else ""
    if second_string:
        return second_string

    return ""


base_directory = Path("./assets")


def getFullPath(file_path: str):
    return (base_directory / file_path).resolve()


def checkIfPathSafe(file_path: str):
    # 確保路徑安全
    file_path = file_path.replace("/api/assets", ".")
    full_path = getFullPath(file_path)
    console.log(full_path)
    console.log(base_directory.resolve())
    if not str(full_path).startswith(str(base_directory.resolve())):
        return False
    return True
