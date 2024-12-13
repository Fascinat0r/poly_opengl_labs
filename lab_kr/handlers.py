from typing import List

import glm
from OpenGL.GLUT import glutLeaveMainLoop
from OpenGL.raw.GLUT import glutWarpPointer
from lab_kr.camera import Camera
from lab_kr.particles.emitter import Emitter

# Используем глобальный словарь для отслеживания нажатых клавиш (по keycode)
keys = {
    119: False,  # W
     97: False,  # A
    115: False,  # S
    100: False,  # D
     99: False,  # C (спуск вниз)
     32: False,  # SPACE (подъем вверх)
     48: False,  # 0
     49: False,  # 1
     50: False,  # 2
     51: False,  # 3
     52: False,  # 4
     53: False,  # 5
     54: False,  # 6
     55: False,  # 7
     56: False,  # 8
     57: False,  # 9
     45: False,  # -
     61: False,  # =
     91: False,  # [
     93: False,  # ]
}


# Обработка нажатий клавиш
def key_pressed(key, x, y):
    """Обработка нажатий клавиш."""
    global keys
    keycode = ord(key)
    if keycode in keys:
        keys[keycode] = True


# Обработка отпусканий клавиш
def key_released(key, x, y):
    """Обработка отпусканий клавиш."""
    global keys
    keycode = ord(key)
    if keycode == 27:  # ESC
        glutLeaveMainLoop()
        return
    if keycode in keys:
        keys[keycode] = False


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


# Обработка настроек радиуса прозрачности для эмиттера
def handle_emitters_options(emitters: List[Emitter]):
    """
    Переключение наличия следа у частиц:
        - "-" - отключить
        - "=" - включить
    Переключение затухания цвета у частиц:
        - "[" - отключить
        - "]" - включить
    Изменение расстояния, на котором частицы становятся прозрачными:
        - цифры от 0 до 1 - соответствующие значения расстояния
    """
    for emitter in emitters:
        if keys[61]:    # =
            emitter.has_trail = True
        elif keys[45]:    # -
            emitter.has_trail = False

        if keys[93]:    # ]
            emitter.color_fading = True
        elif keys[91]:    # [
            emitter.color_fading = False

        if keys[57]:    # 9
            emitter.set_transparency_radius(9.0)
        elif keys[56]:  # 8
            emitter.set_transparency_radius(8.0)
        elif keys[55]:  # 7
            emitter.set_transparency_radius(7.0)
        elif keys[54]:  # 6
            emitter.set_transparency_radius(6.0)
        elif keys[53]:  # 5
            emitter.set_transparency_radius(5.0)
        elif keys[52]:  # 4
            emitter.set_transparency_radius(4.0)
        elif keys[51]:  # 3
            emitter.set_transparency_radius(3.0)
        elif keys[50]:  # 2
            emitter.set_transparency_radius(2.0)
        elif keys[49]:  # 1
            emitter.set_transparency_radius(1.0)
        elif keys[48]:  # 0
            emitter.set_transparency_radius(0.0)


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
