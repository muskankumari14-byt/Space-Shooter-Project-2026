
import random
import pygame

pygame.init()

# Game settings
WIDTH = 600
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (10, 10, 25)
BLUE = (50, 150, 255)
YELLOW = (255, 220, 40)
RED = (240, 70, 70)
GREEN = (80, 220, 120)
GRAY = (180, 180, 190)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)
large_font = pygame.font.SysFont(None, 64)
small_font = pygame.font.SysFont(None, 24)


# Ship class
class Ship:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = (WIDTH - self.width) // 2
        self.y = 520
        self.speed = 8
        self.rect = pygame.Rect(
            self.x, self.y, self.width, self.height
        )

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        self.x = max(0, min(self.x, WIDTH - self.width))
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        pygame.draw.polygon(
            surface, BLUE,
            [
                (self.x + 25, self.y),
                (self.x + 3, self.y + 45),
                (self.x + 25, self.y + 37),
                (self.x + 47, self.y + 45)
            ]
        )

        pygame.draw.rect(
            surface, GRAY,
            (self.x + 19, self.y + 25, 12, 18),
            border_radius=3
        )


# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.width = 5
        self.height = 10
        self.x = x
        self.y = y
        self.speed = 10
        self.rect = pygame.Rect(
            self.x, self.y, self.width, self.height
        )

    def update(self):
        self.y -= self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        pygame.draw.rect(surface, YELLOW, self.rect)

    def is_off_screen(self):
        return self.y + self.height < 0


# Enemy class
class Enemy:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, WIDTH - self.width)
        self.y = -self.height
        self.speed = random.randint(2, 4)
        self.rect = pygame.Rect(
            self.x, self.y, self.width, self.height
        )

    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        pygame.draw.rect(
            surface, RED, self.rect, border_radius=7
        )

        pygame.draw.circle(
            surface, WHITE, (self.x + 12, self.y + 14), 4
        )
        pygame.draw.circle(
            surface, WHITE, (self.x + 28, self.y + 14), 4
        )
        pygame.draw.line(
            surface, BLACK,
            (self.x + 12, self.y + 29),
            (self.x + 28, self.y + 29), 3
        )


# Display text
def draw_text(surface, text, font_object, color,
              x, y, center=False):
    image = font_object.render(text, True, color)
    rect = image.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    surface.blit(image, rect)


# Reset the game
def reset_game():
    return Ship(), [], [], 0, 3, pygame.time.get_ticks()


# Main game
ship, bullets, enemies, score, lives, last_enemy_time = reset_game()

running = True
game_over = False
enemy_spawn_delay = 1000

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Fire bullet using SPACE
            if event.key == pygame.K_SPACE and not game_over:
                if len(bullets) < 5:
                    bullet_x = ship.x + ship.width // 2
                    bullet_y = ship.y

                    bullets.append(Bullet(bullet_x, bullet_y))

                    print(
                        f"Bullet fired at ({bullet_x}, {bullet_y}) | "
                        f"Bullets on screen: {len(bullets)}"
                    )
                else:
                    print("Maximum 5 bullets on screen. No bullet fired.")
                    print("Bullets on screen: 5")

            # Restart using R
            if event.key == pygame.K_r and game_over:
                ship, bullets, enemies, score, lives, last_enemy_time = reset_game()
                game_over = False

    if not game_over:
        keys = pygame.key.get_pressed()
        ship.move(keys)

        # Spawn enemies
        current_time = pygame.time.get_ticks()

        if current_time - last_enemy_time >= enemy_spawn_delay:
            enemies.append(Enemy())
            last_enemy_time = current_time

        # Update bullets
        for bullet in bullets:
            bullet.update()

        bullets = [
            bullet for bullet in bullets
            if not bullet.is_off_screen()
        ]

        # Update enemies and reduce lives
        for enemy in enemies[:]:
            enemy.update()

            if enemy.y >= HEIGHT:
                enemies.remove(enemy)
                lives -= 1

                print(f"Enemy escaped | Lives: {lives}")

                if lives <= 0:
                    game_over = True
                break

        # Bullet-enemy collision detection
        for bullet in bullets[:]:
            hit_enemy = None

            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    hit_enemy = enemy
                    break

            if hit_enemy is not None:
                bullets.remove(bullet)
                enemies.remove(hit_enemy)
                score += 5

                print(
                    f"Enemy destroyed | Score: {score} "
                    f"| Lives: {lives}"
                )

    # Draw background
    screen.fill(BLACK)

    # Stars
    stars = [
        (40, 60), (130, 120), (220, 45),
        (350, 95), (500, 55), (570, 180),
        (75, 250), (180, 330), (420, 270),
        (530, 390), (300, 410), (100, 470),
        (460, 500), (250, 180), (390, 540)
    ]

    for star_x, star_y in stars:
        pygame.draw.circle(
            screen, WHITE, (star_x, star_y), 2
        )

    # Draw ship, bullets and enemies
    ship.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    # Score and lives
    draw_text(screen, f"Score: {score}",
              font, WHITE, 10, 10)

    draw_text(screen, f"Lives: {lives}",
              font, GREEN, WIDTH - 100, 10)

    draw_text(
        screen, "Move: LEFT/RIGHT   Fire: SPACE",
        small_font, GRAY, 10, HEIGHT - 28
    )

    # Game over screen
    if game_over:
        overlay = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        draw_text(
            screen, "GAME OVER", large_font, RED,
            WIDTH // 2, HEIGHT // 2 - 45, True
        )

        draw_text(
            screen, f"Final Score: {score}",
            font, WHITE, WIDTH // 2,
            HEIGHT // 2 + 5, True
        )

        draw_text(
            screen, "Press R to Restart or close the window",
            small_font, WHITE, WIDTH // 2,
            HEIGHT // 2 + 45, True
        )

    pygame.display.flip()

pygame.quit()
