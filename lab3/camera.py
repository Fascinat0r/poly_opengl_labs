# camera.py
import math

import glm


class Camera:
    def __init__(self, position, up, yaw, pitch, zoom=45.0, aspect_ratio=4 / 3):
        self.position = glm.vec3(*position)  # Позиция камеры
        self.up = glm.vec3(*up)  # Вектор "вверх"
        self.front = glm.vec3(0.0, 0.0, -1.0)  # Вектор, куда направлена камера (по умолчанию)
        self.right = glm.vec3(1.0, 0.0, 0.0)  # Вектор "вправо"
        self.world_up = glm.vec3(*up)  # Мировой вектор "вверх"

        self.yaw = yaw  # Угол поворота вокруг вертикальной оси (Y)
        self.pitch = pitch  # Угол наклона камеры (вверх/вниз)
        self.speed = 5.0  # Скорость перемещения камеры
        self.sensitivity = 0.1  # Чувствительность к движению мыши
        self.zoom = zoom  # Угол обзора
        self.max_zoom = zoom
        self.aspect_ratio = aspect_ratio  # Соотношение сторон

        # Вычисляем начальные векторы на основе углов yaw и pitch
        self.update_camera_vectors()

    def get_view_matrix(self):
        """Возвращает матрицу вида камеры."""
        return glm.lookAt(self.position, self.position + self.front, self.up)

    def get_projection_matrix(self):
        """Возвращает матрицу проекции камеры."""
        return glm.perspective(glm.radians(self.zoom), 1, 0.1, 100.0)

    def process_keyboard(self, direction, delta_time):
        """Обрабатывает ввод с клавиатуры для перемещения камеры."""
        velocity = self.speed * delta_time
        if direction == "FORWARD":
            self.position += self.front * velocity
        if direction == "BACKWARD":
            self.position -= self.front * velocity
        if direction == "LEFT":
            self.position -= self.right * velocity
        if direction == "RIGHT":
            self.position += self.right * velocity
        if direction == "UP":
            self.position += self.world_up * velocity
        if direction == "DOWN":
            self.position -= self.world_up * velocity

    def process_mouse_movement(self, x_offset, y_offset, constrain_pitch=True):
        """Обрабатывает движение мыши для вращения камеры."""
        x_offset *= self.sensitivity
        y_offset *= self.sensitivity

        self.yaw += x_offset
        self.pitch += y_offset

        # Ограничение наклона камеры
        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

        # Обновляем векторы камеры
        self.update_camera_vectors()

    def process_mouse_scroll(self, y_offset):
        """Обрабатывает прокрутку мыши для изменения угла обзора."""
        self.zoom -= y_offset
        if self.zoom < 1.0:
            self.zoom = 1.0
        if self.zoom > self.max_zoom:
            self.zoom = self.max_zoom

    def update_camera_vectors(self):
        """Обновляет векторы front, right и up камеры."""
        front = glm.vec3()
        front.x = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        front.y = math.sin(math.radians(self.pitch))
        front.z = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        self.front = glm.normalize(front)
        self.right = glm.normalize(glm.cross(self.front, self.world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))
