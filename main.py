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
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = max(0, min(SCREEN_WIDTH - 50, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - 50, self.y))
    
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
        self.health = 100  # Добавляем здоровье монстру
    
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, 50, 50))
    
    def move(self):
        self.x += random.randint(-10, 10)
        self.y += random.randint(-10, 10)
        self.x = max(0, min(SCREEN_WIDTH - 50, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - 50, self.y))
    
    def take_damage(self, amount):
        self.health -= amount
        print(f"Здоровье монстра: {self.health}")  # Печатаем здоровье монстра после атаки
        if self.health <= 0:
            print("Монстр повержен!")
            pygame.quit()
            sys.exit()

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
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            hero.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            hero.move(5, 0)
        if keys[pygame.K_UP]:
            hero.move(0, -5)
        if keys[pygame.K_DOWN]:
            hero.move(0, 5)
        if keys[pygame.K_SPACE]:  # Атака активируется при нажатии клавиши SPACE
            if pygame.Rect(hero.x, hero.y, 50, 50).colliderect(pygame.Rect(monster.x, monster.y, 50, 50)):
                damage = hero.attack()
                print(f"Герой атакует монстра и наносит {damage} % урона!")
                monster.take_damage(damage)

        monster.move()
        
        screen.fill(WHITE)
        hero.draw()
        monster.draw()
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
