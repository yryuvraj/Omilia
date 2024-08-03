import pygame
import sys
from language_menu import language_call
from help_menu import help_call
import asyncio

# Initialize pygame
pygame.init()

# Declare global variables
global screen, screen_width, screen_height, bg_img, start_button_img, help_button_img
global start_button_rect, help_button_rect

# Set up the screen
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Omilia")

# Load images
bg_img = pygame.image.load("menuAssets/oi.png")
start_button_img = pygame.image.load("menuAssets/start1.png")
help_button_img = pygame.image.load("menuAssets/help1.png")
pygame.mixer.music.load("menuAssets/menubg.ogg")
pygame.mixer.music.play(-1)

# Create Rect objects for the buttons
start_button_rect = pygame.Rect(380, 430, start_button_img.get_width(), start_button_img.get_height())
help_button_rect = pygame.Rect(380, 550, help_button_img.get_width(), help_button_img.get_height())


# Main loop
async def main():
    global screen, screen_width, screen_height, bg_img, start_button_img, help_button_img
    global start_button_rect, help_button_rect

    while True:
        # Draw the background and buttons
        screen.blit(bg_img, (0, 0))
        screen.blit(start_button_img, start_button_rect)
        screen.blit(help_button_img, help_button_rect)

        # Get the list of events
        event_list = pygame.event.get()

        # Process events
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if start_button_rect.collidepoint(event.pos):
                        language_call()
                    elif help_button_rect.collidepoint(event.pos):
                        help_call()

        # Update the screen
        pygame.display.update()
        await asyncio.sleep(0)  # Allow other tasks to run


# Run the main function
asyncio.run(main())
