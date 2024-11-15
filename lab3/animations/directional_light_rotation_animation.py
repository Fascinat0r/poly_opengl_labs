# lab3/animations/directional_light_rotation_animation.py
import glm

from lab3.animations.animation import Animation


class DirectionalLightRotationAnimation(Animation):
    def __init__(self, light, axis=[0.0, 1.0, 0.0], speed=30.0):
        """
        :param light: Экземпляр DirectionalLight.
        :param axis: Ось вращения [x, y, z].
        :param speed: Скорость вращения в градусах в секунду.
        """
        super().__init__(light)
        self.axis = glm.normalize(glm.vec3(*axis))
        self.speed = speed  # градусов в секунду
        self.angle = 0.0  # начальный угол в градусах

    def start(self):
        """Запуск анимации."""
        self.running = True

    def update(self, light, delta_time):
        """Обновление направления направленного света путем вращения вокруг оси."""
        if not self.running:
            return

        # Обновляем угол на основе времени и скорости вращения
        self.angle += self.speed * delta_time
        self.angle = self.angle % 360  # Ограничиваем угол значением 360°

        # Текущее направление света
        current_dir = glm.normalize(glm.vec3(*light.direction))

        # Создаём матрицу вращения
        rotation = glm.rotate(glm.mat4(1.0), glm.radians(self.speed * delta_time), self.axis)

        # Применяем вращение к текущему направлению
        new_dir = rotation * glm.vec4(current_dir, 0.0)

        # Обновляем направление света
        light.direction = [new_dir.x, new_dir.y, new_dir.z]
