from abc import ABC, abstractmethod

from OpenGL.GL import *


class Shape(ABC):
    def __init__(self, position=[0.0, 0.0, 0.0], scale=1.0, color=[1.0, 1.0, 1.0]):
        self.position = position  # Позиция фигуры
        self.scale = scale  # Масштаб фигуры
        self.color = color  # Цвет фигуры

    @abstractmethod
    def draw(self):
        """Отрисовка фигуры."""
        pass

    @abstractmethod
    def draw_edges(self):
        """Отрисовка рёбер фигуры."""
        pass

    def set_color(self, r, g, b):
        """Установка цвета фигуры."""
        self.color = [r, g, b]

    def set_position(self, x, y, z):
        """Установка позиции фигуры."""
        self.position = [x, y, z]

    def set_scale(self, s):
        """Установка масштаба фигуры."""
        self.scale = s
