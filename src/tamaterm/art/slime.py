from ..art_registry import register_art, register_art_default
from ..constants import PetType, Stage, Mood


@register_art_default(PetType.SLIME, Stage.EGG)
def slime_egg():
    return [
        "   .---.   ",
        "  /     \\  ",
        " |   o   | ",
        " |       | ",
        "  '-----'  ",
    ]


@register_art(PetType.SLIME, Stage.EGG, Mood.HAPPY)
def slime_egg_happy():
    return [
        "   .---.   ",
        "  /     \\  ",
        " |   *   | ",
        " |       | ",
        "  '-----'  ",
    ]


@register_art(PetType.SLIME, Stage.EGG, Mood.HUNGRY)
def slime_egg_hungry():
    return [
        "   .---.   ",
        "  /     \\  ",
        " |   ~   | ",
        " |       | ",
        "  '-----'  ",
    ]


@register_art(PetType.SLIME, Stage.EGG, Mood.SLEEPING)
def slime_egg_sleeping():
    return [
        "   .---.   ",
        "  /     \\  ",
        " |   -   | ",
        " |       | ",
        "  '-----'  ",
        "  z Z z    ",
    ]


@register_art(PetType.SLIME, Stage.EGG, Mood.SAD)
def slime_egg_sad():
    return [
        "   .---.   ",
        "  /     \\  ",
        " |   .   | ",
        " |       | ",
        "  '-----'  ",
    ]


@register_art(PetType.SLIME, Stage.EGG, Mood.DEAD)
def slime_egg_dead():
    return [
        "   .---.   ",
        "  /     \\  ",
        " |   x   | ",
        " |       | ",
        "  '-----'  ",
        "    RIP    ",
    ]


@register_art_default(PetType.SLIME, Stage.BABY)
def slime_baby():
    return [
        "  .--.  ",
        " / oo \\ ",
        "|  ~~  |",
        " '----' ",
    ]


@register_art(PetType.SLIME, Stage.BABY, Mood.HAPPY)
def slime_baby_happy():
    return [
        "  .--.  ",
        " / ** \\ ",
        "|  ~~  |",
        " '----' ",
    ]


@register_art(PetType.SLIME, Stage.BABY, Mood.HUNGRY)
def slime_baby_hungry():
    return [
        "  .--.  ",
        " / ;; \\ ",
        "|  ~~  |",
        " '----' ",
    ]


@register_art(PetType.SLIME, Stage.BABY, Mood.SLEEPING)
def slime_baby_sleeping():
    return [
        "  .--.  ",
        " / -- \\ ",
        "|  ~~  |",
        " '----' ",
        " z Z z  ",
    ]


@register_art(PetType.SLIME, Stage.BABY, Mood.DEAD)
def slime_baby_dead():
    return [
        "  .--.  ",
        " / xx \\ ",
        "|  ~~  |",
        " '----' ",
        "  RIP   ",
    ]


@register_art(PetType.SLIME, Stage.BABY, Mood.SAD)
def slime_baby_sad():
    return [
        "  .--.  ",
        " / .. \\ ",
        "|  ~~  |",
        " '----' ",
    ]


@register_art_default(PetType.SLIME, Stage.TEEN)
def slime_teen():
    return [
        "   .---.   ",
        "  / o o \\  ",
        " |  ===  | ",
        " |  ~~~  | ",
        "  '-----'  ",
    ]


@register_art(PetType.SLIME, Stage.TEEN, Mood.HAPPY)
def slime_teen_happy():
    return [
        "   .---.   ",
        "  / * * \\  ",
        " |  ===  | ",
        " |  ~~~  | ",
        "  '-----'  ",
    ]


@register_art(PetType.SLIME, Stage.TEEN, Mood.DEAD)
def slime_teen_dead():
    return [
        "   .---.   ",
        "  / x x \\  ",
        " |  ===  | ",
        " |  ~~~  | ",
        "  '-----'  ",
        "    RIP    ",
    ]


@register_art(PetType.SLIME, Stage.TEEN, Mood.HUNGRY)
def slime_teen_hungry():
    return [
        "   .---.   ",
        "  / ~ ~ \\  ",
        " |  ===  | ",
        " |  ~~~  | ",
        "  '-----'  ",
    ]


@register_art(PetType.SLIME, Stage.TEEN, Mood.SLEEPING)
def slime_teen_sleeping():
    return [
        "   .---.   ",
        "  / - - \\  ",
        " |  ===  | ",
        " |  ~~~  | ",
        "  '-----'  ",
        "  z Z z    ",
    ]


@register_art_default(PetType.SLIME, Stage.ADULT)
def slime_adult():
    return [
        "    .-----.    ",
        "   / o   o \\   ",
        "  |  ===    |  ",
        "  |  ~~~    |  ",
        "  |         |  ",
        "   '-------'   ",
    ]


@register_art(PetType.SLIME, Stage.ADULT, Mood.HAPPY)
def slime_adult_happy():
    return [
        "    .-----.    ",
        "   / *   * \\   ",
        "  |  ===    |  ",
        "  |  ~~~  ~ |  ",
        "  |         |  ",
        "   '-------'   ",
    ]


@register_art(PetType.SLIME, Stage.ADULT, Mood.DEAD)
def slime_adult_dead():
    return [
        "    .-----.    ",
        "   / x   x \\   ",
        "  |  ===    |  ",
        "  |  ~~~    |  ",
        "  |         |  ",
        "   '-------'   ",
        "      RIP      ",
    ]


@register_art(PetType.SLIME, Stage.ADULT, Mood.HUNGRY)
def slime_adult_hungry():
    return [
        "    .-----.    ",
        "   / ~   ~ \\   ",
        "  |  ===    |  ",
        "  |  ~~~    |  ",
        "  |         |  ",
        "   '-------'   ",
    ]


@register_art(PetType.SLIME, Stage.ADULT, Mood.SLEEPING)
def slime_adult_sleeping():
    return [
        "    .-----.    ",
        "   / -   - \\   ",
        "  |  ===    |  ",
        "  |  ~~~    |  ",
        "  |         |  ",
        "   '-------'   ",
        "    z Z z      ",
    ]


@register_art(PetType.SLIME, Stage.ADULT, Mood.SAD)
def slime_adult_sad():
    return [
        "    .-----.    ",
        "   / .   . \\   ",
        "  |  ===    |  ",
        "  |  ~~~    |  ",
        "  |         |  ",
        "   '-------'   ",
    ]
