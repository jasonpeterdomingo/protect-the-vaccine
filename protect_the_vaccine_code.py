"""
- Name: Protect the Vaccine
- Jason Domingo: jayprdom@udel.edu

Image sources:
- https://creazilla.com/nodes/49809-man-scientist-emoji-clipart
"""

from designer import *
from dataclasses import dataclass


@dataclass
class Keys:
    """
    These are the gaming keys
    """
    key_w: bool
    key_s: bool
    key_a: bool
    key_d: bool


@dataclass
class World:
    """
    Creates all the variables needed to make the game work
    """
    scientist: DesignerObject
    scientist_speed: int
    keys: Keys


def create_world() -> World:
    """ Create the world"""
    return World(create_scientist(), 10,
                 Keys(False, False, False, False))


def create_scientist() -> DesignerObject:
    """ Create the scientist"""
    scientist = image("images/scientist.png")
    return scientist


def move_left(world: World):
    """ Move the scientist left"""
    world.scientist.flip_x = True
    world.scientist.x += -world.scientist_speed


def move_right(world: World):
    """ Move the scientist right"""
    world.scientist.flip_x = False
    world.scientist.x += world.scientist_speed


def move_up(world: World):
    """ Move the scientist up"""
    world.scientist.y += -world.scientist_speed


def move_down(world: World):
    """ Move the scientist down"""
    world.scientist.y += world.scientist_speed


def press_key(key: str, world: World):
    """ When a key is pressed, the respected Boolean is activated """
    if key == "w":
        world.keys.key_w = True
    elif key == "s":
        world.keys.key_s = True
    elif key == "a":
        world.keys.key_a = True
    elif key == "d":
        world.keys.key_d = True


def release_key(key: str, world: World):
    """ When a key is released, the respected Boolean is deactivated"""
    if key == "w":
        world.keys.key_w = False
    elif key == "s":
        world.keys.key_s = False
    elif key == "a":
        world.keys.key_a = False
    elif key == "d":
        world.keys.key_d = False


def control_scientist(world: World):
    if world.keys.key_w:
        move_up(world)
    elif world.keys.key_s:
        move_down(world)
    elif world.keys.key_a:
        move_left(world)
    elif world.keys.key_d:
        move_right(world)


when("starting", create_world)
when("typing", press_key)
when("done typing", release_key)
when("updating", control_scientist)
start()
