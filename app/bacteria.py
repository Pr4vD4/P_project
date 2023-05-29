# bacteria.py

import random
from app.cfg import *
from pygame import draw
import math


class Bacteria:
    def __init__(self, x, y, radius, speed, color, hunger=None, predator=None):
        if predator:
            self.predator = predator
        else:
            self.predator = True if random.randint(0, 100) > 80 else False
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed

        self.color = RED if self.predator else color
        self.hunger_threshold = HUNGER_THRESHOLD * radius
        self.target = None
        if hunger:
            self.hunger = hunger
        else:
            self.hunger = self.hunger_threshold - int(self.hunger_threshold * .3)

    def move(self, bacteria_list, food_list):
        eaten = None
        distance = (self.speed * (RADIUS_SPEED_FACTOR / self.radius) + self.radius) / 5   # расстояние, на которое передвинется бактерия
        hunger_minus = (distance * HUNGER_SPEED_FACTOR) * .5  # уменьшаем голод на расстояние, на которое передвинется бактерия
        if self.predator:
            hunger_minus *= .9
        self.hunger -= hunger_minus


        if self.hunger <= 0:  # если голод закончился, удаляем бактерию
            return self
        else:
            if self.hunger <= self.hunger_threshold:
                self.check_collision(bacteria_list)
                self.find_food(food_list, bacteria_list)
            else:

                self.check_collision(bacteria_list)
                angle = random.uniform(0, 2 * math.pi)
                new_x = self.x + distance * math.cos(angle)
                new_y = self.y + distance * math.sin(angle)
                if new_x < 0:
                    new_x = SCREEN_WIDTH
                elif new_x > SCREEN_WIDTH:
                    new_x = 0
                if new_y < 0:
                    new_y = SCREEN_HEIGHT
                elif new_y > SCREEN_HEIGHT:
                    new_y = 0
                self.x = new_x
                self.y = new_y
        if self.target:
            eaten = self.eat_food(food_list, bacteria_list)
        self.divide(bacteria_list)
        if eaten:
            return eaten

    def find_food(self, food_list, bacteria_list):
        closest_food = None
        closest_distance = float('inf')

        if self.predator:
            for food in bacteria_list:
                if self.radius > food.radius:
                    distance = math.sqrt((self.x - food.x) ** 2 + (self.y - food.y) ** 2)
                else:
                    continue
                if distance < closest_distance and not food.predator:
                    self.target = food
                    closest_distance = distance
        else:
            for food in food_list:
                distance = math.sqrt((self.x - food.x) ** 2 + (self.y - food.y) ** 2)
                if distance < closest_distance:
                    self.target = food
                    closest_distance = distance

        if self.target is not None:
            try:
                # Рассчитываем вектор направления к ближайшей еде
                direction_x = self.target.x - self.x
                direction_y = self.target.y - self.y

                # Нормализуем вектор направления
                direction_length = math.sqrt(direction_x ** 2 + direction_y ** 2)
                direction_x /= direction_length
                direction_y /= direction_length

                # Двигаемся в направлении еды
                self.x += direction_x * self.speed * (RADIUS_SPEED_FACTOR / self.radius)
                self.y += direction_y * self.speed * (RADIUS_SPEED_FACTOR / self.radius)
            except Exception:
                pass

    def eat_food(self, food_list, bacteria_list):

        if self.predator:
            distance = math.sqrt((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2)
            if distance < self.radius + self.target.radius:
                self.hunger += self.target.radius * 1.5
                return self.target
        else:
            distance = math.sqrt((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2)
            if distance < self.radius + self.target.size:
                self.hunger += (self.target.size * 3)
                food_list.remove(self.target)

    def check_collision(self, bacteria_list):
        for other_bacteria in bacteria_list:
            if self != other_bacteria:
                distance = math.sqrt((self.x - other_bacteria.x) ** 2 + (self.y - other_bacteria.y) ** 2)

                if distance < self.radius + other_bacteria.radius:
                    dx = other_bacteria.x - self.x
                    dy = other_bacteria.y - self.y
                    magnitude = math.sqrt(dx ** 2 + dy ** 2)
                    if magnitude != 0:
                        dx /= magnitude
                        dy /= magnitude

                    push_distance = (self.radius + other_bacteria.radius - distance) * 0.5
                    push_x = dx * push_distance
                    push_y = dy * push_distance

                    self.x -= push_x
                    self.y -= push_y

                    other_bacteria.x += push_x
                    other_bacteria.y += push_y

    def divide(self, bacteria_list):
        if self.hunger >= self.hunger_threshold - int(self.hunger_threshold * .2):
            self.hunger //= 2
            bonus = random.randint(0, 3) if self.predator else 0
            d_raduis = random.randint(self.radius - 2, self.radius + 2 + bonus)
            if d_raduis < 3:
                d_raduis = 3
            elif d_raduis > 50:
                d_raduis = 50

            d_speed = random.randint(self.speed - 2, self.speed + 2)
            if d_speed <= 0:
                d_speed = 1
            elif d_speed > 80:
                d_speed = 80
            new_bacteria = Bacteria(self.x, self.y, d_raduis, d_speed, self.color, self.hunger, self.predator)
            bacteria_list.append(new_bacteria)

    def draw(self, surface):
        draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # рисуем круг, отображающий голод
        hunger_radius = self.radius * (1 - self.hunger / STARTING_HUNGER)
        draw.circle(surface, HUNGER_COLOR, (int(self.x), int(self.y)), int(hunger_radius))

    @staticmethod
    def generate_bacteria(num_bacteria, window_width, window_height):
        bacteria_list = []
        for i in range(num_bacteria):
            x = random.randint(0, window_width)
            y = random.randint(0, window_height)
            radius = random.randint(3, 10)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            speed = random.randint(8, 15)

            bacteria_list.append(Bacteria(x, y, radius, speed, color))
        return bacteria_list


class Food:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = GREEN

    def draw(self, surface):
        draw.circle(surface, self.color, (self.x, self.y), self.size)

    @staticmethod
    def generate_food_list(food_list, num_food):
        for _ in range(num_food):
            x, y = Food.generate_random_coordinates()
            size = random.randint(2, 4)
            food = Food(x, y, size)
            food_list.append(food)
        return food_list

    @staticmethod
    def generate_random_coordinates():
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        return x, y
