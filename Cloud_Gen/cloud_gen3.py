import random
import pygame

pygame.init()
display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
TILESIZE = 24



def generate():
    rects = [(WIDTH // 2, HEIGHT // 2)]
    for i in range(4):
        d = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        x, y = random.choice(rects)
        a, y = x + d[0] * TILESIZE * 2, y + d[1] * TILESIZE
        rects.append((a, y))
        x, y = x + d[0] * TILESIZE, y + d[1] * TILESIZE
        rects.append((x, y))
    for r in rects.copy():
        x, y = r
        dx = [0, 0, 1, -1]
        dy = [0, 0, 1, -1]
        for ax in dx:
            for ay in dy:
                rects.append((x+ax * TILESIZE, y+ay * TILESIZE))
                rects.append((x+ax * TILESIZE * 2, y+ay * TILESIZE))
    return rects
clock = pygame.time.Clock()
run = True

rects = generate()
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
                rects = generate()
    keys = pygame.key.get_pressed()
    WIN.fill((135, 206, 235))
    for rect in rects:
        drawing_rect.x, drawing_rect.y = rect
        pygame.draw.rect(WIN, (255, 255, 255), drawing_rect)
    pygame.display.update()