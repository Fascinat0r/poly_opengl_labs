import math

from OpenGL.GL import *
from lab1.shapes.shape import Shape


class Cylinder(Shape):
    def __init__(self, base_radius=1.0, top_radius=1.0, height=2.0, slices=20, position=[0.0, 0.0, 0.0], scale=1.0,
                 color=[1.0, 1.0, 1.0], rotation=[0.0, 0.0, 0.0]):
        super().__init__(position, scale, color, rotation)
        self.base_radius = base_radius  # Радиус основания цилиндра
        self.top_radius = top_radius  # Радиус вершины цилиндра
        self.height = height  # Высота цилиндра
        self.slices = slices  # Количество сегментов по окружности

    def draw(self):
        """Отрисовка поверхности цилиндра с заданным цветом."""
        glColor3f(self.color[0], self.color[1], self.color[2])  # Устанавливаем цвет
        self.draw_surface()

    def draw_edges(self):
        """Отрисовка каркасных рёбер цилиндра."""
        glColor3f(0.0, 0.0, 0.0)  # Цвет рёбер — чёрный
        self.draw_wireframe()

    def draw_surface(self):
        """Рисуем поверхность цилиндра."""
        glBegin(GL_TRIANGLES)

        # Боковая поверхность
        for i in range(self.slices):
            theta = 2.0 * math.pi * i / self.slices
            next_theta = 2.0 * math.pi * (i + 1) / self.slices

            # Вершины нижней окружности
            x1_base = self.base_radius * math.cos(theta)
            z1_base = self.base_radius * math.sin(theta)
            x2_base = self.base_radius * math.cos(next_theta)
            z2_base = self.base_radius * math.sin(next_theta)

            # Вершины верхней окружности
            x1_top = self.top_radius * math.cos(theta)
            z1_top = self.top_radius * math.sin(theta)
            x2_top = self.top_radius * math.cos(next_theta)
            z2_top = self.top_radius * math.sin(next_theta)

            # Первый треугольник
            glVertex3f(x1_base, 0.0, z1_base)
            glVertex3f(x2_base, 0.0, z2_base)
            glVertex3f(x1_top, self.height, z1_top)

            # Второй треугольник
            glVertex3f(x1_top, self.height, z1_top)
            glVertex3f(x2_base, 0.0, z2_base)
            glVertex3f(x2_top, self.height, z2_top)

        glEnd()

        # Нижнее основание
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, 0.0, 0.0)  # Центр нижнего основания
        for i in range(self.slices + 1):
            theta = 2.0 * math.pi * i / self.slices
            x = self.base_radius * math.cos(theta)
            z = self.base_radius * math.sin(theta)
            glVertex3f(x, 0.0, z)
        glEnd()

        # Верхнее основание
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, self.height, 0.0)  # Центр верхнего основания
        for i in range(self.slices + 1):
            theta = 2.0 * math.pi * i / self.slices
            x = self.top_radius * math.cos(theta)
            z = self.top_radius * math.sin(theta)
            glVertex3f(x, self.height, z)
        glEnd()

    def draw_wireframe(self):
        """Рисуем каркас цилиндра (линии по рёбрам)."""
        glBegin(GL_LINES)

        # Рёбра между верхним и нижним основанием
        for i in range(self.slices):
            theta = 2.0 * math.pi * i / self.slices
            next_theta = 2.0 * math.pi * (i + 1) / self.slices

            # Вершины нижней окружности
            x1_base = self.base_radius * math.cos(theta)
            z1_base = self.base_radius * math.sin(theta)
            x2_base = self.base_radius * math.cos(next_theta)
            z2_base = self.base_radius * math.sin(next_theta)

            # Вершины верхней окружности
            x1_top = self.top_radius * math.cos(theta)
            z1_top = self.top_radius * math.sin(theta)
            x2_top = self.top_radius * math.cos(next_theta)
            z2_top = self.top_radius * math.sin(next_theta)

            # Линии от нижней окружности к верхней
            glVertex3f(x1_base, 0.0, z1_base)
            glVertex3f(x1_top, self.height, z1_top)

            # Линии между соседними вершинами нижней окружности
            glVertex3f(x1_base, 0.0, z1_base)
            glVertex3f(x2_base, 0.0, z2_base)

            # Линии между соседними вершинами верхней окружности
            glVertex3f(x1_top, self.height, z1_top)
            glVertex3f(x2_top, self.height, z2_top)

        glEnd()
