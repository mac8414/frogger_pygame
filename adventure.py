# Inspired by David Johnson for CS 1400 University of Utah.
"""
    File name: A10.py
    Author: McKay Hunter and Charbel Salloum
    Partner: None
    Date: December 7th, 2023
    Course: CS 1400
    Copyright: CS 1400 and McKay Hunter - This work may not
    be copied for the use in Academic Coursework.

I, McKay Hunter and I, Charbel Salloum, certify that we wrote this code from scratch and
did not copy it in part or whole from another source

File Contents/Program Purpose

    This program is a demonstration of using pygame to create the game frogger. This program uses dictionaries, tuples
    loops, and functions to accomplish the goals of this program.
"""

import sys, pygame, pygame.time
from pygame import Vector2
from random import *

# The following are constants for the bounds of the game, bounding frogger,
# and supporting creation of maps and the game window.
# The numbers are picked according to all the 650 x 800 map images that we have
HEIGHT = 800
WIDTH = 650
LEFT_EDGE = 24
RIGHT_EDGE = WIDTH - 24
BOTTOM_EDGE = HEIGHT - 100
TOP_EDGE = 100


def bound(pos):
    """
    Given the position of the frogger, this function is used to use the pre-established constants
    and bound the frogger to a particular rectangular window.

    :param pos : position of the frogger
    :return: none
    """
    if pos.x > RIGHT_EDGE:  # Checks if the position of frogger is at the right edge of the screen
        pos.x = RIGHT_EDGE  # Sets the position of frogger to be the same as the edge when it hits the edge
    if pos.x < LEFT_EDGE:  # Checks if the position of frogger is at the left edge of the screen
        pos.x = LEFT_EDGE  # Sets the position of frogger to be the same as the edge when it hits the edge
    if pos.y > BOTTOM_EDGE:  # Checks if the position of frogger is at the bottom edge of the screen
        pos.y = BOTTOM_EDGE  # Sets the position of frogger to be the same as the edge when it hits the edge
    if pos.y < TOP_EDGE:  # Checks if the position of frogger is at the top edge of the screen
        pos.y = TOP_EDGE  # Sets the position of frogger to be the same as the edge when it hits the edge


def pixel_collision(game_objects, item1, item2):
    """
    Given two game objects (by name), check if the non-transparent pixels of
    one mask contacts the non-transparent pixels of the other.

    :param game_objects: the dictionary of all items in the game
    :param item1 (string): the name of the first game object that is being compared to the second
    :param item2 (string): the name of the second game object
    :return: (boolean) True if they overlap
    """
    pos1 = game_objects[item1]["pos"]
    pos2 = game_objects[item2]["pos"]
    mask1 = game_objects[item1]["mask"]
    mask2 = game_objects[item2]["mask"]

    # shift images back to 0,0 for collision detection
    width1, height1 = mask1.get_size()
    width2, height2 = mask2.get_size()

    pos1_temp = (pos1.x - width1 / 2, pos1.y - height1 / 2)
    pos2_temp = (pos2.x - width2 / 2, pos2.y - height2 / 2)

    offset = (pos2_temp[0] - pos1_temp[0], pos2_temp[1] - pos1_temp[1])

    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, offset)  # , offset )

    return overlap is not None


def make_map(game_objects, name, x, y):
    """
        Create and add a map object (based on the provided params) to the game_objects dictionary.

        :param game_objects: dictionary of all objects in the game
        :param name:    the name of the object AND the image file
        :param x:       where in the game the object is
        :param y:       where in the game the object is
        :return: -NA-  The game_objects dictionary will have the new object inserted based on the name
        """
    map_info = {}  # Starts by making the map info an empty dictionary
    game_objects[name] = map_info  # put the new object in the dictionary

    # Read the image file name. Note: I have put all of my images in a subfolder named "images"
    image = pygame.image.load("images/" + name + ".png")  # .convert_alpha()

    map_info["name"] = name
    map_info["pos"] = Vector2(x, y)
    map_info["image"] = image
    map_info["mask"] = pygame.mask.from_surface(map_info["image"])
    map_info["visible"] = True


def draw_marker(screen, position):
    """
    Simple helper to draw a location on the screen, so you can
    see if your thoughts of what a position match Python's "thoughts".

    :param screen:  surface you are drawing on
    :param position: Vector2 : location to draw a circle
    :return: -NA-
    """
    pygame.draw.circle(screen, "white", position, 5)


def draw_image_centered(screen, image, pos):
    """
    On the screen, draw the given image **centered** on the given position.

    :param screen:  what we are drawing on
    :param image:   what we are drawing
    :param pos: Vector2 :  where to center the image
    :return: -NA-
    """
    containing_rectangle = image.get_rect()
    screen.blit(image, (pos.x - containing_rectangle.width / 2, pos.y - containing_rectangle.height / 2))


def create_frogger():
    """
    For this function it starts by creating an empty dictionary and adds
    the necessary attributes to the frogger object.

    :return: frogger_info (dictionary) of frogger object information
    """
    frogger_info = {}

    # Read the image file name. Note: I have put all of my images in a subfolder named "images"
    frogger_image = pygame.image.load("images/frogger.png")  # .convert_alpha()

    frogger_info["name"] = "frogger"
    frogger_info["pos"] = Vector2(WIDTH // 2, BOTTOM_EDGE)
    frogger_info["images"] = pygame.transform.smoothscale(frogger_image, Vector2(30, 30))
    frogger_info["mask"] = pygame.mask.from_surface(frogger_info["images"])
    frogger_info["visible"] = True

    return frogger_info


def move_frogger(event, frogger):
    """
    This function takes in two parameters. One being the event of when a key is pressed
    and two the frogger object. When the keys are pressed the position for the frogger changes.
    This function uses all 4 images of Frogger to change through the frogger direction according to movement.
    This function also sets up the bound for frogger movements.

    :param event: The event of when the keys pressed
    :param frogger: The frogger tuple
    :return: N/A
    """
    # If a key is pressed
    if event.type == pygame.KEYDOWN:
        # If left key is pressed, used left facing image of frogger and move 50 pixels to the left.
        if event.key == pygame.K_LEFT:
            frogger_image = pygame.image.load("images/froggerL.png")  # A different image loads after the left key is pressed
            frogger["pos"] += Vector2(-50, 0)
            frogger["images"] = pygame.transform.smoothscale(frogger_image, Vector2(30, 30))
        # If right key is pressed, use right facing image of frogger and move 50 pixels to the right.
        elif event.key == pygame.K_RIGHT:
            frogger_image = pygame.image.load("images/froggerR.png")  # A different image loads after the right key is pressed
            frogger["pos"] += Vector2(50, 0)
            frogger["images"] = pygame.transform.smoothscale(frogger_image, Vector2(30, 30))
        # If up key is pressed, use up facing image of frogger and move 50 pixels up.
        elif event.key == pygame.K_UP:
            frogger_image = pygame.image.load("images/frogger.png")  # A different image loads after the up key is pressed
            frogger["pos"] += Vector2(0, -50)
            frogger["images"] = pygame.transform.smoothscale(frogger_image, Vector2(30, 30))
        # If down key is pressed, use down facing image of frogger and move 50 pixels down.
        elif event.key == pygame.K_DOWN:
            frogger_image = pygame.image.load("images/froggerD.png")  # A different image loads after the down key is pressed
            frogger["pos"] += Vector2(0, 50)
            frogger["images"] = pygame.transform.smoothscale(frogger_image, Vector2(30, 30))

        # delay to get frogger to hop instead of run
        pygame.time.delay(100)

    bound(frogger["pos"])  # Calls bound function to bound the position of frogger to part of the screen


def draw_frogger(frogger, screen):
    """
    This function draws the frogger.

    :param frogger: The frogger dictionary
    :param screen: The game screen
    :return: N/A
    """
    if frogger["visible"]:  # Checks if the frogger is visible on the screen
        draw_image_centered(screen, frogger["images"], frogger["pos"])  # Draws the frogger in the center position


def make_cars(name, car_num, x, y, direction):
    """
    This funtion creates a dictionary with the values of the cars object.
    We don't care about width and height parameters because all car images are resized to 50 x 50 images.
    The cars are numbered by a number for the row first, followed by an underscore and column number,
    from left to right. Rows also work from top to bottom.

    The function takes in the name with the row and column but adjusts it to read the file image of only the "car"
    followed by row number.


    :param name: car1_1, car2_3, etc. These names include the row number and column
    :param car_num: The number of the car in a rows. In other words, the column its in
    :param x: Uses as the x position
    :param y: Uses as the y position
    :return: Returns the new dictionary
    """
    cars_info = {}  # Starts with an empty dictionary
    part_to_ommit = "_" + str(car_num)  # Removes the number at the end of the file string
    image_name = name.replace(part_to_ommit, '')  # Replaces it with the new number
    image = pygame.image.load("images/" + image_name + ".png")  # Converts the parts into a new string

    cars_info["name"] = name  # Enters the dictionary as the name of the car
    cars_info["pos"] = Vector2(x, y)  # Enters the dictionary as the new postion
    cars_info["image"] = image  # Enters the dictionary as the image name
    cars_info["mask"] = pygame.mask.from_surface(cars_info["image"])  # Enters the dictionary as a mask
    cars_info["visible"] = True  # Sets the car as being visible
    cars_info["direction"] = direction

    return cars_info  # Returns the new dictionary


def make_cars_dict():
    """
    This function creates a dictionary with the values of the cars. The dictionary is meant to position the cars
    correctly in 10 rows, skipping row 6 (because it's grass for the frog), and 3 cars in each row.
    The cars are also made to spawn in a random position in the x-axis.
    The cars also have a direction variable which is later used in move_cars() (with -1 or 1 values)
    to make some cars go right and others move left.

    :return: Returns the new dictionary
    """
    # Create and empty dictionary
    cars_dict = {}
    car_row = 1
    car_y_pos = 150
    right_direction = True  # Initial direction for the first row
    # Nested loop to loop through every row, and then every column for every row.
    for vertical_car_count in range(11):
        car_num = 1
        random_pos_num = randint(LEFT_EDGE, RIGHT_EDGE) # Set spawn position of car 1 in the designated row
        car_x_pos = random_pos_num
        random_pos_num += 150
        # Set the direction based on the current row
        if right_direction == True:
            direction = 1
        else:
            direction = -1

        # Loop through each car in a row
        for horizontal_car_count in range(3):
            # Make sure to skip row 6, row where there is grass and safe zone for car
            if car_row == 6:
                pass
            else:
                # Get the name of the car image by adding the row, underscore, and column
                car_name = "car" + str(car_row) + "_" + str(car_num)
                cars_dict[car_name] = make_cars(car_name, car_num, car_x_pos, car_y_pos, direction)
                # Move to next car in a row
                car_num += 1
                # Spawn the next car 150 pixels away from first
                car_x_pos += 150

        # Move through each row and switch directions each time
        car_row += 1
        car_y_pos += 50
        right_direction = not right_direction  # Toggle direction for the next row

    return cars_dict


def draw_car(car, screen):
    """
    This function draws the cars on the screen on their locations.

    :param car: Takes in the car dictionary
    :param screen: Takes in the screen
    :return: N/A
    """

    if car["visible"] == True:
        draw_image_centered(screen, car["image"], car["pos"])  # Uses draw centered image function to create the cars


def move_cars(car, speed):
    """
    This function takes in each car object and its speed (how far it moves each frame)
    and correspondingly moves the car in the correct direction.
    Also, this makes sure that if a car goes beyond the screen edge, it spawns back on the opposite edge.

    :param car: car object in card_dict
    :param speed: an integer corresponding to the movement amount of the car
    :return: None (The cars begin to move when called)
    """
    # Take in the car position and seperate the x and y conponents
    position = car["pos"]
    x, y = position.x, position.y

    # Check if cars go beyond edges and respawn the car on the opposite side
    if x < LEFT_EDGE:
        x = RIGHT_EDGE
    elif x > RIGHT_EDGE:
        x = LEFT_EDGE
    # Move the car by adding to the x component
    else:
        x += int(speed) * car["direction"]  # Adjust the speed based on the car's direction

    # Update car position
    car["pos"] = Vector2(x, y)


def make_logs(name, x, y, direction):
    """
    This function creates all the log information to later store.
    
    :param name: The log name (string)
    :param x: x_component of the spawn position
    :param y: y_component of the spawn position
    :param direction: Direction the logs are moving in (int: takes in 1 or -1)
    :return: None, just creates a dictionary of information for each log
    """
    logs_info = {}
    image = pygame.image.load("images/" + name + ".png")  # .convert_alpha()

    logs_info["name"] = name
    logs_info["pos"] = Vector2(x, y)
    logs_info["image"] = image
    logs_info["mask"] = pygame.mask.from_surface(logs_info["image"])
    logs_info["visible"] = True
    logs_info["direction"] = direction

    return logs_info


def make_logs_dict():
    """
    No parameters for this function. This function is meant to craete a dictionary of all logs, 
    storing logs_info for each log all in one dictionary. 
    
    :return: Returns a new dictionary of logs and all their info
    """
    # Create a new dict
    logs_dict = {}
    logs_row = 1
    log_y_pos = 150 # Initial row position
    right_direction = True  # Initial direction for the first row
    # Nested loop to loop through every row, and then every column for every row.
    for vertical_log_count in range(5):
        log_num = 1
        random_num_pos = randint(LEFT_EDGE, RIGHT_EDGE)
        log_x_pos = random_num_pos

        # Set the direction based on the current row
        if right_direction == True:
            direction = 1
        else:
            direction = -1

        # Loop through each log in a row
        for horizontal_log_count in range(2):
            # Get log image name by adding row, underscore, and column
            log_name = "log" + str(logs_row) + "_" + str(log_num)
            # Make log and its information and store in the logs dictionary
            logs_dict[log_name] = make_logs(log_name, log_x_pos, log_y_pos, direction)
            log_num += 1
            log_x_pos += 300

        # Cycle through every row
        logs_row += 1
        log_y_pos += 50
        right_direction = not right_direction  # Toggle direction for the next row

    return logs_dict


def draw_log(log, screen):
    """
    This function takes in the log dictionary and the screen, and then draws all log objects with their
    corresponding positions.

    :param log: log dictionary
    :param screen: the screen
    :return: N/A
    """
    if log["visible"] == True:  # Sets the log to be visible
        # Uses the draw image centered to draw the logs in their positions#
        draw_image_centered(screen, log["image"], log["pos"])


def move_logs(log, speed):
    """
    This function takes in the log object from the dictionary and the speed (how much the log moves)
    and then moves each log in the correct direction and speed according to the row.
    This also includes bounds for the log movements.

    :param log: Take in log object from logs_dict dictionary
    :param speed: The amount the log moves for each frame (int)
    :return:
    """
    # Get x and y component of each log position
    position = log["pos"]
    x, y= position.x, position.y

    # If a log reaches either right or left bound, spawn it at the opposite side
    if x < LEFT_EDGE:
        x = RIGHT_EDGE
    elif x > RIGHT_EDGE:
        x = LEFT_EDGE
    else:
        # Move the log in the correct direction
        x += int(speed) * log["direction"]  # Adjust the speed based on the car's direction

    return Vector2(x, y)


def main():
    # Setup pygame
    pygame.init()

    # Start at level 1
    level = 1

    # Set up the Level by placing the objects of interest
    game_objects = {}

    # Create the Game Objects and adds them to the game_objects dictionary
    # Make sure to make objects in general order from back of screen to front
    game_objects["frogger"] = create_frogger()
    make_map(game_objects, "background", x=325, y=400)
    make_map(game_objects, "map1", x=325, y=400)
    make_map(game_objects, "map1_rock_obstacles", x=325, y=400)
    make_map(game_objects, "map2", x=325, y=400)
    make_map(game_objects, "map3", x=325, y=400)
    make_map(game_objects,"lava", x=325, y=400)
    make_map(game_objects, "map4", x=325, y=400)
    make_map(game_objects, "acid", x=325, y=400)

    # make cars_dict and add car objects, then update the game_objects dictionary
    cars_dict = make_cars_dict()
    game_objects.update(cars_dict)

    # Add log objects, and update the game_objects dictionary with the log dictionary
    logs_dict = make_logs_dict()
    game_objects.update(logs_dict)

    # Make the name of the level flexible so that it updates with the level too
    map_name_with_level = "map" + str(level)
    # Define the screen according to the map and its level
    screen = pygame.display.set_mode(game_objects[map_name_with_level]["image"].get_size())

    # The frame count records how many times the program has
    # gone through the main loop. You can use this variable to
    # indicate which sprite frame to draw
    frame_count = 0

    # Get a font to use to write on the screen. This font is for Welcome and Levels
    myfont = pygame.font.SysFont('wide latin', 50)
    # This font is smaller for instructions
    smaller_font = pygame.font.SysFont('ahoroni', 35)

    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # "start" the game when user hits space bar
    is_started = False

    music_file_path = r"music3.mp3"
    pygame.mixer.music.load(music_file_path)
    pygame.mixer.music.set_volume(.1)
    # # Set the speed to slow down the music (0.5 means half speed)
    #
    # # Play the music
    pygame.mixer.music.play(-1)

    # Variable to establish if the player has one the game. Used to add ending screen.
    win_game = False

    #   For each level:
    # 1- Add objects
    # 2- Update Objects
    # 3- Draw objects
    while True:

        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                is_alive = False

        # Clear the map by putting a background that introduces levels across the screen
        # The background is used to add messages and level introductions for the user.
        screen.blit(game_objects["background"]["image"], (0, 0))

        if is_alive:
            if is_started:
                # Establish the object frogger and its position, also adding its moving function
                player = game_objects["frogger"]
                temp_position = player["pos"].xy
                move_frogger(event, player)
                # Draw the map corresponding to the level
                draw_image_centered(screen, game_objects[map_name_with_level]["image"],
                                    game_objects[map_name_with_level]["pos"])
                if level == 1:
                    # Check object collision with the rock maze
                    # If the frogger collides with the rock, it stays in it's position and can only move
                    # in direction without rocks
                    if pixel_collision(game_objects, "frogger", "map1_rock_obstacles"):
                        player["pos"] = temp_position

                    # Draw the rocks map obstacle
                    draw_image_centered(screen, game_objects["map1_rock_obstacles"]["image"],
                                        game_objects["map1_rock_obstacles"]["pos"])

                    # Add Hint and level interaction prints to the screen
                    level_interaction = smaller_font.render("Level 1 - Try to reach the other side!", True,
                                                            (250, 250, 250))
                    screen.blit(level_interaction, (20, 30))
                    level_hint = smaller_font.render("Hint: There is only one correct path!", True,
                                                            (250, 250, 250))
                    screen.blit(level_hint, (110, 750))

                if level == 2:
                    # loop through every car in the car_dict
                    # get each car moving at a certain speed, and then draw the cars
                    for car in cars_dict:
                        # speed = randint(1, 25)
                        speed = 7
                        move_cars(cars_dict[car], speed)
                        draw_car(cars_dict[car], screen)

                        # If the frogger collides with a car, the frogger is no longer alive (! is_alive)
                        if pixel_collision(game_objects, "frogger", car):
                            is_alive = False

                    # Add level interaction print to the top of the screen
                    level_interaction = smaller_font.render("Level 2 - Don't hit the cars or you lose!", True,
                                                            (250, 250, 250))
                    screen.blit(level_interaction, (20, 30))

                if level == 3:
                    # Add level interaction print to the top of the screen
                    level_interaction = smaller_font.render(
                        "Level 3 - Careful...don't hit the lava now!", True,
                        (250, 250, 250))
                    screen.blit(level_interaction, (20, 30))
                    # Draws the lava object on the screen
                    draw_image_centered(screen, game_objects["lava"]["image"],
                                        game_objects["lava"]["pos"])
                    # Starts with on_log as false before the loop that sets up the logs
                    on_log = False
                    for log in logs_dict:  # Loops through each log image and draws it on the screen
                        position = game_objects["frogger"]["pos"]
                        speed = 7
                        logs_dict[log]["pos"] = move_logs(logs_dict[log], speed)
                        draw_log(logs_dict[log], screen)

                        if on_log:  # Base case that if the frog is on the log then it does not die
                            continue
                        # # Check if frogger is on a log
                        if pixel_collision(game_objects, "frogger", log):
                            position.x += speed * logs_dict[log]["direction"]  # Changes the direction of the frog
                            on_log = True
                            is_alive = True
                        elif pixel_collision(game_objects, "frogger", "lava") and not on_log:  # Frog dies on the lava
                            is_alive = False

                    # Drawing in the bottom half of cars, from car7 to car 11 (7th to 11th row)
                    bottom_half_cars_keys = list(cars_dict.keys())[15:]
                    bottom_half_cars_dict = {key: cars_dict[key] for key in bottom_half_cars_keys}

                    for car in bottom_half_cars_dict:
                        speed = 7
                        move_cars(bottom_half_cars_dict[car], speed)
                        draw_car(bottom_half_cars_dict[car], screen)

                        # If the frogger collides with a car, the frogger is no longer alive (! is_alive)
                        if pixel_collision(game_objects, "frogger", car):
                            is_alive = False

                    # Check for collisions with logs and lava

                if level == 4:
                    # Add level interaction print to the top of the screen
                    level_interaction = smaller_font.render("Level 4 - Oh no! Everything just got much faster!", True,
                                                            (250, 250, 250))
                    screen.blit(level_interaction, (10, 42))
                    # Draws the acid object on the screen
                    draw_image_centered(screen, game_objects["acid"]["image"],
                                        game_objects["acid"]["pos"])
                    # Starts with on_log as false before the loop that sets up the logs
                    on_log = False
                    for log in logs_dict:  # Loops through each log image and draws it on the screen
                        position = game_objects["frogger"]["pos"]
                        speed = 12
                        logs_dict[log]["pos"] = move_logs(logs_dict[log], speed)
                        draw_log(logs_dict[log], screen)

                        if on_log:  # Base case that if the frog is on the log then it does not die
                            continue
                        # # Check if frogger is on a log
                        if pixel_collision(game_objects, "frogger", log):
                            position.x += speed * logs_dict[log]["direction"]  # Changes the direction of the frog
                            on_log = True
                            is_alive = True
                        elif pixel_collision(game_objects, "frogger", "acid") and not on_log:  # Frog dies on the lava
                            is_alive = False

                    # Drawing in the bottom half of cars, from car7 to car 11 (7th to 11th row)
                    bottom_half_cars_keys = list(cars_dict.keys())[15:]
                    bottom_half_cars_dict = {key: cars_dict[key] for key in bottom_half_cars_keys}
                    for car in bottom_half_cars_dict:
                        speed = 11
                        move_cars(bottom_half_cars_dict[car], speed)
                        draw_car(bottom_half_cars_dict[car], screen)

                        # If the frogger collides with a car, the frogger is no longer alive (! is_alive)
                        if pixel_collision(game_objects, "frogger", car):
                            is_alive = False

                    if pixel_collision(game_objects, "frogger", car):
                        is_alive = False

                # For every level, after all level specification, draw the frogger.
                # This allows the frogger to be on top of everything.
                draw_frogger(player, screen)

            else:  # run this if game is not started (! is_started)
                # According to the level, display certain messages
                if level == 1:
                    # Add text that introduces game title and level 1
                    # Prompt user to hit the space bar to start first level
                    welcome = myfont.render("Frorge?!", True, (0, 0, 0))
                    screen.blit(welcome, (120, 130))
                    level_name_output = myfont.render("Level 1", True, (0, 0, 0))
                    screen.blit(level_name_output, (170, 340))
                    instructions = smaller_font.render("Press the space-bar to Start the Level!", True, (0, 0, 0))
                    screen.blit(instructions, (100, 600))
                if level == 2:
                    # Add text to introduce level 2
                    # Prompt user to hit space bar to start level 2
                    level_name_output = myfont.render("Level 2", True, (0, 0, 0))
                    screen.blit(level_name_output, (170, 340))
                    instructions = smaller_font.render("Press the space-bar to Start the Level!", True, (0, 0, 0))
                    screen.blit(instructions, (100, 600))
                if level == 3:
                    # Add text to introduce level 3
                    # Prompt user to hit space bar to start level 3
                    level_name_output = myfont.render("Level 3", True, (0, 0, 0))
                    screen.blit(level_name_output, (170, 340))
                    instructions = smaller_font.render("Press the space-bar to Start the Level!", True, (0, 0, 0))
                    screen.blit(instructions, (100, 600))
                if level == 4:
                    # Add text to introduce level 4
                    # Prompt user to hit space bar to start level 4
                    level_name_output = myfont.render("Level 4", True, (0, 0, 0))
                    screen.blit(level_name_output, (170, 340))
                    instructions = smaller_font.render("Press the space-bar to Start the Level!", True, (0, 0, 0))
                    screen.blit(instructions, (100, 600))
                if level == 5:
                    # There is no level 5
                    # Level 5 only stands for the 5th screen which represents the ending and the player winning.
                    # Player is no longer alive and the game is won.
                    is_alive = False
                    win_game = True

                # Within each "waiting" screen, if space bar is hit, start game
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    is_started = True

            # Check if frogger reaches the end goal grass.
            # If so, add "waiting" screen to introduce no level
            if game_objects["frogger"]["pos"].y == TOP_EDGE:
                # Loop back into is_started possibilities
                is_started = False

                game_objects[map_name_with_level]["visible"] = False
                # Only run up to level 5, levels being the number of level introductions screens + Final screen
                if level < 5:
                    level += 1
                # Update map_name_with_level when the level changes
                map_name_with_level = "map" + str(level)
                game_objects["frogger"]["pos"] = Vector2(WIDTH // 2, BOTTOM_EDGE)

        # This runs when the player wins, beating level 4
        # Screen blits that basically say congrats for winning.
        elif win_game == True and is_alive == False:
            level_name_output = myfont.render("YAYY!", True, (0, 0, 0))
            screen.blit(level_name_output, (170, 340))
            instructions = smaller_font.render("You won! You really did beat frogger?!", True, (0, 0, 0))
            screen.blit(instructions, (100, 600))
            music_file_path2 = r"mario.mp3"
            pygame.mixer.music.load(music_file_path2)
            pygame.mixer.music.set_volume(.1)
            # # Set the speed to slow down the music (0.5 means half speed)
            #
            # # Play the music
            pygame.mixer.music.play(1)
        # This runs when frogger is no longer alive, without winning
        # Screen blits and prints that tell the user game over.
        else:
            game_message = myfont.render("Game", True, (0, 0, 0))
            screen.blit(game_message, (210 , 320))
            over_message = myfont.render("Over!", True, (0, 0, 0))
            screen.blit(over_message, (220, 380))
            game_over_message = smaller_font.render("Press the space-bar to Restart Game", True, (0, 0, 0))
            screen.blit(game_over_message, (100, 600))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                level = 1
                is_started = False
                is_alive = True

                game_objects["frogger"]["pos"] = Vector2(WIDTH // 2, BOTTOM_EDGE)

        # If you need to debug where something is on the screen, you can draw it
        # using this helper method
        # draw_marker(screen, Vector2(312, 720))

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.flip()

        # This slows down the code, so it doesn't run more than 30 frames per second
        pygame.time.Clock().tick(30)

    pygame.quit()
    sys.exit()

main()

