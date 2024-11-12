from OpenGL.GLUT import *
from lab3.camera import Camera
from lab3.shadow_map import ShadowMap

# Используем глобальный словарь для отслеживания нажатых клавиш
keys = {
    'w': False,
    'a': False,
    's': False,
    'd': False,
    'c': False,  # Для спуска вниз
    ' ': False,  # Для подъёма вверх (пробел)
}

# Отдельный флаг для отслеживания состояния переключения теней
toggle_pressed = {
    't': False
}
# Начальные значения для мыши
last_x, last_y = 400, 300
first_mouse = True


# Обработка нажатий клавиш
def key_pressed(key, x, y):
    """Обработка нажатий клавиш."""
    global keys, toggle_pressed
    if key == b'w':
        keys['w'] = True
    elif key == b'a':
        keys['a'] = True
    elif key == b's':
        keys['s'] = True
    elif key == b'd':
        keys['d'] = True
    elif key == b'c':
        keys['c'] = True  # Спуск камеры
    elif key == b' ':  # Пробел
        keys[' '] = True  # Подъём камеры
    elif key == b't' and not toggle_pressed['t']:
        # Переключаем шейдер только при первом нажатии клавиши 't'
        toggle_pressed['t'] = True


# Обработка отпусканий клавиш
def key_released(key, x, y):
    """Обработка отпусканий клавиш."""
    global keys, toggle_pressed
    if key == b'w':
        keys['w'] = False
    elif key == b'a':
        keys['a'] = False
    elif key == b's':
        keys['s'] = False
    elif key == b'd':
        keys['d'] = False
    elif key == b'c':
        keys['c'] = False  # Остановка спуска
    elif key == b' ':  # Пробел
        keys[' '] = False  # Остановка подъёма
    elif key == b't':
        toggle_pressed['t'] = False  # Сбрасываем флаг переключения


# Обработка движения камеры
def handle_camera_movement(camera: Camera):
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


def handle_shader_switch(shader: ShadowMap):
    """Включение/выключение шейдера, если кнопка 't' нажата."""
    global toggle_pressed
    if toggle_pressed['t']:
        shader.toggle_shader()
        toggle_pressed['t'] = False  # Сбрасываем флаг переключения после активации


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
