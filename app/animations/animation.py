from abc import ABC, abstractmethod

class Animation(ABC):
    def __init__(self, target_object):
        self.running = False  # Переменная, указывающая на то, запущена ли анимация
        self.target_object = target_object  # Объект, к которому привязана анимация

    @abstractmethod
    def start(self):
        """Запуск анимации."""
        pass

    @abstractmethod
    def update(self, shape):
        """Обновление состояния анимации."""
        pass

