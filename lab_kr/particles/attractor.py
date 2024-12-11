import math
from typing import List

import glm

from lab3.shapes.shape import Shape
from lab_kr.shapes.point import Point  # Импортируем класс Point
from lab_kr.particles.particle import Particle


class AttractorHandler:
    def __init__(self, objects: List[Shape], range_of_effect: float):
        """
        :param objects: Список объектов, выступающих в роли аттракторов.
        :param range_of_effect: Радиус действия аттрактора.
        """
        self.objects = objects
        self.range_of_effect = range_of_effect

    def apply_attraction(self, particle: Particle):
        """Обрабатывает взаимодействие частицы с аттракторами."""
        for obj in self.objects:
            if isinstance(obj, Point):  # Проверяем, является ли объект точкой
                if self.is_within_range_point(particle.position, obj):
                    self.apply_force_point(particle, obj)

    def apply_force_point(self, particle: Particle, point: Point):
        """Применяет силу притягивания к точке."""
        # Вычисляем направление от частицы к точке
        direction = glm.normalize(glm.vec3(point.position) - particle.position)

        # Вычисляем силу притягивания
        force_magnitude = self.calculate_force_magnitude(particle, point.position)

        # Применяем силу
        particle.velocity += direction * force_magnitude

    def is_within_range_point(self, position: glm.vec3, point: Point):
        """Проверяет, находится ли частица в зоне действия точки."""
        point_position = glm.vec3(*point.position)
        distance = glm.length(position - point_position)
        return distance <= self.range_of_effect

    def calculate_force_magnitude(self, particle: Particle, attractor_position: glm.vec3):
        """
        Вычисляет величину силы притягивания в зависимости от расстояния до аттрактора.
        Используется экспоненциальное затухание для плавного уменьшения силы с расстоянием.
        """
        distance = glm.length(particle.position - attractor_position)
        if distance > self.range_of_effect:
            return 0.0

        # Экспоненциальное затухание: сила затухает плавно по формуле F = e^(-k * distance)
        k = 5.0 / self.range_of_effect  # Коэффициент для настройки скорости затухания
        return math.exp(-k * distance) * 20
