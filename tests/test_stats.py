from datetime import datetime, timezone, timedelta

from tamaterm.stats import apply_decay, resolve_mood
from tamaterm.state import PetState, Stats
from tamaterm.constants import Mood, Stage, PetType


def test_decay_does_not_apply_to_egg():
    pet = PetState.new()
    pet.stage = Stage.EGG
    pet.last_decay = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    apply_decay(pet)
    assert pet.stats.hunger == 80.0


def test_decay_does_not_apply_to_dead():
    pet = PetState.new()
    pet.mood = Mood.DEAD
    pet.last_decay = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    apply_decay(pet)
    assert pet.stats.hunger == 80.0


def test_decay_reduces_stats():
    pet = PetState.new()
    pet.stage = Stage.BABY
    pet.last_decay = (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat()
    apply_decay(pet)
    assert pet.stats.hunger < 80.0


def test_resolve_mood_normal():
    pet = PetState.new()
    # Default stats (80,80,80,80) trigger HAPPY (happiness>=80, hunger>=60)
    assert resolve_mood(pet) == Mood.HAPPY


def test_resolve_mood_normal_when_moderate():
    pet = PetState.new()
    pet.stats = Stats(hunger=50, happiness=50, energy=50, hygiene=50)
    assert resolve_mood(pet) == Mood.NORMAL


def test_resolve_mood_hungry():
    pet = PetState.new()
    pet.stats.hunger = 10
    assert resolve_mood(pet) == Mood.HUNGRY


def test_resolve_mood_dead():
    pet = PetState.new()
    pet.stats.hunger = 0
    pet.stats.happiness = 0
    assert resolve_mood(pet) == Mood.DEAD


def test_resolve_mood_happy():
    pet = PetState.new()
    pet.stats.happiness = 90
    pet.stats.hunger = 80
    assert resolve_mood(pet) == Mood.HAPPY


def test_resolve_mood_stays_dead():
    pet = PetState.new()
    pet.mood = Mood.DEAD
    assert resolve_mood(pet) == Mood.DEAD
