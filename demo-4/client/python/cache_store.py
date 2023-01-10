from threading import Lock
from mylog import log

class Cache_Store:
    def __init__(self) -> None:
        self._lock = Lock()
        self._map = dict()

    # Check if key exists in cache and return value
    def get(self, key):
        self._lock.acquire
        if key in self._map:
            value = self._map[key]
            log.info(f'Returning value {value}')
            self._lock.release
            return value
        log.warn(f'Value not found by key "{key}"')
        self._lock.release
        return None

    # Put new key-value pair into cache
    # Update value if already exists
    def put(self, key, value):
        self._lock.acquire
        log.info(f'Put key: {key} value: {value}')
        self._map[key] = value
        self._lock.release

    # Delete key-value pair from cache if exists
    def delete(self, key):
        self._lock.acquire
        if key in self._map:
            del self._map[key]
            self._lock.release
            return True
        self._lock.release
        return False