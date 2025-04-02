import abc
import urllib.parse
from enum import StrEnum
from typing import Any, Protocol

from aiocache import BaseCache, cached, caches
from aiocache.base import SENTINEL

from settings import settings


class CacheSotres(StrEnum):
    DEFAULT = "default"
    DISTRIBUTED = "distributed"


class CacheManagerProtocol(Protocol):
    @staticmethod
    @abc.abstractmethod
    def get_mem(mem: CacheSotres) -> BaseCache: ...

    @staticmethod
    @abc.abstractmethod
    def decorate(
        mem: CacheSotres,
        ttl: int | None = None,
        key: Any | None = None,
        key_builder: Any | None = None,
        skip_cache_func: Any = lambda x: False,
        **kwargs,
    ): ...


class CacheManager(CacheManagerProtocol):

    @staticmethod
    def get_mem(mem: CacheSotres) -> BaseCache:
        return caches.get(mem.value)

    @staticmethod
    def decorate(
        mem: CacheSotres,
        ttl: int | None = None,
        key: Any | None = None,
        key_builder: Any | None = None,
        skip_cache_func: Any = lambda x: False,
        *,
        namespace: Any | None = None,
        serializer: Any | None = None,
        plugins: Any | None = None,
        noself: bool = False,
    ):
        return cached(
            alias=mem.value,
            ttl=ttl or SENTINEL,
            key=key,
            key_builder=key_builder,
            skip_cache_func=skip_cache_func,
            namespace=namespace,
            serializer=serializer,
            plugins=plugins,
            noself=noself,
        )
