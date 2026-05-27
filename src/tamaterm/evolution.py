from datetime import datetime, timezone, timedelta

from .constants import Mood, Stage
from .state import PetState

STAGE_DURATIONS = {
    Stage.EGG: timedelta(minutes=5),
    Stage.BABY: timedelta(hours=24),
    Stage.TEEN: timedelta(hours=72),
}

EVOLUTION_THRESHOLDS = {
    Stage.EGG: 40.0,
    Stage.BABY: 50.0,
    Stage.TEEN: 65.0,
}

STAGE_ORDER = [Stage.EGG, Stage.BABY, Stage.TEEN, Stage.ADULT]


def check_evolution(pet: PetState, now: datetime | None = None) -> Stage | None:
    if pet.stage == Stage.ADULT or pet.mood == Mood.DEAD:
        return None

    now = now or datetime.now(timezone.utc)
    birthday = datetime.fromisoformat(pet.birthday)
    elapsed = now - birthday
    required = STAGE_DURATIONS.get(pet.stage)

    if required is None or elapsed < required:
        return None

    threshold = EVOLUTION_THRESHOLDS.get(pet.stage, 50.0)
    if pet.stats.average() >= threshold:
        idx = STAGE_ORDER.index(pet.stage)
        if idx + 1 < len(STAGE_ORDER):
            return STAGE_ORDER[idx + 1]

    return None
