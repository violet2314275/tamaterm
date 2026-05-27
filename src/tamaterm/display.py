from .constants import Mood, Stage
from .state import PetState
from .art_registry import get_art

BAR_WIDTH = 20

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"


def color_for_value(value: float) -> str:
    if value > 60:
        return GREEN
    if value > 30:
        return YELLOW
    return RED


def color_for_mood(mood: Mood) -> str:
    mapping = {
        Mood.HAPPY: CYAN,
        Mood.SLEEPING: DIM,
        Mood.DEAD: RED,
        Mood.HUNGRY: YELLOW,
        Mood.SAD: BLUE,
        Mood.SLEEPY: DIM,
    }
    return mapping.get(mood, "")


def stat_bar(value: float, width: int = BAR_WIDTH, use_color: bool = True) -> str:
    filled = int(value / 100 * width)
    empty = width - filled
    if use_color:
        color = color_for_value(value)
        return f"{color}{'#' * filled}{DIM}{'-' * empty}{RESET}"
    return f"{'#' * filled}{'-' * empty}"


def mood_symbol(mood: Mood) -> str:
    mapping = {
        Mood.NORMAL: "*",
        Mood.HAPPY: "^",
        Mood.HUNGRY: "~",
        Mood.SAD: "v",
        Mood.SLEEPY: "z",
        Mood.SLEEPING: "Z",
        Mood.DEAD: "x",
    }
    return mapping.get(mood, "*")


def build_frame(pet: PetState, use_color: bool = True) -> str:
    art_lines = get_art(pet.pet_type, pet.stage, pet.mood)

    if use_color:
        mood_color = color_for_mood(pet.mood)
        colored_art = [f"{mood_color}{line}{RESET}" for line in art_lines]
    else:
        colored_art = art_lines

    art_block = "\n".join(colored_art)

    sym = mood_symbol(pet.mood)
    stage_label = pet.stage.value
    if use_color:
        header = f"{BOLD} {sym} {pet.name} [{stage_label}]{RESET}"
    else:
        header = f" {sym} {pet.name} [{stage_label}]"

    if use_color:
        stats_block = (
            f"  hunger  [{stat_bar(pet.stats.hunger, use_color=True)}] {color_for_value(pet.stats.hunger)}{pet.stats.hunger:5.1f}{RESET}\n"
            f"  happy   [{stat_bar(pet.stats.happiness, use_color=True)}] {color_for_value(pet.stats.happiness)}{pet.stats.happiness:5.1f}{RESET}\n"
            f"  energy  [{stat_bar(pet.stats.energy, use_color=True)}] {color_for_value(pet.stats.energy)}{pet.stats.energy:5.1f}{RESET}\n"
            f"  clean   [{stat_bar(pet.stats.hygiene, use_color=True)}] {color_for_value(pet.stats.hygiene)}{pet.stats.hygiene:5.1f}{RESET}"
        )
    else:
        stats_block = (
            f"  hunger  [{stat_bar(pet.stats.hunger, use_color=False)}] {pet.stats.hunger:5.1f}\n"
            f"  happy   [{stat_bar(pet.stats.happiness, use_color=False)}] {pet.stats.happiness:5.1f}\n"
            f"  energy  [{stat_bar(pet.stats.energy, use_color=False)}] {pet.stats.energy:5.1f}\n"
            f"  clean   [{stat_bar(pet.stats.hygiene, use_color=False)}] {pet.stats.hygiene:5.1f}"
        )

    width = max(len(line) for line in art_lines) + 4
    width = max(width, 30)
    border = "-" * width

    return f"+{border}+\n{header}\n{art_block}\n{stats_block}\n+{border}+"
