from datetime import datetime, timezone

from .constants import Mood, Stage, DECAY_INTERVAL_SECONDS
from .state import PetState

DECAY_RATES = {
    "hunger": -0.6,
    "happiness": -0.3,
    "energy": -0.2,
    "hygiene": -0.15,
}

NIGHT_MULTIPLIER = 1.2


def apply_decay(pet: PetState, now: datetime | None = None) -> None:
    if pet.stage == Stage.EGG:
        return
    if pet.mood == Mood.DEAD:
        return

    now = now or datetime.now(timezone.utc)
    last = datetime.fromisoformat(pet.last_decay)
    elapsed = (now - last).total_seconds()

    if elapsed < 0:
        pet.last_decay = now.isoformat()
        return

    intervals = elapsed / DECAY_INTERVAL_SECONDS

    if intervals < 1.0:
        return

    hour = now.astimezone().hour
    night = 0 <= hour < 6
    multiplier = NIGHT_MULTIPLIER if night else 1.0

    for stat_name, rate in DECAY_RATES.items():
        current = getattr(pet.stats, stat_name)
        decay = rate * intervals * multiplier
        if stat_name == "energy" and pet.mood == Mood.SLEEPING:
            decay = abs(decay) * 0.5
        setattr(pet.stats, stat_name, current + decay)

    pet.stats.clamp()
    pet.last_decay = now.isoformat()

    if pet.stats.hunger <= 0 and pet.stats.happiness <= 0:
        pet.mood = Mood.DEAD
        pet.death_time = now.isoformat()


def resolve_mood(pet: PetState) -> Mood:
    if pet.mood == Mood.DEAD:
        return Mood.DEAD

    s = pet.stats
    hour = datetime.now().astimezone().hour

    if s.hunger <= 0 and s.happiness <= 0:
        return Mood.DEAD
    if s.hunger <= 15:
        return Mood.HUNGRY
    if pet.mood == Mood.SLEEPING and s.energy < 80:
        return Mood.SLEEPING
    if 0 <= hour < 6 and s.energy < 40:
        return Mood.SLEEPING
    if s.energy <= 20:
        return Mood.SLEEPY
    if s.average() <= 30:
        return Mood.SAD
    if s.happiness >= 80 and s.hunger >= 60:
        return Mood.HAPPY
    if s.average() < 50:
        return Mood.SAD

    return Mood.NORMAL
