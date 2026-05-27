from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone

from .constants import DATA_DIR, PET_FILE, Stage, Mood, PetType


@dataclass
class Stats:
    hunger: float = 100.0
    happiness: float = 100.0
    energy: float = 100.0
    hygiene: float = 100.0

    def clamp(self) -> Stats:
        self.hunger = max(0.0, min(100.0, self.hunger))
        self.happiness = max(0.0, min(100.0, self.happiness))
        self.energy = max(0.0, min(100.0, self.energy))
        self.hygiene = max(0.0, min(100.0, self.hygiene))
        return self

    def is_critical(self) -> bool:
        return any(v <= 10 for v in (self.hunger, self.happiness, self.energy))

    def average(self) -> float:
        return (self.hunger + self.happiness + self.energy + self.hygiene) / 4


@dataclass
class PetState:
    name: str = "Tamago"
    pet_type: PetType = PetType.CAT
    stage: Stage = Stage.EGG
    mood: Mood = Mood.NORMAL
    stats: Stats = field(default_factory=Stats)
    birthday: str = ""
    last_interaction: str = ""
    last_decay: str = ""
    death_time: str | None = None
    total_commits: int = 0
    total_feeds: int = 0
    total_plays: int = 0

    def save(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        data = asdict(self)
        data["pet_type"] = self.pet_type.value
        data["stage"] = self.stage.value
        data["mood"] = self.mood.value
        PET_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def load(cls) -> PetState:
        if not PET_FILE.exists():
            return cls.new()
        data = json.loads(PET_FILE.read_text(encoding="utf-8"))
        data["stats"] = Stats(**data["stats"])
        data["stage"] = Stage(data["stage"])
        data["mood"] = Mood(data["mood"])
        data["pet_type"] = PetType(data["pet_type"])
        return cls(**data)

    @classmethod
    def new(cls, name: str = "Tamago", pet_type: PetType = PetType.CAT) -> PetState:
        now = datetime.now(timezone.utc).isoformat()
        return cls(
            name=name,
            pet_type=pet_type,
            stage=Stage.EGG,
            mood=Mood.NORMAL,
            stats=Stats(),
            birthday=now,
            last_interaction=now,
            last_decay=now,
        )
