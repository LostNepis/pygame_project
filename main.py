import random
import pygame
import sys

size = width, height = 600, 600
cell_size = 40

def generate_level(level):
    flowers = []
    obstacles = []
    num_flowers = 5 + level
    num_obstacles = 3 + level

    for _ in range(num_flowers):
        flowers.append((random.randint(0, 14), random.randint(0, 14)))  # Assuming a 15x15 grid

    for _ in range(num_obstacles):
        obstacles.append((random.randint(0, 14), random.randint(0, 14)))

    return flowers, obstacles

# Draw grid and elements
def draw_level(screen, player_pos, flowers, obstacles, level):
    screen.fill((255, 255, 255))
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, (0, 0, 0), (0, y), (width, y))

    for flower in flowers:
        pygame.draw.rect(screen, (0, 255, 0), (flower[0] * cell_size, flower[1] * cell_size, cell_size, cell_size))
    for obstacle in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), (obstacle[0] * cell_size, obstacle[1] * cell_size, cell_size, cell_size))

    pygame.draw.rect(screen, (0, 0, 255), (player_pos[0] * cell_size, player_pos[1] * cell_size, cell_size, cell_size))

    pygame.display.flip()

# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Цветы")

    level = 1
    flowers, obstacles = generate_level(level)
    player_pos = [0, 0]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_pos[1] > 0:
                    player_pos[1] -= 1
                if event.key == pygame.K_DOWN and player_pos[1] < (height // cell_size) - 1:
                    player_pos[1] += 1
                if event.key == pygame.K_LEFT and player_pos[0] > 0:
                    player_pos[0] -= 1
                if event.key == pygame.K_RIGHT and player_pos[0] < (width // cell_size) - 1:
                    player_pos[0] += 1

        if tuple(player_pos) in flowers:
            flowers.remove(tuple(player_pos))

        if tuple(player_pos) in obstacles:
            running = False

        if not flowers:
            level += 1
            flowers, obstacles = generate_level(level)
            player_pos = [0, 0]

        draw_level(screen, player_pos, flowers, obstacles, level)

    pygame.quit()

if __name__ == "__main__":
    sys.exit(main())
