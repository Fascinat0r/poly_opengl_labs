from OpenGL.GLUT import *

# Используем глобальный словарь для отслеживания нажатых клавиш
keys = {
    'w': False,
    'a': False,
    's': False,
    'd': False,
    'c': False,  # Для спуска вниз
    ' ': False,  # Для подъёма вверх (пробел)
    '1': False
}

# Начальные значения для мыши
last_x, last_y = 400, 300
first_mouse = True


# Обработка нажатий клавиш
def key_pressed(key, x, y):
    """Обработка нажатий клавиш."""
    global keys
    if key == b'w':
        keys['w'] = True
    if key == b'a':
        keys['a'] = True
    if key == b's':
        keys['s'] = True
    if key == b'd':
        keys['d'] = True
    if key == b'c':
        keys['c'] = True  # Спуск камеры
    if key == b' ':  # Пробел
        keys[' '] = True  # Подъём камеры
    if key == b'1':
        keys['1'] = True


# Обработка отпусканий клавиш
def key_released(key, x, y):
    """Обработка отпусканий клавиш."""
    global keys
    if key == b'w':
        keys['w'] = False
    if key == b'a':
        keys['a'] = False
    if key == b's':
        keys['s'] = False
    if key == b'd':
        keys['d'] = False
    if key == b'c':
        keys['c'] = False  # Остановка спуска
    if key == b' ':  # Пробел
        keys[' '] = False  # Остановка подъёма
    if key == b'1':
        keys['1'] = False


# Обработка движения камеры
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
    if keys['c']:
        camera.move_down()  # Спуск камеры вниз
    if keys[' ']:
        camera.move_up()  # Подъём камеры вверх


def handle_light_color_change(light):
    """Изменение цвета источника света."""
    if keys['1']:
        light.change_color()

# Создание обработчика движения мыши
def create_mouse_movement_handler(camera):
    """Создаём замыкание для обработки движения мыши с использованием камеры."""
    last_x, last_y = 400, 300
    first_mouse = True

    def mouse_movement(x, y):
        nonlocal last_x, last_y, first_mouse

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

    return mouse_movement
