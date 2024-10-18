from abc import ABC, abstractmethod

from OpenGL.GL import *


class Shape(ABC):
    def __init__(self, position=[0.0, 0.0, 0.0], scale=1.0, color=[1.0, 1.0, 1.0], rotation=[0.0, 0.0, 0.0]):
        self.position = position  # Позиция фигуры
        self.scale = scale  # Масштаб фигуры
        self.color = color  # Цвет фигуры
        self.rotation = rotation  # Вектор вращения (углы вращения по осям X, Y, Z)

    @abstractmethod
    def draw(self):
        """Отрисовка фигуры."""
        pass

    @abstractmethod
    def draw_edges(self):
        """Отрисовка рёбер фигуры."""
        pass

    def render(self):
        """Отрисовка фигуры с применением всех трансформаций."""
        glPushMatrix()

        # 1. Перемещаем объект в его позицию
        glTranslatef(self.position[0], self.position[1], self.position[2])

        # 2. Применяем вращение по каждой оси
        glRotatef(self.rotation[0], 1.0, 0.0, 0.0)  # Вращение вокруг оси X
        glRotatef(self.rotation[1], 0.0, 1.0, 0.0)  # Вращение вокруг оси Y
        glRotatef(self.rotation[2], 0.0, 0.0, 1.0)  # Вращение вокруг оси Z

        # 3. Применяем масштабирование, если необходимо
        glScalef(self.scale, self.scale, self.scale)

        # 4. Отрисовываем объект
        self.draw()
        self.draw_edges()

        glPopMatrix()
