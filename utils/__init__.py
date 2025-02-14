import traceback, logging

from functools import wraps
from typing import Callable




def logger(f: Callable):
    @wraps(f)
    async def log(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except Exception:
            print(traceback.format_exc())
    return log
