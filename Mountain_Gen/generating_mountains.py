import random
import pygame

pygame.init()
display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
STEP_MAX = 2.5
STEP_CHANGE = 1
HEIGHT_MAX = HEIGHT * 0.3
TILESIZE = 24


def make_mountain(tilesize = TILESIZE):
    lines = []

    height = random.random() * HEIGHT_MAX
    slope = (random.random() * STEP_MAX) * 2 - STEP_MAX
    for x in range(WIDTH + TILESIZE):
        height += slope
        slope += (random.random() * STEP_CHANGE) * 2 - STEP_CHANGE

        if slope > STEP_MAX:
            slope = STEP_MAX
        if slope < -STEP_MAX:
            stope = -STEP_MAX
 
        if height < HEIGHT_MAX:
            height = HEIGHT_MAX
            slope *= -1;
        if height > HEIGHT:
            height = HEIGHT
            slope *= -1
        line = int(x // tilesize) * tilesize, int(HEIGHT), int(x // tilesize) * tilesize, int(height // tilesize) * tilesize
        if line not in lines:
            lines.append(line)
    return lines
clock = pygame.time.Clock()
run = True
lines = make_mountain()
while run:
    clock.tick(45)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_r:
                lines = make_mountain()
    WIN.fill((255, 255, 255))
    for line in lines:
        pygame.draw.line(WIN, (128, 128, 128), (line[0], line[1]), (line[2], line[3]), width = TILESIZE)
    pygame.display.update()