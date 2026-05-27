from __future__ import annotations

import time
import signal
import logging
from datetime import datetime, timezone

from .constants import (
    DATA_DIR, STATUS_FILE, DAEMON_PID_FILE, LOG_FILE,
    DAEMON_TICK_SECONDS, Mood,
)
from .state import PetState
from .stats import apply_decay, resolve_mood
from .evolution import check_evolution
from .events import EventDetector
from .display import build_frame

logger = logging.getLogger("tamaterm.daemon")


class Daemon:
    def __init__(self):
        self.running = True
        self.detector = EventDetector()

    def _setup_logging(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=str(LOG_FILE),
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
        )

    def _write_pid(self):
        import os
        DAEMON_PID_FILE.write_text(str(os.getpid()))

    def _cleanup(self):
        for f in (DAEMON_PID_FILE, STATUS_FILE):
            f.unlink(missing_ok=True)

    def _signal_handler(self, signum, frame):
        self.running = False

    def tick(self, pet: PetState) -> None:
        now = datetime.now(timezone.utc)

        apply_decay(pet, now)

        for effect in self.detector.detect_all():
            pet.stats.happiness += effect.happiness
            pet.stats.hunger += effect.hunger
            pet.stats.energy += effect.energy
            pet.stats.hygiene += effect.hygiene
            pet.stats.clamp()
            logger.info("Event: %s", effect.message)

        pet.mood = resolve_mood(pet)

        new_stage = check_evolution(pet, now)
        if new_stage:
            pet.stage = new_stage
            logger.info("Evolved to %s!", new_stage.value)

        frame = build_frame(pet, use_color=False)
        tmp = STATUS_FILE.with_suffix(".tmp")
        tmp.write_text(frame, encoding="utf-8")
        tmp.replace(STATUS_FILE)

        pet.save()

    def run(self):
        self._setup_logging()
        logger.info("Daemon starting")

        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, self._signal_handler)
        if hasattr(signal, "SIGINT"):
            signal.signal(signal.SIGINT, self._signal_handler)

        self._write_pid()
        pet = PetState.load()

        try:
            while self.running:
                self.tick(pet)
                time.sleep(DAEMON_TICK_SECONDS)
        finally:
            self._cleanup()
            logger.info("Daemon stopped")


def start_daemon():
    import os
    from .platform_compat import is_process_running, kill_process, start_background

    if DAEMON_PID_FILE.exists():
        pid = int(DAEMON_PID_FILE.read_text().strip())
        if is_process_running(pid):
            kill_process(pid)
            import time
            time.sleep(0.5)
        DAEMON_PID_FILE.unlink(missing_ok=True)

    start_background(Daemon().run)


def stop_daemon():
    from .platform_compat import is_process_running, kill_process

    if not DAEMON_PID_FILE.exists():
        return
    pid = int(DAEMON_PID_FILE.read_text().strip())
    if is_process_running(pid):
        kill_process(pid)
    DAEMON_PID_FILE.unlink(missing_ok=True)


if __name__ == "__main__":
    Daemon().run()
