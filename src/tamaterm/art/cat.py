from ..art_registry import register_art, register_art_default
from ..constants import PetType, Stage, Mood


@register_art_default(PetType.CAT, Stage.EGG)
def cat_egg():
    return [
        "    .---.    ",
        "   /     \\   ",
        "  |   o   |  ",
        "  |       |  ",
        "   '-----'   ",
    ]


@register_art(PetType.CAT, Stage.EGG, Mood.HAPPY)
def cat_egg_happy():
    return [
        "    .---.    ",
        "   /     \\   ",
        "  |   *   |  ",
        "  |       |  ",
        "   '-----'   ",
    ]


@register_art(PetType.CAT, Stage.EGG, Mood.HUNGRY)
def cat_egg_hungry():
    return [
        "    .---.    ",
        "   /     \\   ",
        "  |   ~   |  ",
        "  |       |  ",
        "   '-----'   ",
    ]


@register_art(PetType.CAT, Stage.EGG, Mood.SLEEPING)
def cat_egg_sleeping():
    return [
        "    .---.    ",
        "   /     \\   ",
        "  |   -   |  ",
        "  |       |  ",
        "   '-----'   ",
        "   z Z z     ",
    ]


@register_art(PetType.CAT, Stage.EGG, Mood.SAD)
def cat_egg_sad():
    return [
        "    .---.    ",
        "   /     \\   ",
        "  |   .   |  ",
        "  |       |  ",
        "   '-----'   ",
    ]


@register_art(PetType.CAT, Stage.EGG, Mood.DEAD)
def cat_egg_dead():
    return [
        "    .---.    ",
        "   /     \\   ",
        "  |   x   |  ",
        "  |       |  ",
        "   '-----'   ",
        "     RIP     ",
    ]


@register_art_default(PetType.CAT, Stage.BABY)
def cat_baby():
    return [
        "  /\\_/\\  ",
        " ( o.o ) ",
        "  > ^ <  ",
    ]


@register_art(PetType.CAT, Stage.BABY, Mood.HAPPY)
def cat_baby_happy():
    return [
        "  /\\_/\\  ",
        " ( ^.^ ) ",
        "  > ^ <  ",
    ]


@register_art(PetType.CAT, Stage.BABY, Mood.HUNGRY)
def cat_baby_hungry():
    return [
        "  /\\_/\\  ",
        " ( o.o ) ",
        "  > ~ <  ",
    ]


@register_art(PetType.CAT, Stage.BABY, Mood.SLEEPING)
def cat_baby_sleeping():
    return [
        "  /\\_/\\  ",
        " ( -.- ) ",
        "  > ^ <  ",
        "  z Z z  ",
    ]


@register_art(PetType.CAT, Stage.BABY, Mood.SAD)
def cat_baby_sad():
    return [
        "  /\\_/\\  ",
        " ( ._. ) ",
        "  > ^ <  ",
    ]


@register_art(PetType.CAT, Stage.BABY, Mood.DEAD)
def cat_baby_dead():
    return [
        "  /\\_/\\  ",
        " ( x.x ) ",
        "  > ^ <  ",
        "   RIP   ",
    ]


@register_art_default(PetType.CAT, Stage.TEEN)
def cat_teen():
    return [
        "   /\\_/\\   ",
        "  ( o.o )  ",
        "   > ^ <   ",
        "  /|   |\\  ",
        " (_|   |_) ",
    ]


@register_art(PetType.CAT, Stage.TEEN, Mood.HAPPY)
def cat_teen_happy():
    return [
        "   /\\_/\\   ",
        "  ( ^.^ )  ",
        "   > ^ <   ",
        "  /|   |\\  ",
        " (_|   |_) ",
    ]


@register_art(PetType.CAT, Stage.TEEN, Mood.SLEEPING)
def cat_teen_sleeping():
    return [
        "   /\\_/\\   ",
        "  ( -.- )  ",
        "   > ^ <   ",
        "  /|   |\\  ",
        " (_|   |_) ",
        "   z Z z   ",
    ]


@register_art(PetType.CAT, Stage.TEEN, Mood.DEAD)
def cat_teen_dead():
    return [
        "   /\\_/\\   ",
        "  ( x.x )  ",
        "   > ^ <   ",
        "  /|   |\\  ",
        " (_|   |_) ",
        "    RIP    ",
    ]


@register_art(PetType.CAT, Stage.TEEN, Mood.HUNGRY)
def cat_teen_hungry():
    return [
        "   /\\_/\\   ",
        "  ( o.o )  ",
        "   > ~ <   ",
        "  /|   |\\  ",
        " (_|   |_) ",
    ]


@register_art(PetType.CAT, Stage.TEEN, Mood.SAD)
def cat_teen_sad():
    return [
        "   /\\_/\\   ",
        "  ( ._. )  ",
        "   > ^ <   ",
        "  /|   |\\  ",
        " (_|   |_) ",
    ]


@register_art_default(PetType.CAT, Stage.ADULT)
def cat_adult():
    return [
        "    /\\_____/\\    ",
        "   /  o   o  \\   ",
        "  ( ==  ^  == )  ",
        "   )         (   ",
        "  (           )  ",
        " ( (  )   (  ) ) ",
        "(__|__|___|__|__)",
    ]


@register_art(PetType.CAT, Stage.ADULT, Mood.HAPPY)
def cat_adult_happy():
    return [
        "    /\\_____/\\    ",
        "   /  *   *  \\   ",
        "  ( ==  w  == )  ",
        "   )    ~    (   ",
        "  (           )  ",
        " ( (  )   (  ) ) ",
        "(__|__|___|__|__)",
    ]


@register_art(PetType.CAT, Stage.ADULT, Mood.SLEEPING)
def cat_adult_sleeping():
    return [
        "    /\\_____/\\    ",
        "   /  -   -  \\   ",
        "  ( ==  w  == )  ",
        "   )  z Z    (   ",
        "  (           )  ",
        " ( (  )   (  ) ) ",
        "(__|__|___|__|__)",
    ]


@register_art(PetType.CAT, Stage.ADULT, Mood.HUNGRY)
def cat_adult_hungry():
    return [
        "    /\\_____/\\    ",
        "   /  o   o  \\   ",
        "  ( ==  ~  == )  ",
        "   )         (   ",
        "  (           )  ",
        " ( (  )   (  ) ) ",
        "(__|__|___|__|__)",
    ]


@register_art(PetType.CAT, Stage.ADULT, Mood.DEAD)
def cat_adult_dead():
    return [
        "    /\\_____/\\    ",
        "   /  x   x  \\   ",
        "  ( ==  -  == )  ",
        "   )         (   ",
        "  (           )  ",
        " ( (  )   (  ) ) ",
        "(__|__|___|__|__)",
        "      RIP        ",
    ]


@register_art(PetType.CAT, Stage.ADULT, Mood.SAD)
def cat_adult_sad():
    return [
        "    /\\_____/\\    ",
        "   /  .   .  \\   ",
        "  ( ==  v  == )  ",
        "   )         (   ",
        "  (           )  ",
        " ( (  )   (  ) ) ",
        "(__|__|___|__|__)",
    ]
