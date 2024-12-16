import math
from typing import List

import glm

from lab_kr.particles.particle import Particle
from lab_kr.shapes.shape import Shape
from lab_kr.shapes.cylinder import Cylinder


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
            if isinstance(obj, Cylinder):
                self.apply_force_cylinder(particle, obj)

    def apply_force_cylinder(self, particle: Particle, cylinder: Cylinder):
        """Применяет силу отталкивания от поверхности цилиндра, если частица находится в радиусе действия эффекта."""
        # Матрицы поворота цилиндра
        rotation_matrix = glm.mat4(1.0)
        rotation_matrix = glm.rotate(rotation_matrix, glm.radians(cylinder.rotation[0]), glm.vec3(1.0, 0.0, 0.0))
        rotation_matrix = glm.rotate(rotation_matrix, glm.radians(cylinder.rotation[1]), glm.vec3(0.0, 1.0, 0.0))
        rotation_matrix = glm.rotate(rotation_matrix, glm.radians(cylinder.rotation[2]), glm.vec3(0.0, 0.0, 1.0))

        # Переход частицы в локальную систему цилиндра
        inv_rotation_matrix = glm.inverse(rotation_matrix)
        local_particle_position = glm.vec3(inv_rotation_matrix * glm.vec4(particle.position - cylinder.position, 1.0))

        # Определяем проекцию частицы на ось цилиндра
        clamped_y = glm.clamp(local_particle_position.y, 0.0, cylinder.height)

        # Радиус цилиндра на высоте проекции
        current_radius = glm.mix(cylinder.base_radius, cylinder.top_radius, clamped_y / cylinder.height)

        # Расстояние от частицы до боковой поверхности
        to_axis = glm.vec2(local_particle_position.x, local_particle_position.z)
        distance_to_side_surface = glm.length(to_axis) - current_radius

        # Расстояние до верхнего и нижнего оснований
        distance_to_top = local_particle_position.y - cylinder.height
        distance_to_bottom = -local_particle_position.y

        # Определяем минимальное расстояние до поверхности цилиндра
        if local_particle_position.y > cylinder.height:
            # Частица [...] над верхним основанием
            if distance_to_side_surface > 0.0:
                # где-то сбоку
                distance_to_surface = glm.length(glm.vec2(distance_to_side_surface, distance_to_top))
                surface_normal = glm.vec3(to_axis.x, 1.0, to_axis.y)
            else:
                # ровно
                distance_to_surface = distance_to_top
                surface_normal = glm.vec3(0.0, 1.0, 0.0)
        elif local_particle_position.y < 0.0:
            # Частица [...] под нижним основанием
            if distance_to_side_surface > 0.0:
                # где-то сбоку
                distance_to_surface = glm.length(glm.vec2(distance_to_side_surface, distance_to_bottom))
                surface_normal = glm.vec3(to_axis.x, -1.0, to_axis.y)
            else:
                # ровно
                distance_to_surface = distance_to_bottom
                surface_normal = glm.vec3(0.0, -1.0, 0.0)
        else:
            # Частица где-то сбоку
            distance_to_surface = distance_to_side_surface
            surface_normal = glm.vec3(to_axis.x, 0.0, to_axis.y)

        # Проверяем, находится ли частица в зоне действия эффекта
        if abs(distance_to_surface) > self.range_of_effect:
            return

        # Возвращаем нормаль в мировую систему координат
        world_normal = glm.normalize(glm.vec3(rotation_matrix * glm.vec4(surface_normal, 0.0)))

        # Вычисляем величину силы отталкивания
        force_magnitude = self.calculate_force_magnitude_for_cylinder(particle, distance_to_surface)

        # Применяем силу отталкивания
        particle.velocity += world_normal * force_magnitude

    def calculate_force_magnitude_for_cylinder(self, particle: Particle, distance_to_surface: float):
        """
        Вычисляет величину силы отталкивания в зависимости от расстояния до поверхности цилиндра.
        Используется экспоненциальное затухание для плавного уменьшения силы с расстоянием.
        """
        if abs(distance_to_surface) > self.range_of_effect:
            return 0.0

        # Экспоненциальное затухание: сила затухает плавно по формуле F = e^(-distance^2 / range_of_effect)
        return math.exp(-distance_to_surface ** 2 / self.range_of_effect)
