from enum import Enum
from pathlib import Path

DATA_DIR = Path.home() / ".tamaterm"
PET_FILE = DATA_DIR / "pet.json"
STATUS_FILE = DATA_DIR / "status.txt"
DAEMON_PID_FILE = DATA_DIR / "daemon.pid"
LOG_FILE = DATA_DIR / "daemon.log"

DECAY_INTERVAL_SECONDS = 180  # stats decay every 3 minutes
DAEMON_TICK_SECONDS = 3


class Mood(Enum):
    NORMAL = "normal"
    HAPPY = "happy"
    HUNGRY = "hungry"
    SAD = "sad"
    SLEEPY = "sleepy"
    SLEEPING = "sleeping"
    DEAD = "dead"


class Stage(Enum):
    EGG = "egg"
    BABY = "baby"
    TEEN = "teen"
    ADULT = "adult"


class PetType(Enum):
    CAT = "cat"
    DOG = "dog"
    SLIME = "slime"
