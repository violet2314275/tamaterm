from __future__ import annotations

import click

from .constants import PetType, Mood, Stage, DATA_DIR, PET_FILE, DAEMON_PID_FILE, STATUS_FILE
from .state import PetState, Stats


@click.group()
@click.version_option(package_name="tamaterm")
def cli():
    """tamaterm -- a virtual pet that lives in your terminal."""
    pass


@cli.command()
@click.argument("name", default="Tamago")
@click.option("--type", "pet_type", type=click.Choice(["cat", "dog", "slime"]), default="cat")
def init(name, pet_type):
    """Create a new pet and start the daemon."""
    from .daemon import start_daemon

    pet = PetState.new(name=name, pet_type=PetType(pet_type))
    pet.save()
    start_daemon()
    click.echo(f"Created {pet_type} named '{name}'!")
    click.echo("Run 'tamaterm install' to add the pet to your shell prompt.")


@cli.command()
def feed():
    """Feed your pet. Reduces hunger."""
    pet = PetState.load()
    if pet.mood == Mood.DEAD:
        click.echo(f"{pet.name} is dead. Run 'tamaterm revive' or 'tamaterm init'.")
        return
    pet.stats.hunger = min(100, pet.stats.hunger + 25)
    pet.stats.happiness = min(100, pet.stats.happiness + 5)
    pet.total_feeds += 1
    from datetime import datetime, timezone
    pet.last_interaction = datetime.now(timezone.utc).isoformat()
    pet.save()
    click.echo(f"Fed {pet.name}! Hunger +25")


@cli.command()
def play():
    """Play with your pet. Boosts happiness, costs energy."""
    pet = PetState.load()
    if pet.mood == Mood.DEAD:
        click.echo(f"{pet.name} is dead. Run 'tamaterm revive' or 'tamaterm init'.")
        return
    pet.stats.happiness = min(100, pet.stats.happiness + 20)
    pet.stats.energy = max(0, pet.stats.energy - 10)
    pet.stats.hygiene = max(0, pet.stats.hygiene - 5)
    pet.total_plays += 1
    from datetime import datetime, timezone
    pet.last_interaction = datetime.now(timezone.utc).isoformat()
    pet.save()
    click.echo(f"Played with {pet.name}! Happiness +20, Energy -10")


@cli.command()
def clean():
    """Clean your pet. Restores hygiene."""
    pet = PetState.load()
    if pet.mood == Mood.DEAD:
        click.echo(f"{pet.name} is dead. Run 'tamaterm revive' or 'tamaterm init'.")
        return
    pet.stats.hygiene = min(100, pet.stats.hygiene + 30)
    from datetime import datetime, timezone
    pet.last_interaction = datetime.now(timezone.utc).isoformat()
    pet.save()
    click.echo(f"Cleaned {pet.name}! Hygiene +30")


@cli.command()
def sleep():
    """Put your pet to bed. Recovers energy."""
    pet = PetState.load()
    if pet.mood == Mood.DEAD:
        click.echo(f"{pet.name} is dead.")
        return
    pet.mood = Mood.SLEEPING
    pet.stats.energy = min(100, pet.stats.energy + 15)
    from datetime import datetime, timezone
    pet.last_interaction = datetime.now(timezone.utc).isoformat()
    pet.save()
    click.echo(f"{pet.name} is now sleeping... Energy +15")


@cli.command()
def status():
    """Show detailed pet status."""
    pet = PetState.load()
    click.echo(f"Name:    {pet.name}")
    click.echo(f"Type:    {pet.pet_type.value}")
    click.echo(f"Stage:   {pet.stage.value}")
    click.echo(f"Mood:    {pet.mood.value}")
    click.echo(f"Hunger:  {pet.stats.hunger:.1f}/100")
    click.echo(f"Happy:   {pet.stats.happiness:.1f}/100")
    click.echo(f"Energy:  {pet.stats.energy:.1f}/100")
    click.echo(f"Clean:   {pet.stats.hygiene:.1f}/100")
    click.echo(f"Commits: {pet.total_commits}")
    click.echo(f"Feeds:   {pet.total_feeds}")
    click.echo(f"Plays:   {pet.total_plays}")


@cli.command()
def revive():
    """Revive a dead pet (resets to baby stage)."""
    pet = PetState.load()
    if pet.mood != Mood.DEAD:
        click.echo(f"{pet.name} is alive and well!")
        return
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()
    pet.stage = Stage.BABY
    pet.mood = Mood.NORMAL
    pet.stats = Stats()
    pet.death_time = None
    pet.birthday = now
    pet.last_interaction = now
    pet.last_decay = now
    pet.save()
    click.echo(f"{pet.name} has been revived! Back to baby stage.")


@cli.command()
def doctor():
    """Check tamaterm installation health."""
    from .platform_compat import is_process_running

    issues = []
    if not DATA_DIR.exists():
        issues.append("~/.tamaterm directory missing")
    if not PET_FILE.exists():
        issues.append("No pet found. Run 'tamaterm init'")
    if not STATUS_FILE.exists():
        issues.append("Status file missing. Daemon may not be running.")
    if DAEMON_PID_FILE.exists():
        pid = int(DAEMON_PID_FILE.read_text().strip())
        if is_process_running(pid):
            click.echo(f"Daemon PID: {pid}")
        else:
            issues.append(f"Daemon PID {pid} is not running (stale PID file). Run 'tamaterm start'")
    else:
        issues.append("Daemon not running. Run 'tamaterm start'")
    if issues:
        for i in issues:
            click.echo(f"  x {i}")
    else:
        click.echo("  Everything looks good!")


@cli.command()
def install():
    """Install shell hook for your terminal."""
    from .install import detect_shell, install_hook

    shell = detect_shell()
    if shell:
        install_hook(shell)
        click.echo(f"Installed hook for {shell}. Restart your terminal.")
    else:
        click.echo("Could not detect shell. See README for manual setup.")


@cli.command()
def uninstall():
    """Remove shell hook."""
    from .install import detect_shell, uninstall_hook

    shell = detect_shell()
    if shell:
        uninstall_hook(shell)
        click.echo(f"Removed hook for {shell}.")


@cli.command()
def start():
    """Start the background daemon."""
    from .daemon import start_daemon
    start_daemon()
    click.echo("Daemon started.")


@cli.command()
def stop():
    """Stop the background daemon."""
    from .daemon import stop_daemon
    stop_daemon()
    click.echo("Daemon stopped.")
