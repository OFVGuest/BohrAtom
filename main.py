import sys
import pygame
import math
import numpy as np


# region Global variables
const_h = 4.13566 * 10 ** (-15)
var_lambda = 600
var_quantum = 1
val_frequency = (3 * 10 ** 8) / var_lambda
energia_foton = const_h * val_frequency
energia_electron = -13.6 / var_quantum ** 2
num_orbits_to_skip = 1
# endregion


# region screenConfig
pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bohr\'s mind')
# endregion


# region GlobalColors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
# endregion


# region Class
class Sphere:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.callback()
# endregion


# region functions definitions
def high_level():
    global var_quantum, orbit_radius, energia_electron, energia_foton
    if var_quantum + num_orbits_to_skip < 7:
        var_quantum += num_orbits_to_skip
        orbit_radius = (screen_height / 50) * var_quantum ** 2
        energia_electron = -13.6 / var_quantum ** 2


def lower_level():
    global var_quantum, orbit_radius, energia_electron, energia_foton, val_frequency, var_lambda
    energia_electron0 = energia_electron
    if var_quantum - num_orbits_to_skip > 0:
        var_quantum -= num_orbits_to_skip
        orbit_radius = (screen_height / 50) * var_quantum ** 2
        energia_electron = -13.6 / var_quantum ** 2
        val_frequency = np.abs(energia_electron - energia_electron0) / const_h
        var_lambda = (3 * 10 ** 8) / val_frequency
        foton_calculator()


def calculate_color_intensity(tick_color):
    if tick_color <= 30:
        intensity = 255
    elif 30 < tick_color <= 60:
        intensity = 255 - ((tick_color - 30) * (255 - 100) / 30)
    else:
        intensity = 100  # Mínima intensidad después de 60 ticks
    return int(intensity)


def foton_calculator():
    global var_lambda, background_color, tick_color

    # Definir colores con intensidad reducida y transparencia
    alpha = 0.2  # Valor de transparencia, puedes ajustarlo según sea necesario
    reduced_red = (255, 0, 0, alpha)
    reduced_green = (0, 255, 0, alpha)
    reduced_blue = (0, 0, 255, alpha)
    reduced_cyan = (0, 255, 255, alpha)
    reduced_purple = (255, 0, 255, alpha)

    if 618 * 10 ** (-9) < var_lambda < 780 * 10 ** (-9):
        background_color = reduced_red
    elif 581 * 10 ** (-9) < var_lambda < 618 * 10 ** (-9):
        background_color = reduced_red
    elif 570 * 10 ** (-9) < var_lambda < 581 * 10 ** (-9):
        background_color = reduced_red
    elif 497 * 10 ** (-9) < var_lambda < 570 * 10 ** (-9):
        background_color = reduced_green
    elif 476 * 10 ** (-9) < var_lambda < 497 * 10 ** (-9):
        background_color = reduced_cyan
    elif 427 * 10 ** (-9) < var_lambda < 476 * 10 ** (-9):
        background_color = reduced_blue
    elif 380 * 10 ** (-9) < var_lambda < 427 * 10 ** (-9):
        background_color = reduced_purple
    elif var_lambda > 780 * 10 ** (-9):
        print("Infrarrojos")
    elif var_lambda < 380 * 10 ** (-9):
        print("UVs")
    else:
        background_color = (255, 255, 255, alpha)  # Color blanco con transparencia
    tick_color = 50


# Función para obtener las coordenadas de la esfera que gira alrededor de otra
def get_orbit_coordinates(center_x, center_y, radius, angle):
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    return int(x), int(y)


def get_circle_coordinates(center_x, center_y, radius, num_points=100):
    circle_points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        circle_points.append((int(x), int(y)))
    return circle_points


# endregion


# region initial
# Orbit
orbit_radius = (screen_height / 50) * var_quantum ** 2
angle = 0
# Buttons
button_width, button_height = 150, 50
button_x = 50
button_y_top = 50
button_y_bottom = 150
plus_button = Button(button_x, button_y_top, button_width, button_height, "+", high_level)
minus_button = Button(button_x, button_y_bottom, button_width, button_height, "-", lower_level)
# Esfera en el centro
center_x = screen_width // 2
center_y = screen_height // 2
radius = [screen_height / 50, (4 * screen_height) / 50, (9 * screen_height) / 50, (16 * screen_height) / 50,
          (25 * screen_height) / 50, (36 * screen_height) / 50]
center_sphere = Sphere(center_x, center_y, 10, RED)
circle_coordinates = []
# endregion


# region bucleFor
for i in radius:
    circle_coordinates.append(get_circle_coordinates(center_x, center_y, i))
clock = pygame.time.Clock()
running = True
background_color = WHITE  # Color de fondo inicial
tick_color = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            num_orbits_to_skip = 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            num_orbits_to_skip = 2
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            num_orbits_to_skip = 3
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
            num_orbits_to_skip = 4
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                plus_button.handle_click()
                minus_button.handle_click()

    # Coordenadas de la orbita
    orbit_x, orbit_y = get_orbit_coordinates(center_x, center_y, orbit_radius, angle)

    # Draw atomo
    screen.fill(WHITE)
    center_sphere.draw()
    plus_button.draw()
    minus_button.draw()
    pygame.draw.circle(screen, BLUE, (orbit_x, orbit_y), 3)
    for coordinate in circle_coordinates:
        pygame.draw.lines(screen, BLACK, False, coordinate, 1)

    square_size = 50
    square_x = screen_width - square_size
    square_y = screen_height - square_size

    # Dibujar el cuadrado azul con borde negro
    pygame.draw.rect(screen, background_color, (square_x, square_y, square_size, square_size))
    pygame.draw.rect(screen, BLACK, (square_x, square_y, square_size, square_size), 2)

    # Actualizar el ángulo para hacer que la esfera gire
    # El ángulo 0.5 es para n = 1
    angle += 0.5 / var_quantum
    if tick_color > 10:
        print(tick_color)
        tick_color -= 1
    else:
        background_color=WHITE

    pygame.display.flip()
    clock.tick(60)
# endregion


pygame.quit()
sys.exit()
