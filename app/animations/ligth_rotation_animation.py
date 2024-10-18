import math

from app.animations.animation import Animation


class LightRotationAnimation(Animation):
    def __init__(self, light, radius=5.0, speed=30.0):
        """
        light: Источник света (например, экземпляр класса PointLight).
        radius: Радиус круга, по которому будет двигаться свет.
        speed: Скорость вращения в градусах в секунду.
        """
        super().__init__(light)
        self.radius = radius
        self.speed = speed  # Скорость в градусах в секунду
        self.angle = 0.0  # Начальный угол в градусах

    def start(self):
        """Запуск анимации."""
        self.running = True

    def update(self, light, delta_time):
        """Обновление позиции источника света по круговой траектории."""
        if not self.running:
            return

        # Увеличиваем угол на основе времени и скорости вращения
        self.angle += self.speed * delta_time
        self.angle = self.angle % 360  # Ограничиваем угол значением 360°

        # Вычисляем новую позицию источника света
        new_x = self.radius * math.cos(math.radians(self.angle))
        new_z = self.radius * math.sin(math.radians(self.angle))

        # Обновляем позицию света
        light.set_position([new_x, light.position[1], new_z, 1.0])  # w = 1.0 означает позиционный свет
