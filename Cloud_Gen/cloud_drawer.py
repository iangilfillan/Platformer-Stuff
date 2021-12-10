import random
import pygame

pygame.init()
display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
TILESIZE = 24

all_clouds = []

tiles = []
for y in range(HEIGHT//TILESIZE):
    tiles.append([])
    for x in range(WIDTH//TILESIZE):
        tiles[y].append(0)


def add_cloud(tiles):
    rects = []
    count = 0
    for y_index, y in enumerate(tiles):
        for x_index, b in enumerate(tiles[y_index]):
            if b == 1:
                if count == 0:
                    rx, ry = x_index, y_index
                count += 1
                rects.append((y_index - ry, x_index - rx))
    all_clouds.append(rects)

    string = ""
    for a in all_clouds:
        for b in a:
            string += str(b)
        string += "\n"
    with open("cloud_types.txt", "w") as File:
        File.write(string)
clock = pygame.time.Clock()
run = True

drawing_rect = pygame.Rect(0, 0, TILESIZE, TILESIZE)
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_r:
                add_cloud(tiles)
                tiles = []
                for y in range(HEIGHT//TILESIZE):
                    tiles.append([])
                    for x in range(WIDTH//TILESIZE):
                        tiles[y].append(0)
    
    state = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    x, y = x // TILESIZE, y // TILESIZE
    if state[0] == 1:
        tiles[y][x] = 1
    elif state[2] == 1:
        tiles[y][x] = 0


    WIN.fill((135, 206, 235))
    for y_index, y in enumerate(tiles):
        for x_index, b in enumerate(tiles[y_index]):
            if b == 1:
                drawing_rect.x, drawing_rect.y = x_index * TILESIZE, y_index * TILESIZE
                pygame.draw.rect(WIN, (255, 255, 255), drawing_rect)
    pygame.display.update()