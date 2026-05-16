# utils/rate_limiter.py

import time
from functools import wraps

class RateLimiter:
    def __init__(self, calls_per_minute: int):
        self.interval = 60 / calls_per_minute
        self.last_called = 0

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - self.last_called
            wait = self.interval - elapsed
            if wait > 0:
                time.sleep(wait)
            result = func(*args, **kwargs)
            self.last_called = time.time()
            return result
        return wrapper
