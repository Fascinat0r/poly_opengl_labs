from lab1.animations.animation import Animation
from lab1.shapes.shape import Shape


class LoopedScaleAnimation(Animation):
    def __init__(self, target_object: Shape, start_scale: float, end_scale: float, speed: float, oscillate=True,
                 tolerance=0.01):
        super().__init__(target_object)
        self.start_scale = start_scale  # Начальный масштаб
        self.end_scale = end_scale  # Конечный масштаб
        self.speed = speed  # Скорости изменения масштаба по каждой оси [x_speed, y_speed, z_speed]
        self.oscillate = oscillate  # Булевая переменная для зацикленной анимации
        self.tolerance = tolerance  # Допустимая погрешность для достижения масштабов

        # Текущий масштаб и направление изменения масштаба
        self.current_scale = start_scale
        # Направления изменения масштаба, всегда определяются начальным и конечным масштабом
        self.direction = 1 if end_scale > start_scale else -1

        self.moving_back = False

    def start(self):
        """Запуск анимации."""
        self.running = True

    def update(self, shape, delta_time):
        """Обновление масштаба объекта."""
        if not self.running:
            return

        # Определяем направление изменения масштаба на основе стадии анимации
        direction = self.direction if self.moving_back else -self.direction

        # Обновляем текущие масштабы с учетом направления
        self.current_scale += direction * abs(self.speed * delta_time)

        if self.moving_back:
            if (self.direction == 1 and self.current_scale >= self.end_scale) or \
                    (self.direction == -1 and self.current_scale <= self.end_scale):
                self.current_scale = self.end_scale
        else:
            if (self.direction == 1 and self.current_scale <= self.start_scale) or \
                    (self.direction == -1 and self.current_scale >= self.start_scale):
                self.current_scale = self.start_scale

        # Если зацикливание анимации включено, проверяем и изменяем стадию анимации
        if self.oscillate:
            if self.moving_back and all(
                    abs(self.current_scale - self.end_scale) <= self.tolerance for i in range(3)):
                self.moving_back = False
            elif not self.moving_back and all(
                    abs(self.current_scale - self.start_scale) <= self.tolerance for i in range(3)):
                self.moving_back = True

        # Применяем текущие масштабы к объекту
        shape.scale = self.current_scale

    def stop(self):
        """Остановка анимации."""
        self.running = False
