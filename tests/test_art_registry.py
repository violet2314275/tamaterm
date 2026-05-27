from tamaterm.art_registry import get_art, _ART_REGISTRY, _ensure_loaded
from tamaterm.constants import PetType, Stage, Mood


def _reset_registry():
    import sys
    _ART_REGISTRY.clear()
    import tamaterm.art_registry as mod
    mod._loaded = False
    # Unload art modules and clear package references so decorators re-execute
    art_pkg = sys.modules.get("tamaterm.art")
    for name in list(sys.modules):
        if name.startswith("tamaterm.art.") or name == "tamaterm.art":
            if art_pkg and name != "tamaterm.art":
                short = name.split(".")[-1]
                if hasattr(art_pkg, short):
                    delattr(art_pkg, short)
            del sys.modules[name]


def test_get_art_returns_list():
    _reset_registry()
    art = get_art(PetType.CAT, Stage.EGG, Mood.NORMAL)
    assert isinstance(art, list)
    assert len(art) > 0


def test_get_art_falls_back_to_normal():
    _reset_registry()
    # SAD has no registered art for cat egg, should fall back to NORMAL
    art_normal = get_art(PetType.CAT, Stage.EGG, Mood.NORMAL)
    art_sad = get_art(PetType.CAT, Stage.EGG, Mood.SAD)
    assert art_normal == art_sad


def test_get_art_returns_fallback_for_unknown():
    _reset_registry()
    # After clearing, _ensure_loaded will re-import, so test with a combo
    # that definitely doesn't exist by temporarily clearing after load
    _ensure_loaded()
    _ART_REGISTRY.clear()
    art = get_art(PetType.CAT, Stage.EGG, Mood.NORMAL)
    assert art == ["  ???  ", " (o.o) ", "  ???  "]


def test_get_art_cat_has_registered_variants():
    _reset_registry()
    art = get_art(PetType.CAT, Stage.ADULT, Mood.HAPPY)
    assert isinstance(art, list)
    assert len(art) > 0
    assert art != ["  ???  ", " (o.o) ", "  ???  "]


def test_get_art_dog_registered():
    _reset_registry()
    art = get_art(PetType.DOG, Stage.ADULT, Mood.NORMAL)
    assert isinstance(art, list)
    assert len(art) > 0


def test_get_art_slime_registered():
    _reset_registry()
    art = get_art(PetType.SLIME, Stage.ADULT, Mood.NORMAL)
    assert isinstance(art, list)
    assert len(art) > 0


def test_ensure_loaded_idempotent():
    _reset_registry()
    _ensure_loaded()
    count1 = len(_ART_REGISTRY)
    _ensure_loaded()
    count2 = len(_ART_REGISTRY)
    assert count1 == count2
