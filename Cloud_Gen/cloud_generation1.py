import random
import pygame

pygame.init()
display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
TILESIZE = 24



def generate():
    cloud_size = random.randint(11, 16)
    strip_num = 9
    max_strip_length = 4
    strips = []
    for _ in range(strip_num):
        strips.append(random.randint(1, max_strip_length))
    
    strips.sort()

    center = random.randint(1, len(strips)-2)

    s1 = []
    s2 = []
    for i in range(0, strip_num, 2):
        if i+1 >= strip_num:
            break
        s1.append(strips[i])
        s2.append(strips[i+1])
        print(i)
    ss2 = []
    for i in s2:
        ss2 = [i] + ss2
    strips = s1 + [max_strip_length] + ss2
    print(strips)
    rects = []
    for index, s in enumerate(strips):
        y = HEIGHT // 2 - s * TILESIZE // 2
        x = WIDTH // 2 + index * TILESIZE
        h = s * TILESIZE
        rects.append((x, y, h))
    return rects
clock = pygame.time.Clock()
run = True

rects = generate()
drawing_rect = pygame.Rect(0, 0, TILESIZE, HEIGHT)
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
        drawing_rect.x, drawing_rect.y, drawing_rect.h = rect
        pygame.draw.rect(WIN, (255, 255, 255), drawing_rect)
    pygame.display.update()