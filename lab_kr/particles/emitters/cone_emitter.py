import math
import random

import glm

from lab_kr.particles.emitter import Emitter
from lab_kr.particles.particle import Particle


class ConeEmitter(Emitter):
    def __init__(self, position, emission_rate, max_particles, speed_range, size_range, color, lifetime,
                 base_radius, height, rotation=[0.0, 0.0, 0.0]):
        """
        Конусный эмиттер генерирует частицы с поверхности конуса.

        :param position: Позиция вершины конуса.
        :param emission_rate: Скорость генерации частиц.
        :param max_particles: Максимальное количество частиц.
        :param speed_range: Диапазон скорости (min_speed, max_speed).
        :param size_range: Диапазон размеров (min_size, max_size).
        :param color: Цвет частиц в формате [R, G, B, A].
        :param lifetime: Время жизни частицы.
        :param base_radius: Радиус основания конуса.
        :param height: Высота конуса.
        :param rotation: Вращение конуса (углы Эйлера в градусах).
        """
        super().__init__(position, emission_rate, max_particles, acceleration=[0,0,0])
        self.speed_range = speed_range
        self.size_range = size_range
        self.color = glm.vec4(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, color[3] / 255.0)
        self.lifetime = lifetime
        self.base_radius = base_radius
        self.height = height
        self.rotation = rotation

        # Создаем матрицу модели для учета положения и поворота
        self.model_matrix = self.calculate_model_matrix()

    def calculate_model_matrix(self):
        """Вычисляет матрицу модели для эмиттера."""
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(*self.position))
        model = glm.rotate(model, glm.radians(self.rotation[0]), glm.vec3(1.0, 0.0, 0.0))
        model = glm.rotate(model, glm.radians(self.rotation[1]), glm.vec3(0.0, 1.0, 0.0))
        model = glm.rotate(model, glm.radians(self.rotation[2]), glm.vec3(0.0, 0.0, 1.0))
        return model

    def emit_particle(self):
        # Случайная позиция на боковой поверхности конуса
        theta = random.uniform(0, 2 * math.pi)  # Угол по окружности
        h = random.uniform(0, self.height)  # Случайная высота вдоль оси конуса

        # Радиус уменьшается с высотой
        r_local = self.base_radius * (1 - h / self.height)

        # Координаты точки на поверхности конуса (в локальной системе координат)
        local_position = glm.vec3(r_local * math.cos(theta), h, r_local * math.sin(theta))

        # Применяем матрицу модели, чтобы учесть смещение и поворот
        world_position = glm.vec3(self.model_matrix * glm.vec4(local_position, 1.0))

        # Нормаль на боковой поверхности (в локальной системе координат)
        local_normal = glm.vec3(
            self.height * math.cos(theta),  # X радиальная составляющая
            self.base_radius,  # Y наклонная составляющая (вверх)
            self.height * math.sin(theta)  # Z радиальная составляющая
        )
        local_normal = glm.normalize(local_normal)  # Нормализуем

        # Применяем матрицу модели для нормали (без смещения)
        world_normal = glm.normalize(glm.mat3(self.model_matrix) * local_normal)

        # Направление частицы — вдоль нормали
        direction = world_normal

        # Генерация случайной скорости
        speed = random.uniform(self.speed_range[0], self.speed_range[1])
        velocity = direction * speed

        # Генерация случайного размера частицы
        size = random.uniform(self.size_range[0], self.size_range[1])

        return Particle(
            position=world_position,
            velocity=velocity,
            size=size,
            color=self.color,
            lifetime=self.lifetime,
            has_trail=True
        )
