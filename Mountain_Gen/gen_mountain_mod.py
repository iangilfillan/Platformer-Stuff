import random

def generate(WIDTH, HEIGHT, tilesize, pull_down = 0.3, step_max = 2.5, step_change = 1):
    height_max = HEIGHT * pull_down
    lines = []

    height = random.random() * height_max
    slope = (random.random() * step_max) * 2 - step_max
    for x in range(WIDTH + tilesize):
        height += slope
        slope += (random.random() * step_change) * 2 - step_change

        if slope > step_max:
            slope = step_max
        if slope < -step_max:
            stope = -step_max
 
        if height < height_max:
            height = height_max
            slope *= -1;
        if height > HEIGHT:
            height = HEIGHT
            slope *= -1
        line = int(x // tilesize) * tilesize, int(HEIGHT), int(x // tilesize) * tilesize, int(height // tilesize) * tilesize
        if line not in lines:
            lines.append(line)
    return lines