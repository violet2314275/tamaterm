from __future__ import annotations

import os
import sys
from pathlib import Path

MARKER = "# >>> tamaterm >>>"
MARKER_END = "# <<< tamaterm <<<"

BASH_HOOK = '''tamaterm_prompt_hook() {
    local status_file="$HOME/.tamaterm/status.txt"
    if [ -f "$status_file" ]; then
        cat "$status_file"
        echo ""
    fi
}
if [[ -z "$PROMPT_COMMAND" ]]; then
    PROMPT_COMMAND="tamaterm_prompt_hook"
else
    PROMPT_COMMAND="tamaterm_prompt_hook;${PROMPT_COMMAND}"
fi'''

ZSH_HOOK = '''tamaterm_precmd() {
    local status_file="$HOME/.tamaterm/status.txt"
    if [ -f "$status_file" ]; then
        cat "$status_file"
        echo ""
    fi
}
autoload -Uz add-zsh-hook
add-zsh-hook precmd tamaterm_precmd'''

POWERSHELL_HOOK = r'''$global:TamatermOriginalPrompt = $function:prompt
function global:prompt {
    $statusFile = Join-Path $env:USERPROFILE ".tamaterm\status.txt"
    if (Test-Path $statusFile) {
        $content = Get-Content $statusFile -Raw -ErrorAction SilentlyContinue
        if ($content) {
            $clean = $content -replace '\x1b\[[0-9;]*m', ''
            Write-Host $clean -NoNewline
            Write-Host ""
        }
    }
    if ($global:TamatermOriginalPrompt) {
        & $global:TamatermOriginalPrompt
    } else {
        "PS $($executionContext.SessionState.Path.CurrentLocation)$('>' * ($nestedPromptLevel + 1)) "
    }
}'''

FISH_HOOK = '''function tamaterm_prompt --on-event fish_prompt
    set -l status_file "$HOME/.tamaterm/status.txt"
    if test -f "$status_file"
        cat "$status_file"
        echo
    end
end'''


def detect_shell() -> str | None:
    if sys.platform == "win32":
        return "powershell"
    shell = os.environ.get("SHELL", "")
    if "zsh" in shell:
        return "zsh"
    if "bash" in shell:
        return "bash"
    if "fish" in shell:
        return "fish"
    return None


def _get_profile_path(shell: str) -> Path:
    if shell == "powershell":
        profile = os.environ.get("USERPROFILE", str(Path.home()))
        return Path(profile) / "Documents" / "WindowsPowerShell" / "Microsoft.PowerShell_profile.ps1"
    if shell == "fish":
        return Path.home() / ".config" / "fish" / "conf.d" / "tamaterm.fish"
    if shell == "zsh":
        return Path.home() / ".zshrc"
    return Path.home() / ".bashrc"


def _get_hook_code(shell: str) -> str:
    mapping = {
        "bash": BASH_HOOK,
        "zsh": ZSH_HOOK,
        "powershell": POWERSHELL_HOOK,
        "fish": FISH_HOOK,
    }
    return mapping.get(shell, BASH_HOOK)


def install_hook(shell: str) -> None:
    hook_code = _get_hook_code(shell)
    profile_path = _get_profile_path(shell)
    profile_path.parent.mkdir(parents=True, exist_ok=True)

    block = f"{MARKER}\n{hook_code}\n{MARKER_END}\n"

    if profile_path.exists():
        content = profile_path.read_text(encoding="utf-8")
        if MARKER in content:
            return
        content += "\n" + block
    else:
        content = block

    profile_path.write_text(content, encoding="utf-8")


def uninstall_hook(shell: str) -> None:
    profile_path = _get_profile_path(shell)
    if not profile_path.exists():
        return
    content = profile_path.read_text(encoding="utf-8")
    if MARKER not in content:
        return
    start = content.index(MARKER)
    end = content.index(MARKER_END) + len(MARKER_END)
    new_content = content[:start].rstrip() + content[end:]
    profile_path.write_text(new_content, encoding="utf-8")
