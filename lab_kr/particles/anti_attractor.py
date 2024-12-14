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
                if self.is_within_range_cylinder(particle.position, obj):
                    self.apply_force_cylinder(particle, obj)

    def is_within_range_cylinder(self, position: glm.vec3, cylinder: Cylinder):
        """Проверяет, находится ли частица в зоне действия цилиндра с учётом его поворота и радиусов оснований."""
        # Матрицы поворота
        rot_x = glm.rotate(glm.mat4(1.0), glm.radians(cylinder.rotation[0]), glm.vec3(1, 0, 0))
        rot_y = glm.rotate(glm.mat4(1.0), glm.radians(cylinder.rotation[1]), glm.vec3(0, 1, 0))
        rot_z = glm.rotate(glm.mat4(1.0), glm.radians(cylinder.rotation[2]), glm.vec3(0, 0, 1))

        # Итоговая матрица поворота
        rotation_matrix = rot_z * rot_y * rot_x

        # Преобразуем позицию частицы в локальную систему координат цилиндра
        inv_rotation_matrix = glm.inverse(rotation_matrix)
        local_position = glm.vec3(inv_rotation_matrix * glm.vec4(position - cylinder.position, 1.0))

        # Вектор от основания цилиндра к частице в локальной системе координат
        to_particle = local_position - glm.vec3(0, 0, 0)

        # Проекция частицы на ось цилиндра (вдоль локальной Y)
        projected_y = glm.dot(to_particle, glm.vec3(0, 1, 0))  # Скалярное произведение
        clamped_y = glm.clamp(projected_y, 0, cylinder.height)  # Ограничиваем проекцию высотой цилиндра

        # Находим радиус цилиндра на высоте проекции
        current_radius = glm.mix(cylinder.base_radius, cylinder.top_radius, clamped_y / cylinder.height)

        # Находим ближайшую точку на оси цилиндра
        closest_point = glm.vec3(0, clamped_y, 0)

        # Расстояние от частицы до ближайшей точки на оси цилиндра
        distance_to_axis = glm.length(local_position - closest_point)

        # Проверяем, находится ли частица в зоне действия
        return distance_to_axis <= current_radius + self.range_of_effect

    def apply_force_cylinder(self, particle: Particle, cylinder: Cylinder):
        """Применяет силу отталкивания от поверхности цилиндра."""
        # Матрицы поворота цилиндра
        rotation_matrix = glm.mat4(1.0)
        rotation_matrix = glm.rotate(rotation_matrix, glm.radians(cylinder.rotation[0]), glm.vec3(1, 0, 0))
        rotation_matrix = glm.rotate(rotation_matrix, glm.radians(cylinder.rotation[1]), glm.vec3(0, 1, 0))
        rotation_matrix = glm.rotate(rotation_matrix, glm.radians(cylinder.rotation[2]), glm.vec3(0, 0, 1))

        # Переход частицы в локальную систему цилиндра
        inv_rotation_matrix = glm.inverse(rotation_matrix)
        local_particle_position = glm.vec3(inv_rotation_matrix * glm.vec4(particle.position - cylinder.position, 1.0))

        # Определяем проекцию частицы на ось цилиндра
        projection_y = glm.clamp(local_particle_position.y, 0, cylinder.height)
        projected_point = glm.vec3(0, projection_y, 0)

        # Радиус цилиндра на высоте проекции
        current_radius = glm.mix(cylinder.base_radius, cylinder.top_radius, projection_y / cylinder.height)

        # Расстояние от частицы до боковой поверхности
        to_axis = glm.vec2(local_particle_position.x, local_particle_position.z)
        distance_to_side_surface = glm.length(to_axis) - current_radius

        # Расстояние до верхнего и нижнего оснований
        distance_to_top = local_particle_position.y - cylinder.height
        distance_to_bottom = local_particle_position.y

        # Определяем минимальное расстояние до поверхности цилиндра
        if local_particle_position.y > cylinder.height:
            # Частица над верхним основанием
            distance_to_surface = distance_to_top
            surface_normal = glm.vec3(0, 1, 0)
        elif local_particle_position.y < 0:
            # Частица под нижним основанием
            distance_to_surface = distance_to_bottom
            surface_normal = glm.vec3(0, -1, 0)
        else:
            # Частица сбоку
            distance_to_surface = distance_to_side_surface
            surface_normal = glm.normalize(glm.vec3(to_axis.x, 0, to_axis.y))

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
