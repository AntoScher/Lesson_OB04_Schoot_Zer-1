import pygame
import random
import sys
from abc import ABC, abstractmethod

# Инициализация Pygame
pygame.init()

# Задаем размеры окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Бой - Герой против Монстра")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Абстрактный класс для оружия
class Weapon(ABC):
    @abstractmethod
    def attack(self):
        pass

# Класс для меча
class Sword(Weapon):
    def attack(self):
        return random.randint(10, 20)

# Класс для топора
class Axe(Weapon):
    def attack(self):
        return random.randint(15, 25)

# Фабрика для создания оружия
class WeaponFactory:
    @staticmethod
    def create_weapon(weapon_type):
        if weapon_type == '1':
            return Sword()
        elif weapon_type == '2':
            return Axe()
        else:
            raise ValueError("Неверный выбор оружия")

# Класс для управления движением
class Movement:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = max(0, min(SCREEN_WIDTH - 50, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - 50, self.y))
    
    def draw(self, color):
        pygame.draw.rect(screen, color, (self.x, self.y, 50, 50))

# Класс для бойца
class Fighter:
    def __init__(self, movement):
        self.movement = movement
        self.weapon = None
    
    def change_weapon(self, weapon):
        self.weapon = weapon
    
    def attack(self):
        if self.weapon:
            return self.weapon.attack()
        return 0

# Класс для монстра
class Monster:
    def __init__(self, x, y):
        self.movement = Movement(x, y)
        self.health = 100
    
    def move(self):
        self.movement.move(random.randint(-10, 10), random.randint(-10, 10))
    
    def take_damage(self, amount):
        self.health -= amount
        print(f"Здоровье монстра: {self.health}")
        if self.health <= 0:
            print("Монстр повержен!")
            pygame.quit()
            sys.exit()

# Основная функция игры
def main():
    clock = pygame.time.Clock()
    hero_movement = Movement(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
    hero = Fighter(hero_movement)
    monster = Monster(random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50))

    weapon_choice = input("Выберите оружие: 1 - Меч, 2 - Топор\n")
    try:
        hero.change_weapon(WeaponFactory.create_weapon(weapon_choice))
    except ValueError as e:
        print(e)
        sys.exit()

    start_game = input("Начинаем? (y/n)\n")
    if start_game.lower() != 'y':
        sys.exit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            hero.movement.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            hero.movement.move(5, 0)
        if keys[pygame.K_UP]:
            hero.movement.move(0, -5)
        if keys[pygame.K_DOWN]:
            hero.movement.move(0, 5)
        if keys[pygame.K_RETURN]:
            if pygame.Rect(hero.movement.x, hero.movement.y, 50, 50).colliderect(pygame.Rect(monster.movement.x, monster.movement.y, 50, 50)):
                damage = hero.attack()
                print(f"Герой атакует монстра и наносит {damage} урона!")
                monster.take_damage(damage)

        monster.move()
        
        screen.fill(WHITE)
        hero.movement.draw(BLACK)
        monster.movement.draw(RED)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
