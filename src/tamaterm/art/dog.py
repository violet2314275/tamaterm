from ..art_registry import register_art, register_art_default
from ..constants import PetType, Stage, Mood


@register_art_default(PetType.DOG, Stage.EGG)
def dog_egg():
    return [
        "    .---.    ",
        "   /     \\   ",
        "  |   o   |  ",
        "  |       |  ",
        "   '-----'   ",
    ]


@register_art(PetType.DOG, Stage.EGG, Mood.HAPPY)
def dog_egg_happy():
    return [
        "    .---.    ",
        "   /     \\   ",
        "  |   *   |  ",
        "  |       |  ",
        "   '-----'   ",
    ]


@register_art(PetType.DOG, Stage.EGG, Mood.HUNGRY)
def dog_egg_hungry():
    return [
        "    .---.    ",
        "   /     \\   ",
        "  |   ~   |  ",
        "  |       |  ",
        "   '-----'   ",
    ]


@register_art(PetType.DOG, Stage.EGG, Mood.SLEEPING)
def dog_egg_sleeping():
    return [
        "    .---.    ",
        "   /     \\   ",
        "  |   -   |  ",
        "  |       |  ",
        "   '-----'   ",
        "   z Z z     ",
    ]


@register_art(PetType.DOG, Stage.EGG, Mood.SAD)
def dog_egg_sad():
    return [
        "    .---.    ",
        "   /     \\   ",
        "  |   .   |  ",
        "  |       |  ",
        "   '-----'   ",
    ]


@register_art(PetType.DOG, Stage.EGG, Mood.DEAD)
def dog_egg_dead():
    return [
        "    .---.    ",
        "   /     \\   ",
        "  |   x   |  ",
        "  |       |  ",
        "   '-----'   ",
        "     RIP     ",
    ]


@register_art_default(PetType.DOG, Stage.BABY)
def dog_baby():
    return [
        "  /\\   /\\  ",
        " ( o . o ) ",
        "  >  V  <  ",
    ]


@register_art(PetType.DOG, Stage.BABY, Mood.HAPPY)
def dog_baby_happy():
    return [
        "  /\\   /\\  ",
        " ( ^ . ^ ) ",
        "  >  V  <  ",
        "    *w*    ",
    ]


@register_art(PetType.DOG, Stage.BABY, Mood.HUNGRY)
def dog_baby_hungry():
    return [
        "  /\\   /\\  ",
        " ( o . o ) ",
        "  >  ~  <  ",
    ]


@register_art(PetType.DOG, Stage.BABY, Mood.SLEEPING)
def dog_baby_sleeping():
    return [
        "  /\\   /\\  ",
        " ( - . - ) ",
        "  >  V  <  ",
        "   z Z z   ",
    ]


@register_art(PetType.DOG, Stage.BABY, Mood.DEAD)
def dog_baby_dead():
    return [
        "  /\\   /\\  ",
        " ( x . x ) ",
        "  >  V  <  ",
        "    RIP    ",
    ]


@register_art_default(PetType.DOG, Stage.TEEN)
def dog_teen():
    return [
        "   /\\    /\\   ",
        "  ( o  . o )  ",
        "   >   V  <   ",
        "   /|    |\\   ",
        "  (_|    |_)  ",
    ]


@register_art(PetType.DOG, Stage.TEEN, Mood.HAPPY)
def dog_teen_happy():
    return [
        "   /\\    /\\   ",
        "  ( ^  . ^ )  ",
        "   >   V  <   ",
        "   /|    |\\   ",
        "  (_|    |_)  ",
        "     *w*      ",
    ]


@register_art(PetType.DOG, Stage.TEEN, Mood.DEAD)
def dog_teen_dead():
    return [
        "   /\\    /\\   ",
        "  ( x  . x )  ",
        "   >   V  <   ",
        "   /|    |\\   ",
        "  (_|    |_)  ",
        "     RIP      ",
    ]


@register_art(PetType.DOG, Stage.TEEN, Mood.HUNGRY)
def dog_teen_hungry():
    return [
        "   /\\    /\\   ",
        "  ( o  . o )  ",
        "   >   ~  <   ",
        "   /|    |\\   ",
        "  (_|    |_)  ",
    ]


@register_art(PetType.DOG, Stage.TEEN, Mood.SLEEPING)
def dog_teen_sleeping():
    return [
        "   /\\    /\\   ",
        "  ( -  . - )  ",
        "   >   V  <   ",
        "   /|    |\\   ",
        "  (_|    |_)  ",
        "    z Z z     ",
    ]


@register_art_default(PetType.DOG, Stage.ADULT)
def dog_adult():
    return [
        "   /\\       /\\    ",
        "  / o\\     / o \\  ",
        " ( ==  \\___/  == )",
        "  )              ( ",
        " (    \\_____/    ) ",
        "  \\_)  (   )  (_/  ",
        "      (___)        ",
    ]


@register_art(PetType.DOG, Stage.ADULT, Mood.HAPPY)
def dog_adult_happy():
    return [
        "   /\\       /\\    ",
        "  / *\\     / * \\  ",
        " ( ==  \\___/  == )",
        "  )      ~     ( ",
        " (    \\_____/    ) ",
        "  \\_)  (   )  (_/  ",
        "      (___)        ",
    ]


@register_art(PetType.DOG, Stage.ADULT, Mood.DEAD)
def dog_adult_dead():
    return [
        "   /\\       /\\    ",
        "  / x\\     / x \\  ",
        " ( ==  \\___/  == )",
        "  )              ( ",
        " (    \\_____/    ) ",
        "  \\_)  (   )  (_/  ",
        "      (___)        ",
        "       RIP         ",
    ]


@register_art(PetType.DOG, Stage.ADULT, Mood.HUNGRY)
def dog_adult_hungry():
    return [
        "   /\\       /\\    ",
        "  / o\\     / o \\  ",
        " ( ==  \\___/  == )",
        "  )       ~     ( ",
        " (    \\_____/    ) ",
        "  \\_)  (   )  (_/  ",
        "      (___)        ",
    ]


@register_art(PetType.DOG, Stage.ADULT, Mood.SLEEPING)
def dog_adult_sleeping():
    return [
        "   /\\       /\\    ",
        "  / -\\     / - \\  ",
        " ( ==  \\___/  == )",
        "  )              ( ",
        " (    \\_____/    ) ",
        "  \\_)  (   )  (_/  ",
        "      (___)        ",
        "      z Z z        ",
    ]


@register_art(PetType.DOG, Stage.ADULT, Mood.SAD)
def dog_adult_sad():
    return [
        "   /\\       /\\    ",
        "  / .\\     / . \\  ",
        " ( ==  \\___/  == )",
        "  )       v     ( ",
        " (    \\_____/    ) ",
        "  \\_)  (   )  (_/  ",
        "      (___)        ",
    ]
