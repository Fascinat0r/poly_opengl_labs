from abc import ABC, abstractmethod


class Animation(ABC):
    def __init__(self, target_object):
        self.running = False  # Указывает, запущена ли анимация
        self.target_object = target_object  # Объект, к которому привязана анимация

    @abstractmethod
    def start(self):
        """Запуск анимации."""
        pass

    @abstractmethod
    def update(self, shape, delta_time):
        """Обновление состояния анимации с учетом delta_time."""
        pass
