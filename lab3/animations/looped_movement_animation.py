from lab3.animations.animation import Animation


class LoopedMovementAnimation(Animation):
    def __init__(self, target_object, start_position, end_position, speeds, oscillate=True, tolerance=0.1):
        super().__init__(target_object)
        self.start_position = start_position  # Начальная позиция [x, y, z]
        self.end_position = end_position  # Конечная позиция [x, y, z]
        self.speeds = speeds  # Скорости перемещения по каждой оси [x_speed, y_speed, z_speed]
        self.oscillate = oscillate  # Булевая переменная для зацикленного движения
        self.tolerance = tolerance  # Допустимая погрешность для достижения позиций

        # Текущая позиция
        self.current_position = list(start_position)

        # Направления движения по каждой оси (вперед или назад)
        self.directions = [1 if end > start else -1 for start, end in zip(start_position, end_position)]

        # Стадия анимации: True - движемся вперед (к end_position), False - движемся назад (к start_position)
        self.moving_forward = True

    def start(self):
        """Запуск анимации."""
        self.running = True

    def update(self, shape, delta_time):
        """Обновление позиции объекта."""
        if not self.running:
            return

        # Обновляем позицию по каждой оси
        for i in range(3):
            # Определяем направление движения на основе стадии анимации
            direction = self.directions[i] if self.moving_forward else -self.directions[i]

            # Обновляем текущие координаты с учетом направления
            self.current_position[i] += direction * abs(self.speeds[i] * delta_time)

            # Проверка на достижение конечной позиции
            if self.moving_forward:  # Движемся вперед (к end_position)
                if (self.directions[i] == 1 and self.current_position[i] >= self.end_position[i]) or \
                        (self.directions[i] == -1 and self.current_position[i] <= self.end_position[i]):
                    self.current_position[i] = self.end_position[i]
            else:  # Движемся назад (к start_position)
                if (self.directions[i] == 1 and self.current_position[i] <= self.start_position[i]) or \
                        (self.directions[i] == -1 and self.current_position[i] >= self.start_position[i]):
                    self.current_position[i] = self.start_position[i]

        # Проверка на достижение конечной или начальной позиции с учетом погрешности
        if self.oscillate:
            if self.moving_forward and all(
                    abs(self.current_position[i] - self.end_position[i]) <= self.tolerance for i in range(3)):
                # Если достигли конечной позиции, меняем направление на обратное
                self.moving_forward = False
            elif not self.moving_forward and all(
                    abs(self.current_position[i] - self.start_position[i]) <= self.tolerance for i in range(3)):
                # Если вернулись к начальной позиции, меняем направление на вперед
                self.moving_forward = True

        # Применяем текущие координаты к объекту
        shape.position = self.current_position
