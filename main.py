# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0; cols = 10; rows = 10; grid_node_width = 50; grid_node_height = 50
matrix = [[[1, 0], [0, 0], [1, 0], [0, 0], [0, 0], [1, 0]], [[1, 0], [0, 0], [1, 0], [0, 0], [0, 0], [1, 0]], [[1, 0], [1, 0], [0, 0], [0, 0], [0, 0], [1, 0]], [[1, 0], [0, 0], [1, 0], [0, 0], [0, 0], [1, 0]], [[0, 0], [1, 0], [1, 0], [1, 0], [0, 0], [1, 0]], [[1, 0], [0, 0], [1, 0], [1, 0], [1, 0], [0, 0]]]
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
gridDisplay = pygame.display.set_mode((1000, 700)) # screen resolution and size
pygame.display.get_surface().fill((200, 200, 200))  # background
pygame.font.init()
matrix_start_x = 100
matrix_start_y = 100
highlighted = []


def create_square(x, y, color):
    pygame.draw.rect(gridDisplay, color, [x, y, grid_node_width, grid_node_height])


def text_generator(contents, x=0, y=0, color=white, font='freesansbold.ttf', size=100):
    display_surface = pygame.display.set_mode((x, y))
    font = pygame.font.Font(font, size)
    text = font.render(contents, True, 'black', color)
    text_rect = text.get_rect()
    text_rect.center = (x // 2, y // 2)
    display_surface.blit(text, text_rect)


def update_highlighted(highlighted_coordinates):
    shifting_value = 0
    for coordinates in highlighted_coordinates:
        try:
            create_square(matrix_start_x + grid_node_width * coordinates[1], matrix_start_y + grid_node_height * coordinates[0], (255, shifting_value, 0))
            shifting_value += 25
        except ValueError:
            pass


def visualize_grid(given_x=matrix_start_x, y=matrix_start_y, pixel_width=grid_node_width, pixel_height=grid_node_height):
    for row in matrix:
        x = given_x  # for every row we start at the left of the screen again
        for item in row:
            if item[1] == 0:
                # non highlighted
                if item[0] == 0:
                    create_square(x, y, (255, 255, 255))
                else:
                    create_square(x, y, (0, 0, 0))
            else:
                # highlighted
                pass
                #create_square(x, y, (255, 0 + 50 * len(highlighted), 0))

            x += pixel_width  # for every item/number in that row we move one "step" to the right
        y += pixel_height  # for every new row we move one "step" downwards
    update_highlighted(highlighted)
    pygame.display.update()


def check_if_clicked(mouse_position, matrix, start, pixel_width, pixel_height):
    mouse_x, mouse_y = mouse_position
    x_start, y_start = start
    x_end = x_start + pixel_width * len(matrix[0])
    y_end = y_start + pixel_height * len(matrix)

    if x_start <= mouse_x <= x_end and y_start <= mouse_y <= y_end:
        return True
    return False


def ascertain_coordinates(mouse_position, start, pixel_width, pixel_height):
    mouse_x, mouse_y = mouse_position
    x_start, y_start = start
    row_number = int((mouse_y - y_start) / pixel_height)
    column_number = int((mouse_x - x_start) / pixel_width)
    return row_number, column_number


def inverse_pixel(pixel_numbers):
    row_number, column_number = pixel_numbers
    if matrix[row_number][column_number][0]:
        matrix[row_number][column_number][0] = False
    else:
        matrix[row_number][column_number][0] = True


def highlight(pixel_numbers):
    row_number, column_number = pixel_numbers
    current_pixel = matrix[row_number][column_number]
    if current_pixel[1]:
        current_pixel[1] = False
        highlighted.remove((row_number, column_number))
    else:
        if len(highlighted) > 10:
            print("You have reached the maximum amount of highlights!")
            return
        else:
            current_pixel[1] = 1 + len(highlighted)
            highlighted.append((row_number, column_number))


def text_generator_better(contents, x=0, y=0, color='black', font='freesansbold.ttf', size=50):
    font = pygame.font.Font(font, size)
    text_surface = font.render(contents, False, color)
    screen.blit(text_surface, (x, y))


pygame.display.set_caption('Pathfinding Visualizer') # title
text_generator_better('Pathfinding algorithms visualizer')
update = False
visualize_grid()
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    visualize_grid()  # call the function

    event = pygame.event.wait()
    if event.type == pygame.MOUSEBUTTONDOWN:
        # 1 - left click
        # 2 - middle click
        # 3 - right click
        # 4 - scroll up
        # 5 - scroll down
        pos = pygame.mouse.get_pos()
        if check_if_clicked(pos, matrix, (matrix_start_x, matrix_start_y), grid_node_width, grid_node_height):
            print(f'mouse clicked at {pos}')
            coords = ascertain_coordinates(pos, (matrix_start_x, matrix_start_y), grid_node_width, grid_node_height)
            if event.button == 1:
                inverse_pixel(coords)
            if event.button == 3:
                highlight(coords)
                print(f'highlighted at {highlighted}')

    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
