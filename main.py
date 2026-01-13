import pygame
import sys

# ---------------- CONFIGURACIÓN ----------------
WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (135, 206, 235)
RED = (255, 0, 0)

# ---------------- FUNCIONES ----------------
def load_sprite(path, fallback_color, size=(50, 50)):
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)
    except:
        surface = pygame.Surface(size)
        surface.fill(fallback_color)
        return surface

# ---------------- CLASES ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_sprite("assets/mario.png", BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        dx = 0
        if keys[pygame.K_a]:
            dx = -5
        if keys[pygame.K_d]:
            dx = 5

        # Salto
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15
            self.on_ground = False

        # Gravedad
        self.vel_y += 1
        dy = self.vel_y

        # Movimiento horizontal
        self.rect.x += dx

        # Movimiento vertical + colisiones
        self.rect.y += dy
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dy > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_sprite("assets/enemy.png", RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 1

    def update(self):
        self.rect.x += self.direction * 2
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.direction *= -1

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_sprite("assets/flag.png", GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

# ---------------- JUEGO ----------------
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Juego de Plataformas")
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player(100, 500)
        self.enemy = Enemy(600, 500)

        self.platforms = [
            Platform(0, 550, 800, 50),
            Platform(150, 450, 150, 20),
            Platform(400, 350, 150, 20),
        ]

        self.flag = Flag(700, 300)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.player.update(self.platforms)
        self.enemy.update()

        if self.player.rect.colliderect(self.flag.rect):
            print("¡GANASTE!")
            self.running = False

    def draw(self):
        self.screen.fill(BLUE)

        for platform in self.platforms:
            self.screen.blit(platform.image, platform.rect)

        self.screen.blit(self.flag.image, self.flag.rect)
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.enemy.image, self.enemy.rect)

        pygame.display.flip()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()