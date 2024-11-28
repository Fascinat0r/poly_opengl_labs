# particles/emitter.py (продолжение)
import math
import random

import glm

from lab_kr.particles.emitter import Emitter
from lab_kr.particles.particle import Particle


class PlaneEmitter(Emitter):
    def __init__(self, position, emission_rate, max_particles, speed_range, size_range, color, lifetime,
                 width=1.0, height=1.0):
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
        """
        super().__init__(position, emission_rate, max_particles)
        self.speed_range = speed_range
        self.size_range = size_range
        self.color = color
        self.lifetime = lifetime
        self.width = width
        self.height = height

    def emit_particle(self):
        # Случайная позиция частицы в пределах прямоугольника
        x_offset = random.uniform(-self.width / 2, self.width / 2)
        y_offset = random.uniform(-self.height / 2, self.height / 2)
        position = self.position + glm.vec3(x_offset, 0.0, y_offset)

        # Начальная скорость увеличивается с удалением от эмиттера (обязательный параметр)
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, 1)
        direction = glm.vec3(math.cos(angle), 1.0, math.sin(angle))
        speed = self.speed_range[0] + self.speed_range[1] * distance
        velocity = glm.normalize(direction) * speed

        size = random.uniform(self.size_range[0], self.size_range[1])

        return Particle(
            position=position,
            velocity=velocity,
            size=size,
            color=self.color,
            lifetime=self.lifetime,
            has_trail=False
        )
