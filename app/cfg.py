from pygame import time


# title
TITLE = 'Simulator of Bacteria Evolution'

# FPS
clock = time.Clock()
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

# Bacteria properties
NUM_BACTERIA = 80
STARTING_HUNGER = 18

HUNGER_SPEED_FACTOR = .1
RADIUS_SPEED_FACTOR = 1
HUNGER_COLOR = WHITE

HUNGER_THRESHOLD = 15