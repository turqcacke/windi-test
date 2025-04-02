import urllib.parse

from aiocache import caches

from infrastructure.cache.cache_manager import CacheSotres
from settings import settings

_config = {
    {
        CacheSotres.DEFAULT.value: {
            "cache": "aiocache.SimpleMemoryCache",
            "serializer": {"class": "aiocache.serializers.StringSerializer"},
        },
        CacheSotres.DISTRIBUTED.value: {
            "cache": "aiocache.RedisCache",
            "endpoint": settings.REDIS_DSN.unicode_host(),
            "port": settings.REDIS_DSN.port,
            "password": urllib.parse.unquote(settings.REDIS_DSN.password),
            "db": (
                int(settings.REDIS_DSN.path.rsplit("/", 1)[-1])
                if settings.REDIS_DSN.path
                else 0
            ),
            "timeout": settings.REDIS_TIMEOUT,
            "serializer": {"class": "aiocache.serializers.PickleSerializer"},
            "plugins": [
                {"class": "aiocache.plugins.HitMissRatioPlugin"},
                {"class": "aiocache.plugins.TimingPlugin"},
            ],
        },
    }
}
caches.set_config(_config)
