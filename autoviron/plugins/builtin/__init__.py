from .fastapi import FastAPIPlugin
from .django import DjangoPlugin
from .ml import MLPlugin

BUILTIN_PLUGINS = [
    FastAPIPlugin(),
    DjangoPlugin(),
    MLPlugin(),
]
