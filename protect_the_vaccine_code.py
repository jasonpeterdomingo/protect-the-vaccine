"""
- Name: Protect the Vaccine
- Jason Domingo: jayprdom@udel.edu

Image sources:
- https://creazilla.com/nodes/49809-man-scientist-emoji-clipart
- https://openclipart.org/detail/265273/male-zombie
- https://iconscout.com/free-icon/vaccine-2332187
"""

# *** Note to self: window is 800 x 600 ***

from designer import *
from dataclasses import dataclass
from random import randint

set_window_color("silver")


@dataclass
class Keys:
    """ These are the gaming keys """
    key_w: bool
    key_s: bool
    key_a: bool
    key_d: bool


@dataclass
class LastInput:
    """ Stores the latest gaming keystroke to determine direction laser shoots """
    key_w: bool
    key_s: bool
    key_a: bool
    key_d: bool


class Laser(circle):
    """ Give the laser a speed and direction """
    speed: int
    direction: int


@dataclass
class World:
    """ Creates all the variables needed to make the game work """
    scientist: DesignerObject
    scientist_speed: int
    keys: Keys
    lasers: list[Laser]
    last_keystroke: LastInput
    zombies: list[DesignerObject]
    vaccine: DesignerObject


def create_world() -> World:
    """ Create the world"""          
    return World(create_scientist(), 10,
                 Keys(False, False, False, False),
                 [],
                 LastInput(False, False, False, False),
                 [], create_vaccine())


def create_scientist() -> DesignerObject:
    """ Create the scientist"""
    scientist = image("images/scientist.png", 350, 355)
    scientist.scale_x = .4
    scientist.scale_y = .4
    return scientist


def move_left(world: World):
    """ Move the scientist left """
    world.scientist.flip_x = True
    world.scientist.x += -world.scientist_speed


def move_right(world: World):
    """ Move the scientist right """
    world.scientist.flip_x = False
    world.scientist.x += world.scientist_speed


def move_up(world: World):
    """ Move the scientist up """
    world.scientist.y += -world.scientist_speed


def move_down(world: World):
    """ Move the scientist down """
    world.scientist.y += world.scientist_speed


def press_key(key: str, world: World):
    """ When a key is pressed, the respected Boolean and the last keystroke is activated"""
    if key == "w":
        world.keys.key_w = True
        reset_last_input(world)
        world.last_keystroke.key_w = True
    if key == "s":
        world.keys.key_s = True
        reset_last_input(world)
        world.last_keystroke.key_s = True
    if key == "a":
        world.keys.key_a = True
        reset_last_input(world)
        world.last_keystroke.key_a = True
    if key == "d":
        world.keys.key_d = True
        reset_last_input(world)
        world.last_keystroke.key_d = True


def reset_last_input(world: World):
    """ Resets the last input so that the last keystroke can be stored """
    world.last_keystroke.key_w = False
    world.last_keystroke.key_s = False
    world.last_keystroke.key_a = False
    world.last_keystroke.key_d = False


def release_key(key: str, world: World):
    """ When a key is released, the respected Boolean is deactivated """
    if key == "w":
        world.keys.key_w = False
    if key == "s":
        world.keys.key_s = False
    if key == "a":
        world.keys.key_a = False
    if key == "d":
        world.keys.key_d = False


def control_scientist(world: World):
    """ Checks which key is pressed (True) and moves the character in the respected direction until False """
    if world.keys.key_w:
        move_up(world)
    if world.keys.key_s:
        move_down(world)
    if world.keys.key_a:
        move_left(world)
    if world.keys.key_d:
        move_right(world)


def check_boundaries(world: World):
    """Prevents the scientist from walking offscreen """
    if world.scientist.x > get_width():
        move_left(world)
    elif world.scientist.x < 0:
        move_right(world)
    if world.scientist.y > get_height():
        move_up(world)
    elif world.scientist.y < 0:
        move_down(world)


def create_laser() -> Laser:
    """ Create the laser """
    return Laser("red", 10, speed=10, direction=0)


def shoot_laser(world: World, key: str):
    """ Laser is shot when the user presses the space bar """
    if key == "space":
        if len(world.lasers) < 5:
            new_laser = create_laser()
            laser_position(new_laser, world.scientist, world.last_keystroke)
            world.lasers.append(new_laser)


def laser_position(laser: Laser, scientist_direction: DesignerObject,
                   shooting_direction: LastInput):
    """ Have the laser appear where the scientist is located """
    laser.y = scientist_direction.y
    laser.x = scientist_direction.x + 30
    if shooting_direction.key_w:
        laser.direction = 90
    elif shooting_direction.key_s:
        laser.direction = 270
    elif shooting_direction.key_a:
        laser.x = scientist_direction.x - 30
        laser.direction = 180
    elif shooting_direction.key_d:
        laser.direction = 360


def move_laser(world: World):
    """ Moves each laser at a constant speed and direction """
    for laser in world.lasers:
        move_forward(laser, laser.speed, laser.direction)


def destroy_laser_x(world: World):
    """ Destroys the laser that hits offscreen in the x-direction """
    kept = []
    for laser in world.lasers:
        if 0 < laser.x < get_width():
            kept.append(laser)
        else:
            destroy(laser)
    world.lasers = kept


def destroy_laser_y(world: World):
    """ Destroys the laser that hits offscreen in the y-direction """
    kept = []
    for laser in world.lasers:
        if 0 < laser.y < get_height():
            kept.append(laser)
        else:
            destroy(laser)
    world.lasers = kept


def create_zombie(x_cord: int, y_cord: int) -> DesignerObject:
    """ Creates the zombie """
    zombie = image("images/zombie.png", x_cord, y_cord)
    zombie.scale_x = .17
    zombie.scale_y = .17
    return zombie


def spawn_zombies(world: World):
    """ Spawns a zombie randomly between 4 different spawn points """
    spawn_point = randint(0, 250)
    if spawn_point == 0:
        world.zombies.append(create_zombie(get_width()/2, get_height()))
    elif spawn_point == 1:
        world.zombies.append(create_zombie(get_width(), get_height()/2))
    elif spawn_point == 2:
        world.zombies.append(create_zombie(get_width()/2, 0))
    elif spawn_point == 3:
        world.zombies.append(create_zombie(0, get_height()/2))


def collide_laser_zombie(world: World):
    """ Checks if the laser and zombie collides and removes them """
    destroyed_laser = []
    destroyed_zombie = []
    for laser in world.lasers:
        for zombie in world.zombies:
            if colliding(laser, zombie):
                destroyed_laser.append(laser)
                destroyed_zombie.append(zombie)
    world.lasers = filter_from(world.lasers, destroyed_laser)
    world.zombies = filter_from(world.zombies, destroyed_zombie)


def filter_from(old_list: list[DesignerObject], elements_to_remove: list[DesignerObject]):
    """ Destroys elements from the old list and returns a new list """
    new_list = []
    for item in old_list:
        if item in elements_to_remove:
            destroy(item)
        else:
            new_list.append(item)
    return new_list


def create_vaccine() -> DesignerObject:
    """ Create the vaccine """
    vaccine = image("images/vaccine.png")
    return vaccine


def collide_vaccine_scientist(world: World):
    """ Prevents the scientist from walking over vaccine """
    if colliding(world.scientist, world.vaccine):
        if world.last_keystroke.key_w:
            move_down(world)
        elif world.last_keystroke.key_s:
            move_up(world)
        elif world.last_keystroke.key_a:
            move_right(world)
        elif world.last_keystroke.key_d:
            move_left(world)


when("starting", create_world)
when("typing", press_key)
when("done typing", release_key)
when("updating", control_scientist)
when("typing", shoot_laser)
when("updating", move_laser)
when("updating", destroy_laser_x)
when("updating", destroy_laser_y)
when("updating", check_boundaries)
when("updating", spawn_zombies)
when("updating", collide_laser_zombie)
when("updating", collide_vaccine_scientist)
start()
