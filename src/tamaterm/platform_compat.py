import sys
import os
import subprocess


def is_windows() -> bool:
    return sys.platform == "win32"


def get_pid_file() -> str:
    from .constants import DAEMON_PID_FILE
    return str(DAEMON_PID_FILE)


def is_process_running(pid: int) -> bool:
    if is_windows():
        try:
            import ctypes
            handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
            if handle:
                ctypes.windll.kernel32.CloseHandle(handle)
                return True
        except Exception:
            pass
        return False
    else:
        try:
            os.kill(pid, 0)
            return True
        except (OSError, ProcessLookupError):
            return False


def start_background(target, args=()):
    if is_windows():
        CREATE_NO_WINDOW = 0x08000000
        subprocess.Popen(
            [sys.executable, "-m", "tamaterm.daemon"],
            creationflags=CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        pid = os.fork()
        if pid > 0:
            return
        os.setsid()
        pid2 = os.fork()
        if pid2 > 0:
            sys.exit(0)
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")
        target(*args)


def kill_process(pid: int) -> None:
    if is_windows():
        subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True)
    else:
        import signal
        os.kill(pid, signal.SIGTERM)
