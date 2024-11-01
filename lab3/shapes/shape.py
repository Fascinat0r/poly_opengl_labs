from abc import ABC, abstractmethod

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Shape(ABC):
    def __init__(self, position=[0.0, 0.0, 0.0], scale=1.0, color=[1.0, 1.0, 1.0], rotation=[0.0, 0.0, 0.0],
                 material=None, texture=None):
        self.position = position  # Позиция фигуры
        self.scale = scale  # Масштаб фигуры
        self.color = color  # Цвет фигуры
        self.rotation = rotation  # Вектор вращения (углы вращения по осям X, Y, Z)
        self.material = material  # Материал фигуры
        self.texture = texture  # Текстура фигуры (если есть)

    @abstractmethod
    def draw(self):
        """Отрисовка фигуры."""
        pass

    @abstractmethod
    def draw_edges(self):
        """Отрисовка рёбер фигуры."""
        pass

    def apply_material(self):
        """Применение материала для фигуры."""
        if self.material:
            self.material.apply()
        else:
            # Если материал не указан, просто используем цвет
            glColor3f(self.color[0], self.color[1], self.color[2])

    def apply_texture(self):
        """Применение текстуры, если она существует."""
        if self.texture:
            glEnable(GL_TEXTURE_2D)  # Включаем текстурирование
            self.texture.apply()  # Применяем текстуру
        else:
            glDisable(GL_TEXTURE_2D)  # Отключаем текстурирование, если текстуры нет

    def draw_center_axes(self, axis_length=0.2):
        """Отрисовка осей координат в центре объекта."""
        glBegin(GL_LINES)

        # Ось X (красный)
        glColor3f(1.0, 0.0, 0.0)  # Красный цвет для оси X
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(axis_length, 0.0, 0.0)

        # Ось Y (зелёный)
        glColor3f(0.0, 1.0, 0.0)  # Зелёный цвет для оси Y
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, axis_length, 0.0)

        # Ось Z (синий)
        glColor3f(0.0, 0.0, 1.0)  # Синий цвет для оси Z
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, axis_length)

        glEnd()

    def render(self):
        """Отрисовка фигуры с применением всех трансформаций, материалов и текстур."""
        glPushMatrix()

        # 1. Перемещаем объект в его позицию
        glTranslatef(self.position[0], self.position[1], self.position[2])

        # 2. Применяем вращение по каждой оси
        glRotatef(self.rotation[0], 1.0, 0.0, 0.0)  # Вращение вокруг оси X
        glRotatef(self.rotation[1], 0.0, 1.0, 0.0)  # Вращение вокруг оси Y
        glRotatef(self.rotation[2], 0.0, 0.0, 1.0)  # Вращение вокруг оси Z

        # 3. Применяем материал
        self.apply_material()

        # 4. Применяем текстуру
        self.apply_texture()

        # 5. Применяем масштабирование, если необходимо
        glScalef(self.scale, self.scale, self.scale)

        # 6. Отрисовка осей координат в центре объекта
        self.draw_center_axes()

        # 7. Отрисовываем объект
        self.draw()
        self.draw_edges()

        # Отключаем текстуры после их использования
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()
