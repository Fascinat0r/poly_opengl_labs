# particles/emitters/cone_emitter.py
import math
import random

import glm

from lab_kr.particles.emitter import Emitter
from lab_kr.particles.particle import Particle


class ConeEmitter(Emitter):
    def __init__(self, position, emission_rate, max_particles, speed_range, size_range, color, lifetime,
                 main_direction=None, max_angle=15.0):
        """
        :param position: Позиция эмиттера
        :param emission_rate: Частота эмиссии
        :param max_particles: Максимальное количество частиц
        :param speed_range: Диапазон скорости частиц (min_speed, max_speed)
        :param size_range: Диапазон размеров частиц (min_size, max_size)
        :param color: Цвет частиц (RGBA)
        :param lifetime: Время жизни частиц
        :param main_direction: Основное направление конуса
        :param max_angle: Максимальный угол отклонения от основного направления (в градусах)
        """
        super().__init__(position, emission_rate, max_particles)
        if main_direction is None:
            main_direction = [0.5, 0.5, 0.5]
        self.speed_range = speed_range
        self.size_range = size_range
        self.color = glm.vec4(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, color[3] / 255.0)
        self.lifetime = lifetime
        self.main_direction = glm.normalize(glm.vec3(*main_direction))
        self.max_angle = math.radians(max_angle)  # Преобразуем угол в радианы

    def emit_particle(self):
        # Генерация случайного отклонения внутри конуса
        angle_offset = random.uniform(0, self.max_angle)
        angle_azimuth = random.uniform(0, 2 * math.pi)

        # Вектор отклонения
        deviation = glm.vec3(
            math.sin(angle_offset) * math.cos(angle_azimuth),
            math.cos(angle_offset),
            math.sin(angle_offset) * math.sin(angle_azimuth)
        )

        # Направление частицы = основное направление + отклонение
        direction = glm.normalize(self.main_direction + deviation)

        # Случайная скорость
        speed = random.uniform(self.speed_range[0], self.speed_range[1])
        velocity = direction * speed

        # Случайный размер частицы
        size = random.uniform(self.size_range[0], self.size_range[1])

        return Particle(
            position=self.position,
            velocity=velocity,
            size=size,
            color=self.color,
            lifetime=self.lifetime,
            has_trail=False
        )
