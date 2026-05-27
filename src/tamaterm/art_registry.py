from __future__ import annotations

from .constants import Mood, Stage, PetType

_ART_REGISTRY: dict[tuple, list[str]] = {}


def register_art(pet_type: PetType, stage: Stage, mood: Mood):
    def decorator(func):
        _ART_REGISTRY[(pet_type, stage, mood)] = func()
        return func
    return decorator


def register_art_default(pet_type: PetType, stage: Stage):
    def decorator(func):
        _ART_REGISTRY[(pet_type, stage, Mood.NORMAL)] = func()
        return func
    return decorator


def get_art(pet_type: PetType, stage: Stage, mood: Mood) -> list[str]:
    _ensure_loaded()
    key = (pet_type, stage, mood)
    if key in _ART_REGISTRY:
        return _ART_REGISTRY[key]
    default_key = (pet_type, stage, Mood.NORMAL)
    if default_key in _ART_REGISTRY:
        return _ART_REGISTRY[default_key]
    return ["  ???  ", " (o.o) ", "  ???  "]


_loaded = False


def _ensure_loaded():
    global _loaded
    if _loaded:
        return
    _loaded = True
    from .art import cat, dog, slime  # noqa: F401
