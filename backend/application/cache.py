from flask_caching import Cache

cache = Cache(config={
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "RedisCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
})
