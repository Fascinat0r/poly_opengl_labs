import math


class Camera:
    def __init__(self, position, up, yaw, pitch):
        self.position = position  # Позиция камеры (x, y, z)
        self.up = up  # Вектор "вверх" для камеры
        self.front = [0.0, 0.0, -1.0]  # Вектор "вперед" камеры
        self.right = [1.0, 0.0, 0.0]  # Вектор "вправо"

        self.yaw = yaw  # Угол поворота по горизонтали (в градусах)
        self.pitch = pitch  # Угол наклона по вертикали (в градусах)
        self.speed = 0.1  # Скорость движения камеры
        self.sensitivity = 0.1  # Чувствительность мыши

        self.update_camera_vectors()

    def update_camera_vectors(self):
        """Обновляем векторы направления камеры на основе углов поворота."""
        front = [
            math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
            math.sin(math.radians(self.pitch)),
            math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        ]
        self.front = self.normalize(front)
        self.right = self.normalize(self.cross(self.front, self.up))  # Перпендикулярно фронту и вектору вверх

    def normalize(self, vec):
        """Нормализуем вектор."""
        length = math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
        return [vec[0] / length, vec[1] / length, vec[2] / length]

    def cross(self, v1, v2):
        """Вычисляем векторное произведение."""
        return [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        ]

    def move_forward(self):
        """Движение вперед по направлению взгляда."""
        self.position[0] += self.front[0] * self.speed
        self.position[1] += self.front[1] * self.speed
        self.position[2] += self.front[2] * self.speed

    def move_backward(self):
        """Движение назад."""
        self.position[0] -= self.front[0] * self.speed
        self.position[1] -= self.front[1] * self.speed
        self.position[2] -= self.front[2] * self.speed

    def move_left(self):
        """Движение влево."""
        self.position[0] -= self.right[0] * self.speed
        self.position[1] -= self.right[1] * self.speed
        self.position[2] -= self.right[2] * self.speed

    def move_right(self):
        """Движение вправо."""
        self.position[0] += self.right[0] * self.speed
        self.position[1] += self.right[1] * self.speed
        self.position[2] += self.right[2] * self.speed

    def rotate(self, x_offset, y_offset):
        """Вращаем камеру с помощью мыши."""
        self.yaw += x_offset * self.sensitivity
        self.pitch += y_offset * self.sensitivity

        # Ограничиваем наклон, чтобы избежать переворота камеры
        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        self.update_camera_vectors()

    def get_view_matrix(self):
        """Возвращаем матрицу вида для камеры."""
        target = [
            self.position[0] + self.front[0],
            self.position[1] + self.front[1],
            self.position[2] + self.front[2]
        ]
        return self.position, target, self.up
