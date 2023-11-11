"""
- Name: Protect the Vaccine
- Jason Domingo: jayprdom@udel.edu

Image sources:
- https://creazilla.com/nodes/49809-man-scientist-emoji-clipart
"""

from designer import *
from dataclasses import dataclass
from random import randint

set_window_color("silver")


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
    lasers: list[DesignerObject]
    zombies: list[DesignerObject]


def create_world() -> World:
    """ Create the world"""          
    return World(create_scientist(), 10,
                 Keys(False, False, False, False),
                 [], [])


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
    if key == "s":
        world.keys.key_s = True
    if key == "a":
        world.keys.key_a = True
    if key == "d":
        world.keys.key_d = True


def release_key(key: str, world: World):
    """ When a key is released, the respected Boolean is deactivated"""
    if key == "w":
        world.keys.key_w = False
    if key == "s":
        world.keys.key_s = False
    if key == "a":
        world.keys.key_a = False
    if key == "d":
        world.keys.key_d = False


def control_scientist(world: World):
    """ Checks which key is pressed (True) and moves the character in the respected direction until False"""
    if world.keys.key_w:
        move_up(world)
    if world.keys.key_s:
        move_down(world)
    if world.keys.key_a:
        move_left(world)
    if world.keys.key_d:
        move_right(world)


def check_boundaries(world: World):
    """Prevents the scientist from walking offscreen"""
    if world.scientist.x > get_width():
        move_left(world)
    elif world.scientist.x < 0:
        move_right(world)
    if world.scientist.y > get_height():
        move_up(world)
    elif world.scientist.y < 0:
        move_down(world)


def create_laser() -> DesignerObject:
    """Create the laser"""
    return circle("red", 10)


def shoot_laser(world: World, key: str):
    """ Laser is shot"""
    if key == "space":
        if len(world.lasers) < 10:
            new_laser = create_laser()
            world.lasers.append(new_laser)


def shooting_direction(world: World):
    """ Have the laser move like a projectile"""
    LASER_SPEED = 5
    for laser in world.lasers:
        laser.x += LASER_SPEED


def destroy_laser(world: World):
    """ Destroy the laser that hits offscreen"""
    kept = []
    for laser in world.lasers:
        if laser.x < get_width(): # Need to add for y-direction
            kept.append(laser)
        else:
            destroy(laser)
    world.lasers = kept


def create_zombie(x_cord: int, y_cord: int) -> DesignerObject:
    """ Creates the zombie """
    zombie = emoji("zombie", x_cord, y_cord)
    return zombie


def spawn_zombies(world: World):
    spawn_point = randint(0, 250)
    if spawn_point == 0:
        world.zombies.append(create_zombie(get_width()/2, get_height()))
    elif spawn_point == 1:
        world.zombies.append(create_zombie(get_width(), get_height()/2))
    elif spawn_point == 2:
        world.zombies.append(create_zombie(get_width()/2, 0))
    elif spawn_point == 3:
        world.zombies.append(create_zombie(0, get_height()/2))


when("starting", create_world)
when("typing", press_key)
when("done typing", release_key)
when("updating", control_scientist)
when("typing", shoot_laser)
when("updating", shooting_direction)
when("updating", destroy_laser)
when("updating", check_boundaries)
when("updating", spawn_zombies)
start()
