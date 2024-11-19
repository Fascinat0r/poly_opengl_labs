import math

from OpenGL.GL import *
from lab1.shapes.shape import Shape


class Sphere(Shape):
    def __init__(self, radius=1.0, stacks=20, slices=20, position=[0.0, 0.0, 0.0], scale=1.0,
                 color=[1.0, 1.0, 1.0], rotation=[0.0, 0.0, 0.0]):
        super().__init__(position, scale, color, rotation)
        self.radius = radius  # Радиус сферы
        self.stacks = stacks  # Количество параллелей (горизонтальных делений)
        self.slices = slices  # Количество меридианов (вертикальных делений)

    def draw(self):
        """Отрисовка поверхности сферы с заданным цветом."""
        glColor3f(self.color[0], self.color[1], self.color[2])  # Устанавливаем цвет
        self.draw_surface()

    def draw_edges(self):
        """Отрисовка каркасных рёбер сферы."""
        glColor3f(0.0, 0.0, 0.0)  # Цвет рёбер — чёрный
        self.draw_wireframe()

    def draw_surface(self):
        """Рисуем поверхность сферы."""
        glBegin(GL_TRIANGLES)
        for stack in range(self.stacks):
            phi1 = math.pi * stack / self.stacks  # Угол для текущего горизонтального слоя
            phi2 = math.pi * (stack + 1) / self.stacks  # Угол для следующего слоя

            for slice in range(self.slices):
                theta1 = 2.0 * math.pi * slice / self.slices  # Угол для текущего меридиана
                theta2 = 2.0 * math.pi * (slice + 1) / self.slices  # Угол для следующего меридиана

                # Вершины текущего сегмента
                v1 = self.vertex(theta1, phi1)
                v2 = self.vertex(theta2, phi1)
                v3 = self.vertex(theta1, phi2)
                v4 = self.vertex(theta2, phi2)

                # Рисуем два треугольника для сегмента
                glVertex3fv(v1)
                glVertex3fv(v2)
                glVertex3fv(v3)

                glVertex3fv(v3)
                glVertex3fv(v2)
                glVertex3fv(v4)
        glEnd()

    def draw_wireframe(self):
        """Рисуем каркас сферы (линии по рёбрам)."""
        glBegin(GL_LINES)
        for stack in range(self.stacks):
            phi1 = math.pi * stack / self.stacks
            phi2 = math.pi * (stack + 1) / self.stacks

            for slice in range(self.slices):
                theta1 = 2.0 * math.pi * slice / self.slices
                theta2 = 2.0 * math.pi * (slice + 1) / self.slices

                # Вершины текущего сегмента
                v1 = self.vertex(theta1, phi1)
                v2 = self.vertex(theta2, phi1)
                v3 = self.vertex(theta1, phi2)

                # Линии по меридианам
                glVertex3fv(v1)
                glVertex3fv(v3)

                # Линии по параллелям
                glVertex3fv(v1)
                glVertex3fv(v2)
        glEnd()

    def vertex(self, theta, phi):
        """Вычисляет координаты вершины на сфере."""
        x = self.radius * math.sin(phi) * math.cos(theta)
        y = self.radius * math.cos(phi)
        z = self.radius * math.sin(phi) * math.sin(theta)
        return [x, y, z]
