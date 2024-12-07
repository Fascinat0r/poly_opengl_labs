import math
from typing import List

import glm

from lab3.shapes.shape import Shape
from lab_kr.particles.particle import Particle
from lab_kr.shapes.plane import Plane


class AntiAttractorHandler:
    def __init__(self, objects: List[Shape], range_of_effect: float):
        """
        :param objects: Список объектов, выступающих в роли анти-аттракторов.
        :param range_of_effect: Радиус действия анти-аттрактора.
        """
        self.objects = objects
        self.range_of_effect = range_of_effect

    def apply_anti_attraction(self, particle: Particle):
        """Обрабатывает взаимодействие частицы с анти-аттракторами."""
        for obj in self.objects:
            if isinstance(obj, Plane):
                if self.is_within_range_plane(particle.position, obj):
                    self.apply_force_plane(particle, obj)

    def apply_force_plane(self, particle: Particle, plane: Plane):
        """Применяет силу отталкивания от плоскости."""
        # Вычисляем матрицу поворота на основе углов плоскости
        rotation_matrix = glm.mat4(1.0)
        rotation_matrix = glm.rotate(rotation_matrix, glm.radians(plane.rotation[0]), glm.vec3(1, 0, 0))  # Поворот по X
        rotation_matrix = glm.rotate(rotation_matrix, glm.radians(plane.rotation[1]), glm.vec3(0, 1, 0))  # Поворот по Y
        rotation_matrix = glm.rotate(rotation_matrix, glm.radians(plane.rotation[2]), glm.vec3(0, 0, 1))  # Поворот по Z

        # Базовая нормаль для плоскости (Y-вверх)
        base_normal = glm.vec3(0.0, 1.0, 0.0)

        # Применяем матрицу поворота к базовой нормали
        normal = glm.normalize(glm.vec3(rotation_matrix * glm.vec4(base_normal, 0.0)))

        # Определяем, с какой стороны частица относительно плоскости
        plane_to_particle = glm.vec3(particle.position - glm.vec3(*plane.position))
        direction_multiplier = 1.0 if glm.dot(plane_to_particle, normal) > 0 else -1.0

        # Вычисляем силу отталкивания
        force_magnitude = self.calculate_force_magnitude(particle, plane.position)

        # Применяем силу с учётом стороны
        particle.velocity += normal * force_magnitude * direction_multiplier

    def is_within_range_plane(self, position: glm.vec3, plane: Plane):
        """Проверяет, находится ли частица в зоне действия плоскости."""
        plane_position = glm.vec3(*plane.position)
        distance = glm.length(position - plane_position)
        return distance <= self.range_of_effect

    def calculate_force_magnitude(self, particle: Particle, attractor_position: glm.vec3):
        """
        Вычисляет величину силы отталкивания в зависимости от расстояния до анти-аттрактора.
        Используется экспоненциальное затухание для плавного уменьшения силы с расстоянием.
        """
        distance = glm.length(particle.position - attractor_position)
        if distance > self.range_of_effect:
            return 0.0

        # Экспоненциальное затухание: сила затухает плавно по формуле F = e^(-k * distance)
        k = 5.0 / self.range_of_effect  # Коэффициент для настройки скорости затухания
        return math.exp(-k * distance)

