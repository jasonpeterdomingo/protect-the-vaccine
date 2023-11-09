"""
- Name: Protect the Vaccine
- Jason Domingo: jayprdom@udel.edu

Image sources:
- https://creazilla.com/nodes/49809-man-scientist-emoji-clipart
"""

from designer import *
from dataclasses import dataclass


@dataclass
class World:
    scientist: DesignerObject


def create_world() -> World:
    """Create the world"""
    return World(create_scientist())


def create_scientist() -> DesignerObject:
    """Create the scientist"""
    scientist = image("images/scientist.png")
    return scientist
    

def move_left(world: World):
    """Move the scientist left"""
    world.scientist.flip_x = True
    world.scientist.x += -1


def move_right(world: World):
    """Move the scientist right"""
    world.scientist.flip_x = False
    world.scientist.x += 1


def move_up(world: World):
    """Move the scientist up"""
    world.scientist.y += -1


def move_down(world: World):
    """Move the scientist down"""
    world.scientist.y += 1


def control_scientist(world: World, key: str):
    # Figure out how to make character move continuously when pressing down a key
    if key == "W":
        move_up(world)
    elif key == "S":
        move_down(world)
    elif key == "A":
        move_left(world)
    elif key == "D":
        move_right(world)


when("starting", create_world)
when("typing", control_scientist)
start()
