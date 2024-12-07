import glm

from lab3.shapes.shape import Shape
from lab_kr.shapes.cube import Cube
from lab_kr.shapes.sphere import Sphere


class CollisionHandler:
    def __init__(self, scene):
        self.scene = scene

    def handle_collisions(self, particle):
        for obj in self.scene.objects:
            if isinstance(obj, Cube):  # Столкновение с кубом
                if self.check_collision(particle.position, obj):
                    # Изменяем направление движения на противоположное
                    self.handle_collision_cube(particle, obj)
            elif isinstance(obj, Sphere):  # Столкновение с сферой
                if self.check_collision_sphere(particle.position, obj):
                    # Отражение по нормали
                    self.handle_collision_sphere(particle, obj)

    @staticmethod
    def handle_collision_cube(particle, obj: Cube):
        # Определение нормали поверхности в зависимости от столкновенной грани
        half_scale = obj.scale / 2
        min_bound = glm.vec3(obj.position[0] - half_scale, obj.position[1] - half_scale, obj.position[2] - half_scale)
        max_bound = glm.vec3(obj.position[0] + half_scale, obj.position[1] + half_scale, obj.position[2] + half_scale)

        # Вычисление нормали для каждой из граней куба
        normal = glm.vec3(0.0, 0.0, 0.0)
        if abs(particle.position.x - min_bound.x) < 0.1:
            normal = glm.vec3(-1.0, 0.0, 0.0)
        elif abs(particle.position.x - max_bound.x) < 0.1:
            normal = glm.vec3(1.0, 0.0, 0.0)
        elif abs(particle.position.y - min_bound.y) < 0.1:
            normal = glm.vec3(0.0, -1.0, 0.0)
        elif abs(particle.position.y - max_bound.y) < 0.1:
            normal = glm.vec3(0.0, 1.0, 0.0)
        elif abs(particle.position.z - min_bound.z) < 0.1:
            normal = glm.vec3(0.0, 0.0, -1.0)
        elif abs(particle.position.z - max_bound.z) < 0.1:
            normal = glm.vec3(0.0, 0.0, 1.0)

        # Отражение скорости
        particle.velocity = glm.reflect(particle.velocity, normal)

    @staticmethod
    def handle_collision_sphere(particle, obj: Sphere):
        # Нормаль для столкновения с сферой
        center = glm.vec3(*obj.position)
        normal = glm.normalize(particle.position - center)

        # Отражение по нормали
        particle.velocity = glm.reflect(particle.velocity, normal)

    @staticmethod
    def check_collision(position, obj: Shape):
        # Простейшая AABB коллизия с кубом
        half_scale = obj.scale / 2
        min_bound = glm.vec3(obj.position[0] - half_scale,
                             obj.position[1] - half_scale,
                             obj.position[2] - half_scale)
        max_bound = glm.vec3(obj.position[0] + half_scale,
                             obj.position[1] + half_scale,
                             obj.position[2] + half_scale)
        return (min_bound.x <= position.x <= max_bound.x and
                min_bound.y <= position.y <= max_bound.y and
                min_bound.z <= position.z <= max_bound.z)

    @staticmethod
    def check_collision_sphere(position, obj: Shape, obj_radius=1.0):
        # Столкновение с сферой: расстояние до центра меньше радиуса
        center = glm.vec3(*obj.position)
        distance = glm.length(position - center)
        return distance <= obj_radius
