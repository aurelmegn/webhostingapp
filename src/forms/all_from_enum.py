from enum import Enum


def all_from_enum(enum: Enum) -> [()]:
    val = [(x.value, x.name.capitalize()) for x in enum]
    # add a message of the style "please select"
    return val
