import random

from pygame import display, event, QUIT, quit, init

from app.cfg import *
from app.bacteria import Bacteria, Food
import sys

from pygame import event as pg_event

init()

# создание окна
game_window = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.set_caption(TITLE)

# генерация бактерий
bacteria_list = Bacteria.generate_bacteria(NUM_BACTERIA, SCREEN_WIDTH, SCREEN_HEIGHT)
food_list = []

# игровой цикл
while True:
    # обработка событий
    for event in pg_event.get():
        if event.type == QUIT:
            quit()
            sys.exit()

    # обновление экрана
    game_window.fill(WHITE)

    food_list = Food.generate_food_list(food_list, random.randint(2, 8))

    for food in food_list:
        food.draw(game_window)

    # отображение бактерий
    for bacteria in bacteria_list:
        bacteria.draw(game_window)
        dead = bacteria.move(bacteria_list, food_list)
        if dead:
            try:
                bacteria_list.remove(dead)
            except Exception:
                pass

    display.update()
    clock.tick(FPS)
