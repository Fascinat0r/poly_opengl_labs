# particles/emitter.py (продолжение)
import math
import random

import glm

from lab_kr.particles.emitter import Emitter
from lab_kr.particles.particle import Particle


class PlaneEmitter(Emitter):
    def __init__(self, position, emission_rate, max_particles, speed_range, size_range, color, lifetime,
                 width=1.0, height=1.0, max_angle=15.0):
        """
        :param position: Позиция эмиттера
        :param emission_rate: Скорость эмиссии
        :param max_particles: Максимальное количество частиц
        :param speed_range: Диапазон скорости
        :param size_range: Диапазон размеров частиц
        :param color: Цвет частиц
        :param lifetime: Время жизни частиц
        :param width: Ширина области эмиттера
        :param height: Высота области эмиттера
        :param max_angle: Максимальный угол отклонения от нормали (в градусах)
        """
        super().__init__(position, emission_rate, max_particles)
        self.speed_range = speed_range
        self.size_range = size_range
        # Нормализуем цвет, если он задан в диапазоне [0, 255]
        self.color = glm.vec4(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, color[3] / 255.0)
        self.lifetime = lifetime
        self.width = width
        self.height = height
        self.max_angle = math.radians(max_angle)  # Конвертируем в радианы

    def emit_particle(self):
        # Случайная позиция частицы в пределах прямоугольника
        x_offset = random.uniform(-self.width / 2, self.width / 2)
        z_offset = random.uniform(-self.height / 2, self.height / 2)
        position = self.position + glm.vec3(x_offset, 0.0, z_offset)

        # Направление: нормаль плюс случайное отклонение
        normal = glm.vec3(0.0, 1.0, 0.0)  # Нормаль плоскости
        angle_offset = random.uniform(0, self.max_angle)
        angle_azimuth = random.uniform(0, 2 * math.pi)

        # Отклонение нормали в случайном направлении
        random_dir = glm.vec3(
            math.sin(angle_offset) * math.cos(angle_azimuth),
            math.cos(angle_offset),
            math.sin(angle_offset) * math.sin(angle_azimuth)
        )
        direction = glm.normalize(normal + random_dir)

        # Случайная скорость
        speed = random.uniform(self.speed_range[0], self.speed_range[1])
        velocity = direction * speed

        # Случайный размер
        size = random.uniform(self.size_range[0], self.size_range[1])

        return Particle(
            position=position,
            velocity=velocity,
            size=size,
            color=self.color,
            lifetime=self.lifetime,
            has_trail=False
        )
