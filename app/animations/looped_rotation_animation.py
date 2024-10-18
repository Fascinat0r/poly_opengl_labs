from app.animations.animation import Animation


class LoopedRotationAnimation(Animation):
    def __init__(self, target_object, start_angles, end_angles, speeds, oscillate=True, tolerance=0.1):
        super().__init__(target_object)
        self.start_angles = start_angles  # Начальные углы вращения [x, y, z]
        self.end_angles = end_angles  # Конечные углы вращения [x, y, z]
        self.speeds = speeds  # Скорости вращения по каждой оси [x_speed, y_speed, z_speed]
        self.oscillate = oscillate  # Булевая переменная для зацикленного вращения
        self.tolerance = tolerance  # Допустимая погрешность для достижения углов

        # Текущие углы и направление вращения
        self.current_angles = list(start_angles)

        # Направления изменения углов, всегда определяются начальным и конечным углом
        self.directions = [1 if end > start else -1 for start, end in zip(start_angles, end_angles)]

        # Стадия анимации: True - движемся вперед (к end_angles), False - движемся назад (к start_angles)
        self.moving_forward = True

    def start(self):
        """Запуск анимации."""
        self.running = True

    def update(self, shape):
        """Обновление углов вращения объекта."""
        if not self.running:
            return

        # Обновляем углы вращения по каждой оси
        for i in range(3):
            # Определяем направление вращения на основе стадии анимации
            direction = self.directions[i] if self.moving_forward else -self.directions[i]

            # Обновляем текущие углы с учетом направления
            self.current_angles[i] += direction * self.speeds[i]

            # Проверка на достижение конечного угла с учетом направления вращения
            if self.moving_forward:  # Движемся вперед (к конечным углам)
                if (self.directions[i] == 1 and self.current_angles[i] >= self.end_angles[i]) or \
                        (self.directions[i] == -1 and self.current_angles[i] <= self.end_angles[i]):
                    self.current_angles[i] = self.end_angles[i]
            else:  # Движемся назад (к начальным углам)
                if (self.directions[i] == 1 and self.current_angles[i] <= self.start_angles[i]) or \
                        (self.directions[i] == -1 and self.current_angles[i] >= self.start_angles[i]):
                    self.current_angles[i] = self.start_angles[i]

        # Если зацикливание анимации включено, проверяем и изменяем стадию анимации
        if self.oscillate:
            if self.moving_forward and all(
                    abs(self.current_angles[i] - self.end_angles[i]) <= self.tolerance for i in range(3)):
                # Если достигли конечных углов, начинаем двигаться назад
                self.moving_forward = False
            elif not self.moving_forward and all(
                    abs(self.current_angles[i] - self.start_angles[i]) <= self.tolerance for i in range(3)):
                # Если вернулись к начальным углам, начинаем двигаться вперед
                self.moving_forward = True

        # Применяем текущие углы вращения к объекту
        shape.rotation = list(self.current_angles)
