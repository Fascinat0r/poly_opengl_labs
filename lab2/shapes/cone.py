import math

from OpenGL.GL import *

from lab2.shapes.shape import Shape


class Cone(Shape):
    def __init__(self, base_radius=1.0, height=2.0, slices=30, position=[0.0, 0.0, 0.0], scale=1.0,
                 rotation=[0.0, 0.0, 0.0], material=None):
        super().__init__(position, scale, rotation, material=material)
        self.base_radius = base_radius  # Радиус основания конуса
        self.height = height  # Высота конуса
        self.slices = slices  # Количество сегментов по окружности

    def draw(self):
        """Отрисовка поверхности конуса с заданным цветом."""
        # glColor3f(self.color[0], self.color[1], self.color[2])  # Устанавливаем цвет
        self.draw_surface()

    def draw_edges(self):
        """Отрисовка каркасных рёбер конуса."""
        glColor3f(0.0, 0.0, 0.0)  # Цвет рёбер — чёрный
        self.draw_wireframe()

    def draw_surface(self):
        """Рисуем поверхность конуса."""
        glBegin(GL_TRIANGLES)

        # Вершина конуса
        tip = [0.0, self.height, 0.0]

        # Отрисовка боковых поверхностей
        for i in range(self.slices):
            theta = 2.0 * math.pi * i / self.slices
            next_theta = 2.0 * math.pi * (i + 1) / self.slices

            # Треугольники для боковой поверхности
            x1 = self.base_radius * math.cos(theta)
            z1 = self.base_radius * math.sin(theta)
            x2 = self.base_radius * math.cos(next_theta)
            z2 = self.base_radius * math.sin(next_theta)

            glVertex3f(tip[0], tip[1], tip[2])  # Вершина конуса
            glVertex3f(x1, 0.0, z1)  # Точка на основании
            glVertex3f(x2, 0.0, z2)  # Следующая точка на основании

        glEnd()

        # Основание конуса
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, 0.0, 0.0)  # Центр основания
        for i in range(self.slices + 1):
            theta = 2.0 * math.pi * i / self.slices
            x = self.base_radius * math.cos(theta)
            z = self.base_radius * math.sin(theta)
            glVertex3f(x, 0.0, z)
        glEnd()

    def draw_wireframe(self):
        """Рисуем каркас конуса (линии по рёбрам)."""
        glBegin(GL_LINES)

        # Вершина конуса
        tip = [0.0, self.height, 0.0]

        # Рёбра от вершины до основания
        for i in range(self.slices):
            theta = 2.0 * math.pi * i / self.slices
            next_theta = 2.0 * math.pi * (i + 1) / self.slices

            # Вершины на основании
            x1 = self.base_radius * math.cos(theta)
            z1 = self.base_radius * math.sin(theta)
            x2 = self.base_radius * math.cos(next_theta)
            z2 = self.base_radius * math.sin(next_theta)

            # Линии от вершины к основанию
            glVertex3f(tip[0], tip[1], tip[2])
            glVertex3f(x1, 0.0, z1)

            # Линии по основанию
            glVertex3f(x1, 0.0, z1)
            glVertex3f(x2, 0.0, z2)

        glEnd()
