# particles/emitter.py (продолжение)
import math
import random

import glm

from lab_kr.particles.emitter import Emitter
from lab_kr.particles.particle import Particle


class PlaneEmitter(Emitter):
    def __init__(self, position, emission_rate, max_particles, speed_range, size_range, color, lifetime,
                 width=1.0, height=1.0, max_angle=15.0, plane_normal=(0.0, -1.0, 0.0)):
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
        :param plane_normal: Основное направление нормали плоскости
        """
        super().__init__(position, emission_rate, max_particles)
        self.speed_range = speed_range
        self.size_range = size_range
        self.color = glm.vec4(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, color[3] / 255.0)
        self.lifetime = lifetime
        self.width = width
        self.height = height
        self.max_angle = math.radians(max_angle)
        self.plane_normal = glm.normalize(glm.vec3(*plane_normal))

    def emit_particle(self):
        # Случайная позиция частицы в пределах плоскости
        x_offset = random.uniform(-self.width / 2, self.width / 2)
        z_offset = random.uniform(-self.height / 2, self.height / 2)
        position = self.position + glm.vec3(x_offset, 0.0, z_offset)

        # Генерация случайного направления в пределах конуса отклонения
        random_angle = random.uniform(0, self.max_angle)
        random_azimuth = random.uniform(0, 2 * math.pi)

        # Переход к локальным координатам
        perpendicular1 = glm.cross(self.plane_normal, glm.vec3(1.0, 0.0, 0.0))
        if glm.length(perpendicular1) < 1e-6:
            perpendicular1 = glm.cross(self.plane_normal, glm.vec3(0.0, 0.0, 1.0))
        perpendicular1 = glm.normalize(perpendicular1)

        perpendicular2 = glm.cross(self.plane_normal, perpendicular1)
        perpendicular2 = glm.normalize(perpendicular2)

        direction = (
            glm.normalize(self.plane_normal * math.cos(random_angle) +
                          perpendicular1 * math.sin(random_angle) * math.cos(random_azimuth) +
                          perpendicular2 * math.sin(random_angle) * math.sin(random_azimuth))
        )

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
