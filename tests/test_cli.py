from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from tamaterm.cli import cli
from tamaterm.constants import Mood, PetType


def _make_runner():
    return CliRunner()


def test_init_command():
    runner = _make_runner()
    with patch("tamaterm.cli.PetState") as mock_cls, \
         patch("tamaterm.daemon.start_daemon") as mock_daemon:
        mock_pet = MagicMock()
        mock_pet.name = "Whiskers"
        mock_pet.pet_type = PetType.CAT
        mock_cls.new.return_value = mock_pet
        result = runner.invoke(cli, ["init", "Whiskers", "--type", "cat"])
        assert result.exit_code == 0
        assert "Whiskers" in result.output
        mock_pet.save.assert_called_once()
        mock_daemon.assert_called_once()


def test_feed_command():
    runner = _make_runner()
    mock_pet = MagicMock()
    mock_pet.mood = Mood.NORMAL
    mock_pet.name = "Test"
    mock_pet.stats = MagicMock()
    mock_pet.stats.hunger = 50
    mock_pet.stats.happiness = 50
    with patch("tamaterm.cli.PetState") as mock_cls:
        mock_cls.load.return_value = mock_pet
        result = runner.invoke(cli, ["feed"])
        assert result.exit_code == 0
        assert "Fed" in result.output
        mock_pet.save.assert_called_once()


def test_feed_command_dead():
    runner = _make_runner()
    mock_pet = MagicMock()
    mock_pet.mood = Mood.DEAD
    mock_pet.name = "Test"
    with patch("tamaterm.cli.PetState") as mock_cls:
        mock_cls.load.return_value = mock_pet
        result = runner.invoke(cli, ["feed"])
        assert "dead" in result.output


def test_play_command():
    runner = _make_runner()
    mock_pet = MagicMock()
    mock_pet.mood = Mood.NORMAL
    mock_pet.name = "Test"
    mock_pet.stats = MagicMock()
    mock_pet.stats.happiness = 50
    mock_pet.stats.energy = 80
    mock_pet.stats.hygiene = 80
    with patch("tamaterm.cli.PetState") as mock_cls:
        mock_cls.load.return_value = mock_pet
        result = runner.invoke(cli, ["play"])
        assert result.exit_code == 0
        assert "Played" in result.output
        mock_pet.save.assert_called_once()


def test_play_command_dead():
    runner = _make_runner()
    mock_pet = MagicMock()
    mock_pet.mood = Mood.DEAD
    mock_pet.name = "Test"
    with patch("tamaterm.cli.PetState") as mock_cls:
        mock_cls.load.return_value = mock_pet
        result = runner.invoke(cli, ["play"])
        assert "dead" in result.output


def test_clean_command():
    runner = _make_runner()
    mock_pet = MagicMock()
    mock_pet.mood = Mood.NORMAL
    mock_pet.name = "Test"
    mock_pet.stats = MagicMock()
    mock_pet.stats.hygiene = 50
    with patch("tamaterm.cli.PetState") as mock_cls:
        mock_cls.load.return_value = mock_pet
        result = runner.invoke(cli, ["clean"])
        assert result.exit_code == 0
        assert "Cleaned" in result.output
        mock_pet.save.assert_called_once()


def test_clean_command_dead():
    runner = _make_runner()
    mock_pet = MagicMock()
    mock_pet.mood = Mood.DEAD
    mock_pet.name = "Test"
    with patch("tamaterm.cli.PetState") as mock_cls:
        mock_cls.load.return_value = mock_pet
        result = runner.invoke(cli, ["clean"])
        assert "dead" in result.output


def test_sleep_command():
    runner = _make_runner()
    mock_pet = MagicMock()
    mock_pet.mood = Mood.NORMAL
    mock_pet.name = "Test"
    mock_pet.stats = MagicMock()
    mock_pet.stats.energy = 50
    with patch("tamaterm.cli.PetState") as mock_cls:
        mock_cls.load.return_value = mock_pet
        result = runner.invoke(cli, ["sleep"])
        assert result.exit_code == 0
        assert "sleeping" in result.output
        mock_pet.save.assert_called_once()


def test_sleep_command_dead():
    runner = _make_runner()
    mock_pet = MagicMock()
    mock_pet.mood = Mood.DEAD
    mock_pet.name = "Test"
    with patch("tamaterm.cli.PetState") as mock_cls:
        mock_cls.load.return_value = mock_pet
        result = runner.invoke(cli, ["sleep"])
        assert "dead" in result.output


def test_status_command():
    runner = _make_runner()
    mock_pet = MagicMock()
    mock_pet.name = "Test"
    mock_pet.pet_type.value = "cat"
    mock_pet.stage.value = "baby"
    mock_pet.mood.value = "normal"
    mock_pet.stats.hunger = 80.0
    mock_pet.stats.happiness = 90.0
    mock_pet.stats.energy = 70.0
    mock_pet.stats.hygiene = 60.0
    mock_pet.total_commits = 5
    mock_pet.total_feeds = 3
    mock_pet.total_plays = 2
    with patch("tamaterm.cli.PetState") as mock_cls:
        mock_cls.load.return_value = mock_pet
        result = runner.invoke(cli, ["status"])
        assert result.exit_code == 0
        assert "Test" in result.output
        assert "80.0" in result.output


def test_revive_command():
    runner = _make_runner()
    mock_pet = MagicMock()
    mock_pet.mood = Mood.DEAD
    mock_pet.name = "Test"
    mock_pet.stats = MagicMock()
    with patch("tamaterm.cli.PetState") as mock_cls:
        mock_cls.load.return_value = mock_pet
        result = runner.invoke(cli, ["revive"])
        assert result.exit_code == 0
        assert "revived" in result.output
        mock_pet.save.assert_called_once()


def test_revive_command_alive():
    runner = _make_runner()
    mock_pet = MagicMock()
    mock_pet.mood = Mood.NORMAL
    mock_pet.name = "Test"
    with patch("tamaterm.cli.PetState") as mock_cls:
        mock_cls.load.return_value = mock_pet
        result = runner.invoke(cli, ["revive"])
        assert "alive" in result.output


def test_doctor_command_healthy():
    runner = _make_runner()
    with patch("tamaterm.cli.DATA_DIR") as mock_dir, \
         patch("tamaterm.cli.PET_FILE") as mock_pet, \
         patch("tamaterm.cli.STATUS_FILE") as mock_status, \
         patch("tamaterm.cli.DAEMON_PID_FILE") as mock_pid, \
         patch("tamaterm.platform_compat.is_process_running", return_value=True):
        mock_dir.exists.return_value = True
        mock_pet.exists.return_value = True
        mock_status.exists.return_value = True
        mock_pid.exists.return_value = True
        mock_pid.read_text.return_value = "1234"
        result = runner.invoke(cli, ["doctor"])
        assert result.exit_code == 0
        assert "looks good" in result.output


def test_doctor_command_stale_pid():
    runner = _make_runner()
    with patch("tamaterm.cli.DATA_DIR") as mock_dir, \
         patch("tamaterm.cli.PET_FILE") as mock_pet, \
         patch("tamaterm.cli.STATUS_FILE") as mock_status, \
         patch("tamaterm.cli.DAEMON_PID_FILE") as mock_pid, \
         patch("tamaterm.platform_compat.is_process_running", return_value=False):
        mock_dir.exists.return_value = True
        mock_pet.exists.return_value = True
        mock_status.exists.return_value = True
        mock_pid.exists.return_value = True
        mock_pid.read_text.return_value = "1234"
        result = runner.invoke(cli, ["doctor"])
        assert "stale" in result.output


def test_doctor_command_missing_everything():
    runner = _make_runner()
    with patch("tamaterm.cli.DATA_DIR") as mock_dir, \
         patch("tamaterm.cli.PET_FILE") as mock_pet, \
         patch("tamaterm.cli.STATUS_FILE") as mock_status, \
         patch("tamaterm.cli.DAEMON_PID_FILE") as mock_pid:
        mock_dir.exists.return_value = False
        mock_pet.exists.return_value = False
        mock_status.exists.return_value = False
        mock_pid.exists.return_value = False
        result = runner.invoke(cli, ["doctor"])
        assert "missing" in result.output.lower() or "not found" in result.output.lower() or "no pet" in result.output.lower()


def test_start_command():
    runner = _make_runner()
    with patch("tamaterm.daemon.start_daemon") as mock_daemon:
        result = runner.invoke(cli, ["start"])
        assert result.exit_code == 0
        assert "started" in result.output.lower()
        mock_daemon.assert_called_once()


def test_stop_command():
    runner = _make_runner()
    with patch("tamaterm.daemon.stop_daemon") as mock_daemon:
        result = runner.invoke(cli, ["stop"])
        assert result.exit_code == 0
        assert "stopped" in result.output.lower()
        mock_daemon.assert_called_once()
