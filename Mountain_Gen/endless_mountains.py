import random
import pygame

pygame.init()
display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
STEP_MAX = 2.5
STEP_CHANGE = 0.5
HEIGHT_MAX = HEIGHT * 0.3 
TILESIZE = 24



def generate(List, slope, height):
    rects = []
    for x in List:
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
        rect = int(x // TILESIZE)*TILESIZE, int(height // TILESIZE) * TILESIZE
        for r in rects:
            if rect[0] == r[0]:
                break
        else:
            rects.append(rect)
    return rects, slope, height
clock = pygame.time.Clock()
run = True
height = random.random() * HEIGHT_MAX
slope = (random.random() * STEP_MAX) * 2 - STEP_MAX
rects = []

List = range(WIDTH)
rs, slope, height = generate(List, slope, height)
rects += rs
drawing_rect = pygame.Rect(0, 0, TILESIZE, HEIGHT)
x_offset = 0
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_r:
                List = range(len(rects) * TILESIZE, len(rects) * TILESIZE + WIDTH)
                rs, slope, height = generate(List, slope, height)
                rects += rs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        x_offset -= 10
    if keys[pygame.K_a]:
        x_offset += 10
    if -x_offset >= len(rects) * TILESIZE - WIDTH:
        List = range(len(rects) * TILESIZE, len(rects) * TILESIZE + WIDTH)
        rs, slope, height = generate(List, slope, height)
        rects += rs
    WIN.fill((255, 255, 255))
    for rect in rects:
        drawing_rect.x, drawing_rect.y = rect
        drawing_rect.x += x_offset
        pygame.draw.rect(WIN, (144, 144, 144), drawing_rect)
    pygame.display.update()