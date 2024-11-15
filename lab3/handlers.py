# handlers.py
import glm

from OpenGL.raw.GLUT import glutWarpPointer
from lab3.camera import Camera

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
    key = key.decode('utf-8').lower()
    if key == 'w':
        keys['w'] = True
    elif key == 'a':
        keys['a'] = True
    elif key == 's':
        keys['s'] = True
    elif key == 'd':
        keys['d'] = True
    elif key == 'c':
        keys['c'] = True  # Спуск камеры
    elif key == ' ':
        keys[' '] = True  # Подъём камеры вверх
    elif key == 't' and not toggle_pressed['t']:
        # Переключаем шейдер или теневую опцию
        toggle_pressed['t'] = True
        # Здесь можно добавить логику переключения теней
        print("Toggle shadows")  # Пример действия


# Обработка отпусканий клавиш
def key_released(key, x, y):
    """Обработка отпусканий клавиш."""
    global keys, toggle_pressed
    key = key.decode('utf-8').lower()
    if key == 'w':
        keys['w'] = False
    elif key == 'a':
        keys['a'] = False
    elif key == 's':
        keys['s'] = False
    elif key == 'd':
        keys['d'] = False
    elif key == 'c':
        keys['c'] = False  # Остановка спуска
    elif key == ' ':
        keys[' '] = False  # Остановка подъёма камеры вверх
    elif key == 't':
        toggle_pressed['t'] = False  # Сбрасываем флаг переключения


# Обработка движения камеры
def handle_camera_movement(camera: Camera, delta_time=0.016):
    """Движение камеры на основе нажатых клавиш."""
    move_direction = glm.vec3(0.0, 0.0, 0.0)

    if keys['w']:
        move_direction += camera.front  # Вперёд
    if keys['s']:
        move_direction -= camera.front  # Назад
    if keys['a']:
        move_direction -= camera.right  # Влево
    if keys['d']:
        move_direction += camera.right  # Вправо
    if keys[' ']:
        move_direction += camera.world_up  # Вверх
    if keys['c']:
        move_direction -= camera.world_up  # Вниз

    # Нормализация вектора движения, чтобы скорость оставалась постоянной
    if glm.length(move_direction) > 0:
        move_direction = glm.normalize(move_direction)

    # Применение движения к позиции камеры
    camera.position += move_direction * camera.speed * delta_time


# Создание обработчика движения мыши
def create_mouse_movement_handler(camera, get_window_size):
    """Создаём замыкание для обработки движения мыши с использованием камеры."""
    last_x, last_y = 0, 0
    first_mouse = True

    def mouse_movement(x, y):
        nonlocal last_x, last_y, first_mouse

        # Получаем текущие размеры окна
        window_width, window_height = get_window_size()

        # Центр окна
        center_x = window_width // 2
        center_y = window_height // 2

        if first_mouse:
            last_x, last_y = x, y
            first_mouse = False

        # Вычисляем смещение
        x_offset = x - last_x
        y_offset = last_y - y  # Инвертируем Y

        # Сохраняем текущую позицию для следующего шага
        last_x, last_y = x, y

        # Передаём смещение в камеру
        camera.process_mouse_movement(x_offset, y_offset)

        # Возвращаем курсор в центр окна
        glutWarpPointer(center_x, center_y)
        last_x, last_y = center_x, center_y  # Сбрасываем координаты в центр

    return mouse_movement


def reset_mouse_position(window_width, window_height):
    """Возвращает мышь в центр окна."""
    center_x, center_y = window_width // 2, window_height // 2
    glutWarpPointer(center_x, center_y)
