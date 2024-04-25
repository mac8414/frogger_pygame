# Sample Solution Code by David Johnson and Jim de St. Germain
# Updated Fall 2023

import pygame, sys, math
from pygame import Vector2

def main():

    # Setup pygame
    pygame.init()

    # Define the screen
    screen_size = width, height = 600, 400
    screen = pygame.display.set_mode(screen_size)

    # A list (really a dictionary) or objects that are part of the game
    game_objects = {}

    # Set up one of the game objects using a dictionary, in this case the alien's flying saucer
    alien_info = {
        "name": "alien1",
        "images": [],
        "mask": None,
        "pos": Vector2( width//2, height//2 )
    }

    alien_info["images"].append(pygame.image.load("alien1.png").convert_alpha())
    alien_info["images"].append(pygame.image.load("alien2.png").convert_alpha())
    alien_info["images"].append(pygame.image.load("alien3.png").convert_alpha())

    # Save the alien information inside the dictionary of all game objects
    game_objects["alien1"] = alien_info

    frame_number = 0
    alien_frame = 0

    ################################################################
    # Main part of the game

    is_playing = True

    while is_playing:

        # Check for events
        for event in pygame.event.get():
            # Stop loop if click on window close button
            if event.type == pygame.QUIT:
                is_playing = False

            # Check for a key press, and if they match the left and right arrow, move the alien ship
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT:
            #         game_objects["alien1"]["pos"] += Vector2(-5, 0)
            #     if event.key == pygame.K_RIGHT:
            #         game_objects["alien1"]["pos"] += Vector2(5, 0)
            #     if event.key == pygame.K_UP:
            #         game_objects["alien1"]["pos"] += Vector2(0, -5)
            #     if event.key == pygame.K_DOWN:
            #         game_objects["alien1"]["pos"] += Vector2(0, 5)

        # Set the alien to the mouse location
        # pos = Vector2(pygame.mouse.get_pos())
        # game_objects["alien1"]["pos"] = pos

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game_objects["alien1"]["pos"] += Vector2(-5, 0)
        if keys[pygame.K_RIGHT]:
            game_objects["alien1"]["pos"] += Vector2(5, 0)
        if keys[pygame.K_UP]:
            game_objects["alien1"]["pos"] += Vector2(0, -5)
        if keys[pygame.K_DOWN]:
            game_objects["alien1"]["pos"] += Vector2(0, 5)

        # Erase the screen with a background color
        screen.fill((0, 100, 50))  # fill the window with a color

        # Draw the alien (Choose the one that is most readable to you)
        screen.blit(game_objects["alien1"]["images"][alien_frame], game_objects["alien1"]["pos"] )

        # Bring all the changes to the screen into view
        pygame.display.flip()

        # Pause for a few milliseconds
        pygame.time.Clock().tick(30)

        frame_number += 1
        alien_frame = (frame_number // 10) % 3

    # Once the game loop is done, close the window and quit.
    pygame.quit()
    sys.exit()

if __name__=="__main__":
    main()