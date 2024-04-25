# Starter code for an adventure game.
# Inspired by David Johnson for CS 1400 University of Utah.
# Written by Jim de St. Germain

# Add your Header Doc String Here
#
#

import sys, pygame, math
from pygame import Vector2

# The following are constants for the bounds of the game, bounding frogger
HEIGHT = 480
WIDTH = 359
LEFT_EDGE = 20
RIGHT_EDGE = WIDTH - 20
BOTTOM_EDGE = HEIGHT - 50
TOP_EDGE = 60
CELL_WIDTH = 25


def bound( pos ):
    """
    make sure the vector is a location "on the screen"
    :param pos: Vector 2
    :return: None (modifies the pos vector)
    """
    if pos.x > RIGHT_EDGE:
        pos.x = RIGHT_EDGE
    if pos.x < LEFT_EDGE:
        pos.x = LEFT_EDGE
    if pos.y > BOTTOM_EDGE:
        pos.y = BOTTOM_EDGE
    if pos.y < TOP_EDGE:
        pos.y = TOP_EDGE


def pixel_collision( game_objects, item1, item2 ):
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
    pos1_temp = (pos1[0] - mask1.get_width() / 2, pos1[1] - mask1.get_height() / 2)
    pos2_temp = (pos2[0] - mask2.get_width() / 2, pos2[1] - mask2.get_height() / 2)

    offset = (pos2_temp[0] - pos1_temp[0], pos2_temp[1] - pos1_temp[1])

    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap( mask2, offset ) #, offset )
    return overlap != None


def draw_marker( screen, position ):
    """
    Simple helper to draw a location on the screen so you can
    see if your thoughts of what a position match Python's "thoughts".
    :param screen:  surface you are drawing on
    :param position: Vector2 : location to draw a circle
    :return: -NA-
    """
    pygame.draw.circle( screen, "black", position, 5 )


def move_frogger(frogger):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        frogger["pos"].x += -10
    if keys[pygame.K_RIGHT]:
        frogger["pos"].x += 10
    if keys[pygame.K_UP]:
        frogger["pos"].y += -10
    if keys[pygame.K_DOWN]:
        frogger["pos"].y += 10

    bound(frogger["pos"])


def draw_image_centered( screen, image, pos ):
    """
    On the screen, draw the given image **centered** on the given position.

    :param screen:  what we are drawing on
    :param image:   what we are drawing
    :param pos: Vector2 :  where to center the image
    :return: -NA-
    """
    containing_rectangle = image.get_rect()
    screen.blit( image, (pos.x - containing_rectangle.width/2, pos.y - containing_rectangle.height/2 ) )

def  add_game_object( game_objects, name, width, height, x, y ):
    """
    Create and add a new game object (based on the provided params) to the game_objects dictionary.

    :param game_objects: dictionary of all objects in the game
    :param name:    the name of the object AND the image file
    :param width:   how wide to make the object/image in the game
    :param height:  how tall to make the object/image in the game
    :param x:       where in the game the object is
    :param y:       where in the game the object is
    :return: -NA-  The game_objects dictionary will have the new object inserted based on the name
    """
    information = {}
    game_objects[name] = information   # put the new object in the dictionary

    # Read the image file name. Note: I have put all of my images in a subfolder named "images"
    image = pygame.image.load("images/"+name+".png") # .convert_alpha()

    information["name"] = name
    information["pos"] = Vector2(x, y)
    information["image"] = pygame.transform.smoothscale(image, (width, height))
    information["mask"] = pygame.mask.from_surface(information["image"])
    information["visible"] = True

    # Note: this code does not support animations.  If you want animations (and you should)
    #       you will need to update it based on the lab code!


def main():

    # Initialize pygame
    pygame.init()
    pygame.key.set_repeat(0,0)
    # Set up the Level by placing the objects of interest
    game_objects = {}

    #
    # Create the Game Objects and add them to the game_objects dictionary
    #
    # IMPORTANT: You must replace these images with your own.
    # IMPORTANT: the image file name is the name used for the item
    add_game_object( game_objects, "map1",     width=359, height=480, x=180, y=239)
    add_game_object(game_objects, "water", 359, 135, 180, 155)
    add_game_object( game_objects, "frogger",  30, 30, 180, 430)
    add_game_object( game_objects, "key",     20, 20, 150, 460 )
    add_game_object( game_objects, "car2", 30, 30, 90, 400)

    # create the window based on the map size
    screen = pygame.display.set_mode( game_objects["map1"]["image"].get_size() )


    # The frame count records how many times the program has
    # gone through the main loop.  Normally you don't need this information
    # but if you want to do an animation, you can use this variable to
    # indicate which sprite frame to draw
    frame_count = 0

    # Get a font to use to write on the screen.
    myfont = pygame.font.SysFont('monospace', 24)

    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # "start" the game when user hits space bar
    is_started = False

    # has the player found (moved on top of) the key to the door?
    frogger_pass = False

    # This is the main game loop. In it, we must:
    # - check for events
    # - update the scene
    # - draw the scene
    while True:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Position the player to the mouse location
        if is_alive:
            if is_started:
                player = game_objects["frogger"]
                move_frogger(player)

            else:
                # if space bar is clicked, start the game
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    is_started = True

        # Clear the map by putting a background gray across the screen
        screen.fill((150,150,150)) # This helps check if the image path is transparent

        # Check for game logic situation
        if not frogger_pass and game_objects["frogger"]["pos"].y <= (TOP_EDGE + 20):
            game_objects["key"]["visible"] = False
            frogger_pass = True

        # Draw the game objects
        for object in game_objects.values():
            if object["visible"]:
                draw_image_centered( screen, object["image"], object["pos"] )

            #See if we touch water
            if pixel_collision( game_objects, "frogger", "water" ):
                label = myfont.render( "Frogger fell in the Water!", True, (255, 255, 0) )
                screen.blit( label, (20, 40) )
                is_alive = False
                add_game_object( game_objects, "frogger",  30, 30, 180, 430)

        # If you need to debug where something is on the screen, you can draw it
        # using this helper method
        draw_marker( screen, Vector2(180,225) )

        # Write some text to the screen. You can do something like this to show some hints or whatever you want.
        # label = myfont.render("By Jim! - Put your Mouse on the Ship!", True, (255,255,0))
        # screen.blit(label, (20,20))

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.flip()

        # This slows down the code so it doesn't run more than 30 frames per second
        pygame.time.Clock().tick( 30 )

    pygame.quit()
    sys.exit()


# Start the program
main()