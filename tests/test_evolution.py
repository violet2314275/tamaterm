from datetime import datetime, timezone, timedelta

from tamaterm.evolution import check_evolution
from tamaterm.state import PetState, Stats
from tamaterm.constants import Stage, Mood


def test_egg_evolution_after_5_minutes():
    pet = PetState.new()
    pet.birthday = (datetime.now(timezone.utc) - timedelta(minutes=6)).isoformat()
    pet.stats = Stats(hunger=80, happiness=80, energy=80, hygiene=80)
    result = check_evolution(pet)
    assert result == Stage.BABY


def test_egg_no_evolution_before_5_minutes():
    pet = PetState.new()
    pet.birthday = (datetime.now(timezone.utc) - timedelta(minutes=3)).isoformat()
    result = check_evolution(pet)
    assert result is None


def test_no_evolution_when_dead():
    pet = PetState.new()
    pet.mood = Mood.DEAD
    pet.birthday = (datetime.now(timezone.utc) - timedelta(hours=100)).isoformat()
    result = check_evolution(pet)
    assert result is None


def test_no_evolution_when_adult():
    pet = PetState.new()
    pet.stage = Stage.ADULT
    result = check_evolution(pet)
    assert result is None


def test_baby_evolution_insufficient_care():
    pet = PetState.new()
    pet.stage = Stage.BABY
    pet.birthday = (datetime.now(timezone.utc) - timedelta(hours=25)).isoformat()
    pet.stats = Stats(hunger=20, happiness=20, energy=20, hygiene=20)
    result = check_evolution(pet)
    assert result is None
