from abc import ABC, abstractmethod

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from lab2.materials.material import Material


class Shape(ABC):
    def __init__(self, position, scale, rotation, color=[1.0, 1.0, 1.0, 1.0],
                 material=None):
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.material = material if material else Material(color=color)  # Материал объекта

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
            pass
            # Если материал не указан, просто используем цвет
            #glColor3f(self.color[0], self.color[1], self.color[2])

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
        """Отрисовка фигуры с применением трансформаций и материала."""
        # Сохраняем текущую матрицу
        glPushMatrix()
        # Применяем трансформации объекта
        glTranslatef(*self.position)
        # Поворачиваем объект
        glRotatef(self.rotation[0], 1.0, 0.0, 0.0)
        glRotatef(self.rotation[1], 0.0, 1.0, 0.0)
        glRotatef(self.rotation[2], 0.0, 0.0, 1.0)
        # Масштабируем объект
        glScalef(self.scale, self.scale, self.scale)

        self.material.apply()  # Применение материала
        self.draw()  # Отрисовка объекта
        self.material.cleanup()  # Очистка после рендеринга

        # Отрисовка осей координат в центре объекта
        self.draw_center_axes()

        # Восстанавливаем матрицу
        glPopMatrix()
