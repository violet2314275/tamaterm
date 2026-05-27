from unittest.mock import patch, MagicMock

from tamaterm.platform_compat import is_windows, is_process_running, kill_process


def test_is_windows_true():
    with patch("tamaterm.platform_compat.sys") as mock_sys:
        mock_sys.platform = "win32"
        assert is_windows() is True


def test_is_windows_false():
    with patch("tamaterm.platform_compat.sys") as mock_sys:
        mock_sys.platform = "linux"
        assert is_windows() is False


def test_is_process_running_unix_alive():
    with patch("tamaterm.platform_compat.is_windows", return_value=False), \
         patch("tamaterm.platform_compat.os") as mock_os:
        mock_os.kill.return_value = None
        assert is_process_running(1234) is True
        mock_os.kill.assert_called_once_with(1234, 0)


def test_is_process_running_unix_dead():
    with patch("tamaterm.platform_compat.is_windows", return_value=False), \
         patch("tamaterm.platform_compat.os") as mock_os:
        mock_os.kill.side_effect = ProcessLookupError
        mock_os.OSError = OSError
        assert is_process_running(1234) is False


def test_is_process_running_unix_no_such_process():
    with patch("tamaterm.platform_compat.is_windows", return_value=False), \
         patch("tamaterm.platform_compat.os") as mock_os:
        mock_os.kill.side_effect = OSError
        mock_os.OSError = OSError
        assert is_process_running(1234) is False


def test_kill_process_unix():
    with patch("tamaterm.platform_compat.is_windows", return_value=False), \
         patch("tamaterm.platform_compat.os") as mock_os:
        kill_process(1234)
        # signal.SIGTERM is 15 on most systems; just verify os.kill was called
        mock_os.kill.assert_called_once()
        assert mock_os.kill.call_args[0][0] == 1234


def test_kill_process_windows():
    with patch("tamaterm.platform_compat.is_windows", return_value=True), \
         patch("tamaterm.platform_compat.subprocess") as mock_sub:
        kill_process(1234)
        mock_sub.run.assert_called_once_with(
            ["taskkill", "/PID", "1234", "/F"], capture_output=True
        )
