from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

from tamaterm.daemon import Daemon, start_daemon, stop_daemon
from tamaterm.state import PetState, Stats
from tamaterm.constants import Mood, Stage


def test_daemon_tick_applies_decay():
    daemon = Daemon()
    pet = PetState.new()
    pet.stage = Stage.BABY
    pet.last_decay = datetime.now(timezone.utc).isoformat()

    with patch("tamaterm.daemon.apply_decay") as mock_decay, \
         patch("tamaterm.daemon.resolve_mood", return_value=Mood.NORMAL), \
         patch("tamaterm.daemon.check_evolution", return_value=None), \
         patch("tamaterm.daemon.build_frame", return_value="frame"), \
         patch("tamaterm.daemon.STATUS_FILE") as mock_status, \
         patch.object(pet, "save"):
        mock_status.with_suffix.return_value = MagicMock()
        daemon.tick(pet)
        mock_decay.assert_called_once()


def test_daemon_tick_applies_event_effects():
    daemon = Daemon()
    pet = PetState.new()
    pet.stats = Stats(hunger=50, happiness=50, energy=50, hygiene=50)

    effect = MagicMock()
    effect.happiness = 8
    effect.hunger = 0
    effect.energy = -3
    effect.hygiene = 0
    effect.message = "test event"

    with patch("tamaterm.daemon.apply_decay"), \
         patch.object(daemon.detector, "detect_all", return_value=[effect]), \
         patch("tamaterm.daemon.resolve_mood", return_value=Mood.NORMAL), \
         patch("tamaterm.daemon.check_evolution", return_value=None), \
         patch("tamaterm.daemon.build_frame", return_value="frame"), \
         patch("tamaterm.daemon.STATUS_FILE") as mock_status, \
         patch.object(pet, "save"):
        mock_status.with_suffix.return_value = MagicMock()
        daemon.tick(pet)
        assert pet.stats.happiness == 58
        assert pet.stats.energy == 47


def test_daemon_tick_evolution():
    daemon = Daemon()
    pet = PetState.new()
    pet.stage = Stage.EGG

    with patch("tamaterm.daemon.apply_decay"), \
         patch("tamaterm.daemon.resolve_mood", return_value=Mood.NORMAL), \
         patch("tamaterm.daemon.check_evolution", return_value=Stage.BABY), \
         patch("tamaterm.daemon.build_frame", return_value="frame"), \
         patch("tamaterm.daemon.STATUS_FILE") as mock_status, \
         patch.object(pet, "save"):
        mock_status.with_suffix.return_value = MagicMock()
        daemon.tick(pet)
        assert pet.stage == Stage.BABY


def test_daemon_signal_handler():
    daemon = Daemon()
    assert daemon.running is True
    daemon._signal_handler(None, None)
    assert daemon.running is False


def test_start_daemon_already_running():
    with patch("tamaterm.daemon.DAEMON_PID_FILE") as mock_pid_file, \
         patch("tamaterm.platform_compat.is_process_running", return_value=True), \
         patch("tamaterm.platform_compat.kill_process") as mock_kill, \
         patch("tamaterm.platform_compat.start_background") as mock_bg, \
         patch("time.sleep"):
        mock_pid_file.exists.return_value = True
        mock_pid_file.read_text.return_value = "  1234  "
        start_daemon()
        mock_kill.assert_called_once_with(1234)
        mock_bg.assert_called_once()


def test_start_daemon_stale_pid():
    with patch("tamaterm.daemon.DAEMON_PID_FILE") as mock_pid_file, \
         patch("tamaterm.platform_compat.is_process_running", return_value=False), \
         patch("tamaterm.platform_compat.start_background") as mock_bg:
        mock_pid_file.exists.return_value = True
        mock_pid_file.read_text.return_value = "1234"
        start_daemon()
        mock_bg.assert_called_once()


def test_start_daemon_no_pid_file():
    with patch("tamaterm.daemon.DAEMON_PID_FILE") as mock_pid_file, \
         patch("tamaterm.platform_compat.start_background") as mock_bg:
        mock_pid_file.exists.return_value = False
        start_daemon()
        mock_bg.assert_called_once()


def test_stop_daemon_no_pid_file():
    with patch("tamaterm.daemon.DAEMON_PID_FILE") as mock_pid_file:
        mock_pid_file.exists.return_value = False
        stop_daemon()  # Should not raise


def test_stop_daemon_running():
    with patch("tamaterm.daemon.DAEMON_PID_FILE") as mock_pid_file, \
         patch("tamaterm.platform_compat.is_process_running", return_value=True), \
         patch("tamaterm.platform_compat.kill_process") as mock_kill:
        mock_pid_file.exists.return_value = True
        mock_pid_file.read_text.return_value = "1234"
        stop_daemon()
        mock_kill.assert_called_once_with(1234)
        mock_pid_file.unlink.assert_called_once_with(missing_ok=True)
