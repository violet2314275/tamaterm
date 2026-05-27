import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from tamaterm.state import PetState, Stats
from tamaterm.constants import Stage, Mood, PetType


def test_stats_clamp():
    s = Stats(hunger=150, happiness=-10, energy=50, hygiene=50)
    s.clamp()
    assert s.hunger == 100
    assert s.happiness == 0
    assert s.energy == 50


def test_stats_average():
    s = Stats(hunger=80, happiness=60, energy=40, hygiene=20)
    assert s.average() == 50.0


def test_stats_critical():
    s = Stats(hunger=5, happiness=80, energy=80, hygiene=80)
    assert s.is_critical()


def test_pet_state_new():
    pet = PetState.new(name="TestCat", pet_type=PetType.CAT)
    assert pet.name == "TestCat"
    assert pet.pet_type == PetType.CAT
    assert pet.stage == Stage.EGG
    assert pet.mood == Mood.NORMAL
    assert pet.birthday != ""


def test_pet_state_save_load(tmp_path):
    with patch("tamaterm.state.DATA_DIR", tmp_path), \
         patch("tamaterm.state.PET_FILE", tmp_path / "pet.json"):
        pet = PetState.new(name="TestPet", pet_type=PetType.DOG)
        pet.save()

        loaded = PetState.load()
        assert loaded.name == "TestPet"
        assert loaded.pet_type == PetType.DOG
        assert loaded.stage == Stage.EGG


def test_pet_state_load_nonexistent(tmp_path):
    with patch("tamaterm.state.DATA_DIR", tmp_path), \
         patch("tamaterm.state.PET_FILE", tmp_path / "pet.json"):
        pet = PetState.load()
        assert pet.name == "Tamago"
        assert pet.stage == Stage.EGG
