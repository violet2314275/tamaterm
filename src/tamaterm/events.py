from __future__ import annotations

import subprocess
import os
from dataclasses import dataclass
from typing import Optional

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


@dataclass
class EventEffect:
    happiness: float = 0
    hunger: float = 0
    energy: float = 0
    hygiene: float = 0
    message: str = ""


class EventDetector:
    def __init__(self):
        self._last_commit_count = 0
        self._last_cpu_spike = False
        self._last_branch = ""

    def detect_git_activity(self) -> Optional[EventEffect]:
        try:
            result = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                capture_output=True, text=True, timeout=5,
                cwd=os.getcwd(),
            )
            if result.returncode != 0:
                return None
            count = int(result.stdout.strip())
            if self._last_commit_count > 0 and count > self._last_commit_count:
                diff = count - self._last_commit_count
                self._last_commit_count = count
                return EventEffect(
                    happiness=+8 * diff,
                    energy=-3 * diff,
                    message=f"commit detected! (+{diff})",
                )
            self._last_commit_count = count
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
            pass
        return None

    def detect_branch_change(self) -> Optional[EventEffect]:
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True, text=True, timeout=5,
                cwd=os.getcwd(),
            )
            if result.returncode != 0:
                return None
            branch = result.stdout.strip()
            if self._last_branch and branch != self._last_branch:
                old = self._last_branch
                self._last_branch = branch
                return EventEffect(happiness=+5, message=f"branch: {old} -> {branch}")
            self._last_branch = branch
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return None

    def detect_cpu_spike(self) -> Optional[EventEffect]:
        if not HAS_PSUTIL:
            return None
        cpu = psutil.cpu_percent(interval=0.1)
        is_spike = cpu > 80
        if is_spike and not self._last_cpu_spike:
            self._last_cpu_spike = True
            return EventEffect(
                energy=-5, happiness=-3,
                message=f"CPU spike ({cpu:.0f}%)",
            )
        self._last_cpu_spike = is_spike
        return None

    def detect_memory_pressure(self) -> Optional[EventEffect]:
        if not HAS_PSUTIL:
            return None
        mem = psutil.virtual_memory()
        if mem.percent > 90:
            return EventEffect(
                happiness=-2, energy=-3,
                message=f"memory pressure ({mem.percent:.0f}%)",
            )
        return None

    def detect_all(self) -> list[EventEffect]:
        effects = []
        for detector in [
            self.detect_git_activity,
            self.detect_branch_change,
            self.detect_cpu_spike,
            self.detect_memory_pressure,
        ]:
            effect = detector()
            if effect:
                effects.append(effect)
        return effects
