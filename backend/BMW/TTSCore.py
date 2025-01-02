
from typing import Literal
from io import BytesIO

AVALIABLE_VOICE = Literal['xiao-mei', 'xiao-shy']


async def tts(voice: AVALIABLE_VOICE, text: str) -> BytesIO:
    # 你也可以生成一個檔案，然後回應檔案位置
    # BytesIO 就是指檔案資料本身的意思
    
    ...
    