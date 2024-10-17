from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT import *

keys = {
    'w': False,
    'a': False,
    's': False,
    'd': False
}

# Начальные значения для мыши
last_x, last_y = 400, 300
first_mouse = True


def key_pressed(key, x, y):
    """Обработка нажатий клавиш."""
    global keys
    print(f"Key pressed: {key}")
    if key == b'w':
        keys['w'] = True
    if key == b'a':
        keys['a'] = True
    if key == b's':
        keys['s'] = True
    if key == b'd':
        keys['d'] = True


def key_released(key, x, y):
    """Обработка отпусканий клавиш."""
    global keys
    print(f"Key released: {key}")
    if key == b'w':
        keys['w'] = False
    if key == b'a':
        keys['a'] = False
    if key == b's':
        keys['s'] = False
    if key == b'd':
        keys['d'] = False


def handle_camera_movement(camera):
    """Движение камеры на основе нажатых клавиш."""
    if keys['w']:
        camera.move_forward()
    if keys['s']:
        camera.move_backward()
    if keys['a']:
        camera.move_left()
    if keys['d']:
        camera.move_right()


def mouse_movement(x, y, camera):
    """Обработка движения мыши."""
    global last_x, last_y, first_mouse

    # Центр окна
    center_x, center_y = 400, 300

    if first_mouse:
        last_x, last_y = x, y
        first_mouse = False

    x_offset = x - last_x
    y_offset = last_y - y  # Инвертируем Y

    last_x, last_y = center_x, center_y  # Перемещаем указатель мыши в центр

    camera.rotate(x_offset, y_offset)

    # Возвращаем указатель мыши в центр окна
    glutWarpPointer(center_x, center_y)
