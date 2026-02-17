import random
import pygame

SIZE : tuple = (800, 600)
PIXEL_SIZE : int = 8

grid_width : int = int(SIZE[0] / PIXEL_SIZE)
grid_height : int = int(SIZE[1] / PIXEL_SIZE)

def init_world() -> list:
    # create a empty world grid
    _world = []
    for x in range(grid_width):
        _world.append([])
        for y in range(grid_height):
            _world[x].append(0)
    return _world

def update_world(world : list, grid_width : int, grid_height : int) -> list:
    # update the world, save the data into a temp world first
    _temp = init_world()
    for x in range(grid_width):
        for y in range(grid_height):
            if world[x][y] > 0:
                _val = world[x][y]
                # check if element is at the bottom stop moving
                if y == grid_height - 1:
                    _temp[x][y] = _val
                    continue
                # check if space below is empty and move down if possible
                if world[x][y + 1] == 0:
                    _temp[x][y + 1] = _val
                else:
                    # if space below is occupied try to move left or right
                    # randomize dir, pos or neg 1
                    _rand = random.choice([-1, 1])
                    if (x - _rand >= 0) and (x - _rand < grid_width) and (world[x - _rand][y + 1]) == 0:
                        _temp[x - _rand][y] = _val
                    # keep the position if no movement is possible
                    else:
                        _temp[x][y] = _val
    return _temp

def draw_world(screen: pygame.Surface, world: list, grid_width: int, grid_height: int, pixel_size: int) -> None:
    # draw all elements
    for x in range(grid_width):
        for y in range(grid_height):
            if world[x][y] > 0:
                _val = world[x][y]
                _color = pygame.Color(0, 0, 0)
                _color.hsva = (_val, 75, 90, 100)
                pygame.draw.rect(screen, _color, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))

def emit_points(world: list, emit: bool, pos: tuple, pixel_size: int, hue: float) -> list:
    # emission of particles at curser positiuon
    if emit:
        _pos_x = int(pos[0] / pixel_size)
        _pos_y = int(pos[1] / pixel_size)
        if world[_pos_x][_pos_y] == 0:
            world[_pos_x][_pos_y] = int(hue)
    return world

def setup_pygame(size: tuple, caption: str) -> tuple:
    # setup pygame, init screen and clock
    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption(caption)
    return screen, clock

def run_simulation() -> None:
    # main simulation loop
    screen, clock = setup_pygame(SIZE, 'Sand Simulation')

    # Simulation variables
    world = init_world()
    emit = False
    hue = 0.1
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    emit = not emit  # Toggle emit

        # Clear screen
        screen.fill('black')

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Update and draw the sand
        world = emit_points(world, emit, mouse_pos, PIXEL_SIZE, hue)
        world = update_world(world, grid_width, grid_height)
        draw_world(screen, world, grid_width, grid_height, PIXEL_SIZE)

        # Update the hue of the next spawned particle
        hue = (hue + 0.1) % 360

        # Update display and maintain framerate
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    run_simulation()