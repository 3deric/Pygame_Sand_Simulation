import random
import pygame

SIZE : tuple = (800, 600)
PIXEL_SIZE : int = 8

world : [] = []
grid_width : int = int(SIZE[0] / PIXEL_SIZE)
grid_height : int = int(SIZE[1] / PIXEL_SIZE)

emit : bool = False
hue : int = 0.1


def init_world() -> []:
    _world = []
    for x in range(int(SIZE[0] / PIXEL_SIZE)):
        _world.append([])
        for y in range(int(SIZE[1] / PIXEL_SIZE)):
            _world[x].append(0)
    return _world

def update_world():
    # temporary world
    _temp = init_world()
    for x in range(grid_width):
        for y in range(grid_height):
            if world[x][y] > 0:
                _val = world[x][y]
                #check if element is at the bottom stop moving
                if y == grid_height -1:
                    _temp[x][y] = _val
                    break
                #check if space below is empty and move down if possible
                if world[x][y +1 ] == 0:
                    _temp[x][y + 1] = _val
                else:
                    #if space below is occupied try to move left or right
                    # randomize dir, pos or neg 1
                    _rand = random.choice([-1,1])
                    if (x - _rand >= 0) and (x - _rand < grid_width) and (world[x - _rand][y + 1]) == 0:
                        _temp[x-_rand][y] = _val

                    #keep the position if no movement is possible
                    else:
                        _temp[x][y] = _val

    return _temp

def draw_world():
    for x in range(grid_width):
        for y in range(grid_height):
            if world[x][y] > 0:
                _val = world[x][y]
                _color = pygame.Color(0,0,0)
                _color.hsva = (_val, 75,90,100)
                pygame.draw.rect(screen, _color, (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

def emit_points():
    if emit == True:
        pos = pygame.mouse.get_pos()
        world[int(pos[0] / PIXEL_SIZE)][int(pos[1] / PIXEL_SIZE)] = int(hue)
# pygame setup

pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption('Sand Simulation')
running = True
dt = 0

world = init_world()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if emit == True:
                    emit = False
                else:
                    emit = True

    screen.fill('black')
    # update and draw the sand
    emit_points()
    world = update_world()
    draw_world()
    # update the hue of the next spawned particle
    hue = (hue + 0.1) % 360
    pygame.display.flip()
    dt = clock.tick(60) / 1000

if __name__ == '__main__':
    pass