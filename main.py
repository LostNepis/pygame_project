import pygame
import random

pygame.init()

size = width, height = 600, 600
cell_size = 40
fps = 60
font = pygame.font.Font(None, 36)

flowers_collected = 0
high_score = 0
current_level = 1
time_left = 30

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Цветы")

def generate_level(level):
    """генерация уровня"""
    flowers = []
    obstacles = []
    num_flowers = 5 + level
    num_obstacles = 3 + level
    # рандомное размещение цветов и препятствий
    for _ in range(num_flowers):
        flowers.append((random.randint(0, (width // cell_size) - 1),
                        random.randint(0, (height // cell_size) - 1)))
    for _ in range(num_obstacles):
        obstacles.append((random.randint(0, (width // cell_size) - 1),
                          random.randint(0, (height // cell_size) - 1)))
    return flowers, obstacles

def draw_game(player_pos, flowers, obstacles):
    """отрисовка уровня"""
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

    text = font.render(f"Собрано цветов: {flowers_collected}", True, (0, 0, 0))
    screen.blit(text, (320, 10))
    text2 = font.render(f"Осталось времени: {time_left}", True, (0, 0, 0))
    screen.blit(text2, (320, 50))

def main_menu():
    """меню"""
    screen.fill((255, 255, 255))
    play_button = font.render("Играть", True, (0, 0, 0))
    quit_button = font.render("Выйти", True, (0, 0, 0))
    screen.blit(play_button, (250, 200))
    screen.blit(quit_button, (250, 300))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 250 <= x <= 350 and 200 <= y <= 236:
                    return True
                if 250 <= x <= 350 and 300 <= y <= 336:
                    return False

def game_loop():
    global flowers_collected, high_score, current_level, time_left
    player_pos = [0, 0]
    flowers, obstacles = generate_level(current_level)
    clock = pygame.time.Clock()
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # передвижение
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_pos[1] > 0:
                    player_pos[1] -= 1
                if event.key == pygame.K_DOWN and player_pos[1] < (height // cell_size) - 1:
                    player_pos[1] += 1
                if event.key == pygame.K_LEFT and player_pos[0] > 0:
                    player_pos[0] -= 1
                if event.key == pygame.K_RIGHT and player_pos[0] < (width // cell_size) - 1:
                    player_pos[0] += 1

            # проверка времени
            if event.type == timer_event:
                time_left -= 1
                if time_left <= 0:
                    return

        # игрок собрал цветок
        if tuple(player_pos) in flowers:
            flowers.remove(tuple(player_pos))
            flowers_collected += 1

        # игрок врезался в препятствие
        if tuple(player_pos) in obstacles:
            return


        # все цветы собраны
        if not flowers:
            current_level += 1
            time_left += 10
            flowers, obstacles = generate_level(current_level)

        draw_game(player_pos, flowers, obstacles)
        pygame.display.flip()
        clock.tick(fps)

while True:
    # обновление данных, при заходе в меню
    if main_menu():
        flowers_collected = 0
        current_level = 1
        time_left = 30
        game_loop()
    else:
        pygame.quit()
        break