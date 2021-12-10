import pygame

pygame.init()
width, height = 900, 600
WIN = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    WIN.fill((200, 200, 200))
    x, y = pygame.mouse.get_pos()
    x += 48
    y1, y2 = y+24, y-24
    distance_to_edge = x - width
    line_width = max(48,distance_to_edge)
    offset = line_width/2
    pygame.draw.line(WIN, (128, 128, 128), (x - offset, y1), (x - offset, y2), width = 48)
    pygame.display.update()