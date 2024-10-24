import pygame
import random
import sys

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


# Класс для бойца
class Fighter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.weapon = None

    def change_weapon(self, weapon):
        self.weapon = weapon

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, 50, 50))

    def attack(self):
        if self.weapon:
            return self.weapon.attack()
        return 0


# Абстрактный класс для оружия
class Weapon:
    def attack(self):
        raise NotImplementedError("Метод attack() должен быть определен в подклассах")


# Класс для меча
class Sword(Weapon):
    def attack(self):
        return random.randint(10, 20)


# Класс для топора
class Axe(Weapon):
    def attack(self):
        return random.randint(15, 25)


# Класс для монстра
class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, 50, 50))

    def move(self):
        self.x += random.randint(-10, 10)
        self.y += random.randint(-10, 10)
        self.x = max(0, min(SCREEN_WIDTH - 50, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - 50, self.y))


# Основная функция игры
def main():
    clock = pygame.time.Clock()
    hero = Fighter(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
    monster = Monster(random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50))

    weapon_choice = input("Выберите оружие: 1 - Меч, 2 - Топор\n")
    if weapon_choice == '1':
        hero.change_weapon(Sword())
    elif weapon_choice == '2':
        hero.change_weapon(Axe())
    else:
        print("Неверный выбор")
        sys.exit()

    start_game = input("Начинаем? (y/n)\n")
    if start_game.lower() != 'y':
        sys.exit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        hero.draw()
        monster.draw()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            hero.x -= 5
        if keys[pygame.K_RIGHT]:
            hero.x += 5
        if keys[pygame.K_UP]:
            hero.y -= 5
        if keys[pygame.K_DOWN]:
            hero.y += 5

        monster.move()

        if keys[pygame.K_SPACE]:
            damage = hero.attack()
            if pygame.Rect(hero.x, hero.y, 50, 50).colliderect(pygame.Rect(monster.x, monster.y, 50, 50)):
                print("Герой атакует монстра и наносит", damage, "урона!")
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
