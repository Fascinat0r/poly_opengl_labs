import math


class Camera:
    def __init__(self, position, up, yaw, pitch):
        self.position = position  # Позиция камеры
        self.up = up  # Вектор "вверх"
        self.front = [0.0, 0.0, -1.0]  # Вектор, куда направлена камера (по умолчанию)
        self.right = [1.0, 0.0, 0.0]  # Вектор "вправо"
        self.yaw = yaw  # Угол поворота вокруг вертикальной оси (Y)
        self.pitch = pitch  # Угол наклона камеры (вверх/вниз)
        self.speed = 0.05  # Скорость перемещения камеры
        self.sensitivity = 0.1  # Чувствительность к движению мыши

        # Вычисляем начальные векторы на основе углов yaw и pitch
        self.update_camera_vectors()


    def move_forward(self):
        """Двигает камеру вперёд."""
        self.position[0] += self.front[0] * self.speed
        self.position[1] += self.front[1] * self.speed
        self.position[2] += self.front[2] * self.speed

    def move_backward(self):
        """Двигает камеру назад."""
        self.position[0] -= self.front[0] * self.speed
        self.position[1] -= self.front[1] * self.speed
        self.position[2] -= self.front[2] * self.speed

    def move_left(self):
        """Двигает камеру влево."""
        self.position[0] -= self.right[0] * self.speed
        self.position[1] -= self.right[1] * self.speed
        self.position[2] -= self.right[2] * self.speed

    def move_right(self):
        """Двигает камеру вправо."""
        self.position[0] += self.right[0] * self.speed
        self.position[1] += self.right[1] * self.speed
        self.position[2] += self.right[2] * self.speed

    def move_up(self):
        """Поднимает камеру вверх."""
        self.position[1] += self.speed

    def move_down(self):
        """Опускает камеру вниз."""
        self.position[1] -= self.speed

    def rotate(self, x_offset, y_offset):
        """Вращает камеру при движении мыши."""
        self.yaw += x_offset * self.sensitivity
        self.pitch += y_offset * self.sensitivity

        # Ограничение наклона камеры
        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        # Пересчёт фронтального вектора камеры
        self.update_camera_vectors()

    def update_camera_vectors(self):
        """Обновляет векторы front и right камеры, сохраняя горизонт."""
        # Обновляем вектор front на основе углов yaw и pitch
        front_x = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        front_y = math.sin(math.radians(self.pitch))
        front_z = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        self.front = [front_x, front_y, front_z]

        # Нормализуем вектор front
        self.front = self.normalize(self.front)

        # Пересчитываем вектор right как векторное произведение front и фиксированного вектора up (0, 1, 0)
        # Это позволяет сохранять вертикальный вектор "вверх" (ось Y)
        self.right = self.cross_product(self.front, [0.0, 1.0, 0.0])
        self.right = self.normalize(self.right)

        # Вектор up остаётся фиксированным как ось Y, потому что мы хотим "держать горизонт"
        self.up = [0.0, 1.0, 0.0]

    @staticmethod
    def normalize(vec):
        """Нормализует вектор."""
        length = math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
        return [vec[0] / length, vec[1] / length, vec[2] / length]

    @staticmethod
    def cross_product(v1, v2):
        """Вычисляет векторное произведение двух векторов."""
        return [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        ]

    def get_view_matrix(self):
        """Возвращает параметры камеры для gluLookAt."""
        # Позиция, куда направлен взгляд камеры (по направлению вектора front)
        target = [
            self.position[0] + self.front[0],
            self.position[1] + self.front[1],
            self.position[2] + self.front[2]
        ]
        return self.position, target, self.up
