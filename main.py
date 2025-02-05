import pygame
import random
import os


pygame.init()

size = width, height = 900, 900
cell_size = 60
fps = 60
font = pygame.font.Font(None, 36)

#загрузка картинок
down_image = pygame.transform.scale(pygame.image.load("pictures/down.png"), (cell_size, cell_size))
up_image = pygame.transform.scale(pygame.image.load("pictures/up.png"), (cell_size, cell_size))
left_image = pygame.transform.scale(pygame.image.load("pictures/left.png"), (cell_size, cell_size))
right_image = pygame.transform.scale(pygame.image.load("pictures/right.png"), (cell_size, cell_size))
player_image = down_image

pen_image = pygame.transform.scale(pygame.image.load("pictures/pen.png"), (cell_size, cell_size))

flower_images = [pygame.transform.scale(pygame.image.load(f"pictures/f{i}.png"), (cell_size, cell_size)) for i in range(1, 9)]

flowers_collected = 0
high_score = 0
current_level = 1
time_left = 30

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Цветы")

def load_data():
    global high_score
    if os.path.exists("game_data.txt"):
        with open("game_data.txt", 'r') as file:
            high_score = int(file.readline().strip())
    else:
        high_score = 0

def save_data(score):
    with open("game_data.txt", 'w') as file:
        file.write(str(score))


def generate_level(level):
    """генерация уровня"""
    flowers = [((random.randint(0, (width // cell_size) - 1),
                 random.randint(0, (height // cell_size) - 1)),
                random.choice(flower_images)) for _ in range(5 + level)]
    obstacles = [((random.randint(0, (width // cell_size) - 1),
                   random.randint(0, (height // cell_size) - 1)),
                  pen_image) for _ in range(3 + level)]
    return flowers, obstacles


def draw_game(player_pos, flowers, obstacles, player_image):
    """отрисовка уровня"""
    screen.fill((255, 255, 255))
    for x in range(width // cell_size):
        for y in range(height // cell_size):
            color = (140, 135, 166) if (x + y) % 2 == 0 else (106, 95, 162)
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

    for flower in flowers:
        screen.blit(flower[1], (flower[0][0] * cell_size, flower[0][1] * cell_size))
    for obstacle in obstacles:
        screen.blit(obstacle[1], (obstacle[0][0] * cell_size, obstacle[0][1] * cell_size))

    screen.blit(player_image, (player_pos[0] * cell_size, player_pos[1] * cell_size))

    collected_text = font.render(f"Собрано цветов: {flowers_collected}", True, (0, 0, 0))
    screen.blit(collected_text, (320, 10))
    time_text = font.render(f"Осталось времени: {time_left}", True, (0, 0, 0))
    screen.blit(time_text, (320, 50))

def main_menu():
    """меню"""
    screen.fill((255, 255, 255))
    play_button = font.render("Играть", True, (0, 0, 0))
    quit_button = font.render("Выйти", True, (0, 0, 0))
    time_text = font.render(f"Твой рекорд: {high_score}", True, (0, 0, 0))
    screen.blit(time_text, (320, 50))
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
                if 250 <= x <= 350 and 200 <= y <= 236: # нажата кнопка играть
                    return True
                if 250 <= x <= 350 and 300 <= y <= 336: # нажата выйти
                    return False

def game_loop():
    """основной цикл"""
    global flowers_collected, high_score, current_level, time_left, player_image
    player_pos = [0, 0]
    flowers, obstacles = generate_level(current_level)
    clock = pygame.time.Clock()
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # передвижение
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_pos[1] > 0:
                    player_pos[1] -= 1
                    player_image = up_image
                if event.key == pygame.K_DOWN and player_pos[1] < (height // cell_size) - 1:
                    player_pos[1] += 1
                    player_image = down_image
                if event.key == pygame.K_LEFT and player_pos[0] > 0:
                    player_pos[0] -= 1
                    player_image = left_image
                if event.key == pygame.K_RIGHT and player_pos[0] < (width // cell_size) - 1:
                    player_pos[0] += 1
                    player_image = right_image

            # убавление времени
            if event.type == timer_event:
                time_left -= 1
                if time_left <= 0:
                    return

        for flower in flowers:
            # удаление цветка при касании с игроком
            if player_pos == list(flower[0]):
                flowers.remove(flower)
                flowers_collected += 1
                break

        # смерть при касании препятствия
        if any(player_pos == list(obstacle[0]) for obstacle in obstacles):
            return

        # переход на следущий уровень
        if not flowers:
            current_level += 1
            time_left += 10
            flowers, obstacles = generate_level(current_level)


        draw_game(player_pos, flowers, obstacles, player_image)
        pygame.display.flip()
        clock.tick(60)

load_data()
while True:
    # обновление данных, при заходе в меню
    if main_menu():
        if flowers_collected > high_score:
            save_data(flowers_collected)
        flowers_collected = 0
        current_level = 1
        time_left = 15
        game_loop()


    else:
        pygame.quit()
        break