from tamaterm.display import build_frame, stat_bar
from tamaterm.state import PetState
from tamaterm.constants import Mood, Stage, PetType


def test_build_frame_basic():
    pet = PetState.new(name="Test", pet_type=PetType.CAT)
    frame = build_frame(pet, use_color=False)
    assert "Test" in frame
    assert "egg" in frame
    assert "hunger" in frame
    assert "happy" in frame


def test_build_frame_with_color():
    pet = PetState.new(name="Test", pet_type=PetType.CAT)
    frame = build_frame(pet, use_color=True)
    assert "\033[" in frame
    assert "Test" in frame


def test_stat_bar():
    bar = stat_bar(80)
    assert len(bar) > 0


def test_build_frame_different_moods():
    for mood in [Mood.HAPPY, Mood.HUNGRY, Mood.SLEEPING, Mood.DEAD]:
        pet = PetState.new(name="Test", pet_type=PetType.CAT)
        pet.mood = mood
        frame = build_frame(pet, use_color=False)
        assert "Test" in frame


def test_build_frame_different_pets():
    for pet_type in [PetType.CAT, PetType.DOG, PetType.SLIME]:
        pet = PetState.new(name="Test", pet_type=pet_type)
        pet.stage = Stage.ADULT
        frame = build_frame(pet, use_color=False)
        assert "Test" in frame
