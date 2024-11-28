# particles/collision.py
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
                    particle.velocity = -particle.velocity
            elif isinstance(obj, Sphere):  # Столкновение с сферой
                if self.check_collision_sphere(particle.position, obj):
                    # Отражение по нормали
                    normal = glm.normalize(particle.position - glm.vec3(*obj.position))
                    particle.velocity = glm.reflect(particle.velocity, normal)
            # Добавьте другие типы объектов и соответствующие проверки

    def check_collision(self, position, obj: Shape):
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

    def check_collision_sphere(self, position, obj: Shape, obj_radius=1.0):
        # Столкновение с сферой: расстояние до центра меньше радиуса
        center = glm.vec3(*obj.position)
        distance = glm.length(position - center)
        return distance <= obj_radius
