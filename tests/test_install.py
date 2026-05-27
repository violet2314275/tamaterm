import os
from pathlib import Path
from unittest.mock import patch

from tamaterm.install import (
    detect_shell, _get_profile_path, _get_hook_code,
    install_hook, uninstall_hook, MARKER, MARKER_END,
    BASH_HOOK, ZSH_HOOK, POWERSHELL_HOOK, FISH_HOOK,
)


def test_detect_shell_windows():
    with patch("tamaterm.install.sys") as mock_sys, \
         patch("tamaterm.install.os") as mock_os:
        mock_sys.platform = "win32"
        assert detect_shell() == "powershell"


def test_detect_shell_zsh():
    with patch("tamaterm.install.sys") as mock_sys, \
         patch("tamaterm.install.os", environ={"SHELL": "/bin/zsh"}):
        mock_sys.platform = "linux"
        assert detect_shell() == "zsh"


def test_detect_shell_bash():
    with patch("tamaterm.install.sys") as mock_sys, \
         patch("tamaterm.install.os", environ={"SHELL": "/bin/bash"}):
        mock_sys.platform = "linux"
        assert detect_shell() == "bash"


def test_detect_shell_fish():
    with patch("tamaterm.install.sys") as mock_sys, \
         patch("tamaterm.install.os", environ={"SHELL": "/usr/bin/fish"}):
        mock_sys.platform = "linux"
        assert detect_shell() == "fish"


def test_detect_shell_unknown():
    with patch("tamaterm.install.sys") as mock_sys, \
         patch("tamaterm.install.os", environ={"SHELL": ""}):
        mock_sys.platform = "linux"
        assert detect_shell() is None


def test_get_hook_code():
    assert _get_hook_code("bash") == BASH_HOOK
    assert _get_hook_code("zsh") == ZSH_HOOK
    assert _get_hook_code("powershell") == POWERSHELL_HOOK
    assert _get_hook_code("fish") == FISH_HOOK
    assert _get_hook_code("unknown") == BASH_HOOK  # fallback


def test_get_profile_path_bash():
    with patch("tamaterm.install.Path.home", return_value=Path("/home/user")):
        assert _get_profile_path("bash") == Path("/home/user/.bashrc")


def test_get_profile_path_zsh():
    with patch("tamaterm.install.Path.home", return_value=Path("/home/user")):
        assert _get_profile_path("zsh") == Path("/home/user/.zshrc")


def test_get_profile_path_fish():
    with patch("tamaterm.install.Path.home", return_value=Path("/home/user")):
        assert _get_profile_path("fish") == Path("/home/user/.config/fish/conf.d/tamaterm.fish")


def test_install_hook_creates_file(tmp_path):
    profile = tmp_path / ".bashrc"
    with patch("tamaterm.install._get_profile_path", return_value=profile):
        install_hook("bash")
        content = profile.read_text()
        assert MARKER in content
        assert MARKER_END in content
        assert "tamaterm_prompt_hook" in content


def test_install_hook_skips_if_already_installed(tmp_path):
    profile = tmp_path / ".bashrc"
    with patch("tamaterm.install._get_profile_path", return_value=profile):
        install_hook("bash")
        content1 = profile.read_text()
        install_hook("bash")
        content2 = profile.read_text()
        assert content1 == content2


def test_install_hook_appends_to_existing(tmp_path):
    profile = tmp_path / ".bashrc"
    profile.write_text("# existing config\n")
    with patch("tamaterm.install._get_profile_path", return_value=profile):
        install_hook("bash")
        content = profile.read_text()
        assert "# existing config" in content
        assert MARKER in content


def test_uninstall_hook_removes_block(tmp_path):
    profile = tmp_path / ".bashrc"
    with patch("tamaterm.install._get_profile_path", return_value=profile):
        install_hook("bash")
        uninstall_hook("bash")
        content = profile.read_text()
        assert MARKER not in content


def test_uninstall_hook_no_file(tmp_path):
    profile = tmp_path / ".nonexistent"
    with patch("tamaterm.install._get_profile_path", return_value=profile):
        uninstall_hook("bash")  # Should not raise


def test_uninstall_hook_no_marker(tmp_path):
    profile = tmp_path / ".bashrc"
    profile.write_text("# existing config\n")
    with patch("tamaterm.install._get_profile_path", return_value=profile):
        uninstall_hook("bash")
        content = profile.read_text()
        assert "# existing config" in content
