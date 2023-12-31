"""
- Name: Protect the Vaccine
- Jason Domingo: jayprdom@udel.edu

Image sources:
- https://creazilla.com/nodes/49809-man-scientist-emoji-clipart
- https://openclipart.org/detail/265273/male-zombie
- https://iconscout.com/free-icon/vaccine-2332187

Sources (reason for use is explained in the exact line used):
[1] https://docs.python.org/3/library/math.html
[2] https://www.w3schools.com/python/ref_string_format.asp
"""

from designer import *
from dataclasses import dataclass
from random import randint
import math

set_window_color("silver")


@dataclass
class Keys:
    """ These are the keys to move scientist """
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


class Zombie(image):
    """ The zombie's speed and direction """
    speed: int
    direction: float
    health: int


@dataclass
class Timer:
    """ The time information """
    frame_count: int
    game_time: int
    screen: DesignerObject


@dataclass
class Score:
    """ The score information """
    score: int
    screen: DesignerObject


@dataclass
class Results:
    """ Displays the results at the end"""
    header: DesignerObject


@dataclass
class World:
    """ Creates all the variables needed to make the game work """
    scientist: DesignerObject
    scientist_speed: int
    keys: Keys
    lasers: list[Laser]
    last_keystroke: LastInput
    zombies: list[Zombie]
    vaccine: DesignerObject
    time_info: Timer
    score_info: Score
    power_ups: list[DesignerObject]
    powered: bool
    power_up_index: list[int]


def create_world() -> World:
    """ Create the world

    Returns:
        World: the world screen dataclass
    """
    return World(create_scientist(), 10,
                 Keys(False, False, False, False),
                 [],
                 LastInput(False, False, False, False),
                 [], create_vaccine(),
                 Timer(900, 30,
                       text("black", "{sec}", 25, get_width()/2, 20)),
                 Score(0, text("black", "Score: {score}", 25, get_width()/2, 80)),
                 [], False, [])


def create_game_over() -> Results:
    """ Displays if you lose

    Returns:
        Results: the dataclass displayed in another screen
    """
    return Results(text("black", "YOU LOST!", 25, get_width() / 2, 20))


def create_you_win() -> Results:
    """ Displays if you win

       Returns:
        Results: the dataclass displayed in another screen
    """
    return Results(text("black", "YOU WIN!", 25, get_width() / 2, 20))


def game_timer(world: World):
    """ Updates frame count, game time, and score

    Args:
        world (World): the World dataclass
    """
    world.time_info.frame_count -= 1
    if world.time_info.frame_count % 30 == 0:
        world.time_info.game_time -= 1
    if world.time_info.frame_count % 300 == 0:
        world.score_info.score += 10
        difficulty_increase(world)


def stop_game(world: World) -> bool:
    """ Stops the game once the game timer reaches 0 (after 30 seconds)

    Args:
        world (World): the World dataclass
    Returns:
        bool: weather the game is running or not running
    """
    game_not_running = False
    if world.time_info.frame_count == 0:
        game_not_running = True
        change_scene("you_win")
    return game_not_running


def create_scientist() -> DesignerObject:
    """ Create the scientist

    Returns:
        DesignerObject: the image of a scientist (player)
    """
    scientist = image("images/scientist.png", 350, 300)
    scientist.scale_x = .4
    scientist.scale_y = .4
    return scientist


def move_left(world: World):
    """ Move the scientist left

    Args:
        world (World): the World dataclass
    """
    world.scientist.flip_x = True
    world.scientist.x += -world.scientist_speed


def move_right(world: World):
    """ Move the scientist right

    Args:
        world (World): the World dataclass
    """
    world.scientist.flip_x = False
    world.scientist.x += world.scientist_speed


def move_up(world: World):
    """ Move the scientist up

    Args:
        world (World): the World dataclass
    """
    world.scientist.y += -world.scientist_speed


def move_down(world: World):
    """ Move the scientist down

    Args:
        world (World): the World dataclass
    """
    world.scientist.y += world.scientist_speed


def press_key(key: str, world: World):
    """ When a key is pressed, the respected Boolean and the last keystroke is activated

    Args:
        key (str): the key pressed
        world (World): the World dataclass
    """
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
    """ Resets the last input so that the last keystroke can be stored

    Args:
        world (World): the World dataclass
    """
    world.last_keystroke.key_w = False
    world.last_keystroke.key_s = False
    world.last_keystroke.key_a = False
    world.last_keystroke.key_d = False


def release_key(key: str, world: World):
    """ When a key is released, the respected Boolean is deactivated

    Args:
        key (str): the key released
        world (World): the World dataclass
    """
    if key == "w":
        world.keys.key_w = False
    if key == "s":
        world.keys.key_s = False
    if key == "a":
        world.keys.key_a = False
    if key == "d":
        world.keys.key_d = False


def control_scientist(world: World):
    """ Checks which key is pressed (True) and moves the character in the respected direction until False

    Args:
        world (World): the World dataclass
    """
    if world.keys.key_w:
        move_up(world)
    if world.keys.key_s:
        move_down(world)
    if world.keys.key_a:
        move_left(world)
    if world.keys.key_d:
        move_right(world)


def check_boundaries(world: World):
    """Prevents the scientist from walking offscreen

    Args:
        world (World): the World dataclass
    """
    if world.scientist.x > get_width():
        move_left(world)
    elif world.scientist.x < 0:
        move_right(world)
    if world.scientist.y > get_height():
        move_up(world)
    elif world.scientist.y < 0:
        move_down(world)


def create_laser(radius: int) -> Laser:
    """ Create the laser

    Args:
        radius (int): how wide the circle should be drawn
    Returns:
        the Laser circle dataclass with individual speed and direction
    """
    return Laser("red", radius, speed=10, direction=0)


def shoot_laser(world: World, key: str):
    """ Laser is shot when the user presses the space bar

    Args:
        world (World): the World dataclass
        key: the key pressed
    """
    radius = 10
    if world.powered:
        radius = 30
    if len(world.lasers) < 5:
        if key == "space":
            new_laser = create_laser(radius)
            laser_position(new_laser, world.scientist, world.last_keystroke)
            world.lasers.append(new_laser)
        if key == "q":
            new_laser = create_laser(radius)
            diagonal_shot(new_laser, world.scientist, "q")
            world.lasers.append(new_laser)
        if key == "e":
            new_laser = create_laser(radius)
            diagonal_shot(new_laser, world.scientist, "e")
            world.lasers.append(new_laser)
        if key == "z":
            new_laser = create_laser(radius)
            diagonal_shot(new_laser, world.scientist, "z")
            world.lasers.append(new_laser)
        if key == "x":
            new_laser = create_laser(radius)
            diagonal_shot(new_laser, world.scientist, "x")
            world.lasers.append(new_laser)


def laser_position(laser: Laser, scientist_direction: DesignerObject,
                   shooting_direction: LastInput):
    """ Have the laser appear where the scientist is located and shoot based on last input

    Args:
        laser (Laser): the circle dataclass Laser
        scientist_direction (DesignerObject): where the scientist exists on screen
        shooting_direction (LastInput): the last input recorded to determine shooting direction
    """
    laser.y = scientist_direction.y
    laser.x = scientist_direction.x
    if shooting_direction.key_w:
        laser.direction = 90
    elif shooting_direction.key_s:
        laser.direction = 270
    elif shooting_direction.key_a:
        laser.x = scientist_direction.x - 30
        laser.direction = 180
    elif shooting_direction.key_d:
        laser.direction = 360


def diagonal_shot(laser: Laser, scientist_direction: DesignerObject, key_pressed: str):
    """ Have the laser appear where the scientist is and shoots diagonally based on key pressed

    Args:
        laser (Laser): the circle Laser dataclass
        scientist_direction (DesignerObject): where the scientist is located
        key_pressed: the key pressed
    """
    laser.y = scientist_direction.y
    laser.x = scientist_direction.x
    if key_pressed == "q":
        laser.direction = 135
    elif key_pressed == "e":
        laser.direction = 45
    elif key_pressed == "z":
        laser.direction = 225
    elif key_pressed == "x":
        laser.direction = 315


def move_laser(world: World):
    """ Moves each laser at a constant speed and direction

     Args:
        world (World): the World dataclass
    """
    for laser in world.lasers:
        move_forward(laser, laser.speed, laser.direction)


def destroy_laser_x(world: World):
    """ Destroys the laser that hits offscreen in the x-direction

    Args:
        world (World): the World dataclass
    """
    kept = []
    for laser in world.lasers:
        if 0 < laser.x < get_width():
            kept.append(laser)
        else:
            destroy(laser)
    world.lasers = kept


def destroy_laser_y(world: World):
    """ Destroys the laser that hits offscreen in the y-direction

    Args:
        world (World): the World dataclass
    """
    kept = []
    for laser in world.lasers:
        if 0 < laser.y < get_height():
            kept.append(laser)
        else:
            destroy(laser)
    world.lasers = kept


def create_zombie(x_cord: int, y_cord: int, speed: int, health: int) -> Zombie:
    """ Creates the zombie

    Args:
        x_cord (int): the x-coordinate of the zombie
        y_cord (int): the y-coordinate of the zombie
        speed (int): the speed of the zombie
        health (int): the health of the zombie
    Returns:
        Zombie: the zombie image dataclass with its speed, direction, and health
    """
    return Zombie("images/zombie.png", x_cord, y_cord, speed=speed, direction=0, health=health)


def spawn_zombies(world: World):
    """ Spawns a zombie randomly between 4 different spawn points

    Args:
        world (World): the World dataclass
    """
    speed = 1
    health = 1
    quantity = 5
    if world.time_info.frame_count <= 600:
        speed = 2
        health = 200
        quantity = 8
    elif world.time_info.frame_count <= 300:
        speed = 3
        health = 300
        quantity = 10
    spawn_point = randint(0, 250)
    if len(world.zombies) < quantity:
        if spawn_point == 0:
            new_zombie = create_zombie(randint(0, 800), get_height(), speed, health)
            new_zombie.scale_x = .17
            new_zombie.scale_y = .17
            world.zombies.append(new_zombie)
        elif spawn_point == 1:
            new_zombie = create_zombie(get_width(), randint(0, 600), speed, health)
            new_zombie.scale_x = .17
            new_zombie.scale_y = .17
            world.zombies.append(new_zombie)
        elif spawn_point == 2:
            new_zombie = create_zombie(randint(0, 800), 0, speed, health)
            new_zombie.scale_x = .17
            new_zombie.scale_y = .17
            world.zombies.append(new_zombie)
        elif spawn_point == 3:
            new_zombie = create_zombie(0, randint(0, 600), speed, health)
            new_zombie.scale_x = .17
            new_zombie.scale_y = .17
            world.zombies.append(new_zombie)


def find_closer_entity(world: World):
    """ Determine who the zombie should follow

    Args:
        world (World): the World dataclass
    """
    for zombie in world.zombies:
        if ((zombie.x - world.vaccine.x) < (zombie.x - world.scientist.x) or
                (zombie.y - world.vaccine.y) < (zombie.y - world.scientist.y)):
            zombie_direction(zombie, world.vaccine)
        elif ((zombie.x - world.vaccine.x) > (zombie.x - world.scientist.x) or
              (zombie.y - world.vaccine.y) < (zombie.y - world.scientist.y)):
            zombie_direction(zombie, world.scientist)


def zombie_direction(zombie: Zombie, entity: DesignerObject):
    """ Change the direction of the zombie to follow the entity

    Args:
        zombie (Zombie): the image Zombie dataclass
        entity (DesignerObject): either the scientist or vaccine
    """
    if zombie.x > entity.x:
        zombie.flip_x = True
        zombie.direction = get_angle(entity, zombie)
    elif zombie.x < entity.x:
        zombie.flip_x = False
        zombie.direction = get_angle(entity, zombie)
    if zombie.y > entity.y:
        zombie.direction = get_angle(entity, zombie)
    elif zombie.y < entity.y:
        zombie.direction = get_angle(entity, zombie)


def get_angle(entity: DesignerObject, zombie: Zombie) -> float:
    """ Gets the angle for the zombie's direction

    Args:
        entity (DesignerObject): either the vaccine or scientist
        zombie (Zombie): the zombie following the entity
    Returns:
        float: the degrees which the zombie should travel to reach the entity
    """
    # [1] was used to apply atan2: the arc tangent function to calculate the angle between the x and y coordinate
    rise = entity.y - zombie.y
    run = entity.x - zombie.x
    return math.degrees(math.atan2(-rise, run)) % 360  # Had help from Dr. Bart to fix equation


def move_zombie(world: World):
    """ Move each zombie

    Args:
        world (World): the World dataclass
    """
    for zombie in world.zombies:
        move_forward(zombie, zombie.speed, zombie.direction)


def collide_laser_zombie(world: World):
    """ Checks if the laser and zombie collides and removes them

    Args:
        world (World): the World dataclass
    """
    destroyed_laser = []
    destroyed_zombie = []
    for laser in world.lasers:
        for zombie in world.zombies:
            if colliding(laser, zombie):
                if laser.radius == 30:
                    zombie.health -= 300
                zombie.health -= 100
                if zombie.health <= 0:
                    destroyed_laser.append(laser)
                    destroyed_zombie.append(zombie)
                    create_power_ups(world, zombie.x, zombie.y)
                    world.score_info.score += 1
                else:
                    destroyed_laser.append(laser)
    world.lasers = filter_from(world.lasers, destroyed_laser)
    world.zombies = filter_from(world.zombies, destroyed_zombie)


def filter_from(old_list: list[DesignerObject], elements_to_remove: list[DesignerObject]):
    """ Destroys elements from the old list and returns a new list

    Args:
        old_list (list[DesignerObject]): the full list of DesignerObject before filtering
        elements_to_remove(list[DesignerObject]: the elements to be destroyed
    """
    new_list = []
    for item in old_list:
        if item in elements_to_remove:
            destroy(item)
        else:
            new_list.append(item)
    return new_list


def create_power_ups(world: World, x_cord: int, y_cord: int) -> DesignerObject:
    """ Chance a dead zombie will drop a power up

    Args:
         world (World): the World dataclass
         x_cord (int): the x coordinate of where the zombie died
         y_cord (int): the y coordinate of where the zombie died
     Returns:
         DesignerObject: the power-up emoji
    """
    spawn_chance = randint(0, 10)
    if spawn_chance == 0:
        power_up = Emoji("🍎", x_cord, y_cord)
        world.power_ups.append(power_up)
        world.power_up_index.append(0)
    elif spawn_chance == 1:
        power_up = Emoji("🌟", x_cord, y_cord)
        world.power_ups.append(power_up)
        world.power_up_index.append(1)
        return power_up


def power_up_collision(world: World):
    """ Checks if scientist touches power-up and gives the scientist abilities

    Args:
        world (World): the World dataclass
    """
    destroyed_power_up = []
    for power_up in world.power_ups:
        for index in world.power_up_index:
            if index == 0:
                if colliding(world.scientist, power_up):
                    destroyed_power_up.append(power_up)
                    world.scientist_speed = 15
            elif index == 1:
                if colliding(world.scientist, power_up):
                    destroyed_power_up.append(power_up)
                    world.powered = True

    world.power_ups = filter_from(world.power_ups, destroyed_power_up)


def create_vaccine() -> DesignerObject:
    """ Create the vaccine

    Returns:
        DesignerObject: the vaccine image
    """
    vaccine = image("images/vaccine.png", 420, 300)
    return vaccine


def collide_vaccine_scientist(world: World):
    """ Prevents the scientist from walking over vaccine

    Args:
        world (World): the World dataclass
    """
    if colliding(world.scientist, world.vaccine):
        if world.last_keystroke.key_w:
            move_down(world)
        elif world.last_keystroke.key_s:
            move_up(world)
        elif world.last_keystroke.key_a:
            move_right(world)
        elif world.last_keystroke.key_d:
            move_left(world)


def zombie_collision(world: World) -> bool:
    """ Stops the game if a zombie collides with scientist or vaccine

    Args:
        world: the World dataclass
    Returns:
        bool: whether the zombie touched the entity or not
    """
    zombie_touches = False
    for zombie in world.zombies:
        if colliding(zombie, world.scientist) or colliding(zombie, world.vaccine):
            zombie_touches = True
            change_scene("game_over")
    return zombie_touches


def difficulty_increase(world: World):
    """ Increases current zombies' speed and health after 10 seconds

    Args:
        world (World): the World dataclass
    """
    for zombie in world.zombies:
        zombie.speed += 1
        zombie.health = 200


def time_remaining(world: World):
    """ Displays time left

    Args:
        world (World): the World dataclass
    """
    world.time_info.screen.text = "{sec}".format(sec=world.time_info.game_time)  # [2] text formatting


def update_score(world: World):
    """ Displays the score

    Args:
        world (World): the World dataclass
    """
    world.score_info.screen.text = "Score: {score}".format(score=str(world.score_info.score))


when("starting: world", create_world)
when("typing: world", press_key)
when("done typing: world", release_key)
when("updating: world", control_scientist)
when("typing: world", shoot_laser)
when("updating: world", move_laser)
when("updating: world", destroy_laser_x)
when("updating: world", destroy_laser_y)
when("updating: world", check_boundaries)
when("updating: world", spawn_zombies)
when("updating: world", collide_laser_zombie)
when("updating: world", collide_vaccine_scientist)
when("updating: world", find_closer_entity)
when("updating: world", move_zombie)
when("updating: world", power_up_collision)
when("updating: world", game_timer)
when("updating: world", time_remaining)
when("updating: world", update_score)
when(stop_game, pause)
when(zombie_collision, pause)
when("starting: game_over", create_game_over)
when("starting: you_win", create_you_win)
start()
