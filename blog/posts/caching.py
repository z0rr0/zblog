from django.core.cache import caches


class QuerySetCache:
    cache = caches['queries']

    @classmethod
    def set(cls, key, value):
        cls.cache.set(key, value)

    @classmethod
    def get(cls, key, default=None):
        cls.cache.get(key, default)

    @classmethod
    def get_or_set(cls, key, default):
        cls.cache.get_or_set(key, default)

    @classmethod
    def clear(cls):
        cls.cache.clear()
