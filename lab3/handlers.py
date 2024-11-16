import glm
from OpenGL.raw.GLUT import glutWarpPointer
from lab3.camera import Camera

# Используем глобальный словарь для отслеживания нажатых клавиш (по keycode)
keys = {
    119: False,  # W
    97: False,   # A
    115: False,  # S
    100: False,  # D
    99: False,   # C (спуск вниз)
    32: False,   # SPACE (подъем вверх)
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
    keycode = ord(key)
    if keycode in keys:
        keys[keycode] = True
    elif keycode == ord('t') and not toggle_pressed['t']:
        # Переключаем шейдер или теневую опцию
        toggle_pressed['t'] = True
        print("Toggle shadows")  # Пример действия


# Обработка отпусканий клавиш
def key_released(key, x, y):
    """Обработка отпусканий клавиш."""
    global keys, toggle_pressed
    keycode = ord(key)
    if keycode in keys:
        keys[keycode] = False
    elif keycode == ord('t'):
        toggle_pressed['t'] = False  # Сбрасываем флаг переключения


# Обработка движения камеры
def handle_camera_movement(camera: Camera, delta_time=0.016):
    """Движение камеры на основе нажатых клавиш."""
    move_direction = glm.vec3(0.0, 0.0, 0.0)

    if keys[119]:  # W
        move_direction += camera.front  # Вперёд
    if keys[115]:  # S
        move_direction -= camera.front  # Назад
    if keys[97]:   # A
        move_direction -= camera.right  # Влево
    if keys[100]:  # D
        move_direction += camera.right  # Вправо
    if keys[32]:   # SPACE
        move_direction += camera.world_up  # Вверх
    if keys[99]:   # C
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
