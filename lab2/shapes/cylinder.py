import math

from OpenGL.GL import *
from lab2.shapes.shape import Shape
from lab2.shapes.utils import draw_edge, batch_draw_triangles


class Cylinder(Shape):
    def __init__(self, base_radius=1.0, top_radius=1.0, height=2.0, slices=30, position=[0.0, 0.0, 0.0], scale=1.0,
                 rotation=[0.0, 0.0, 0.0], material=None):
        super().__init__(position, scale, rotation, material=material)
        self.base_radius = base_radius  # Радиус основания цилиндра
        self.top_radius = top_radius  # Радиус вершины цилиндра
        self.height = height  # Высота цилиндра
        self.slices = slices  # Количество сегментов по окружности

    def draw(self):
        """Отрисовка поверхности цилиндра."""
        self.draw_surface()

    def draw_edges(self):
        """Отрисовка каркасных рёбер цилиндра."""
        glColor3f(0.0, 0.0, 0.0)  # Чёрный цвет для рёбер
        self.draw_wireframe()

    def draw_surface(self):
        """Рисуем поверхность цилиндра с использованием batch."""
        triangles = []

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

            # Нормаль для боковой поверхности
            normal = [math.cos((theta + next_theta) / 2), 0.0, math.sin((theta + next_theta) / 2)]

            # Текстурные координаты
            uv_base1 = [i / self.slices, 0.0]
            uv_base2 = [(i + 1) / self.slices, 0.0]
            uv_top1 = [i / self.slices, 1.0]
            uv_top2 = [(i + 1) / self.slices, 1.0]

            # Первый треугольник
            triangles.append((
                [x1_base, 0.0, z1_base], [x2_base, 0.0, z2_base], [x1_top, self.height, z1_top],
                normal, uv_base1, uv_base2, uv_top1
            ))

            # Второй треугольник
            triangles.append((
                [x1_top, self.height, z1_top], [x2_base, 0.0, z2_base], [x2_top, self.height, z2_top],
                normal, uv_top1, uv_base2, uv_top2
            ))

        batch_draw_triangles(triangles)

        # Нижнее основание
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0.0, -1.0, 0.0)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0.0, 0.0, 0.0)  # Центр нижнего основания
        for i in range(self.slices + 1):
            theta = 2.0 * math.pi * i / self.slices
            x = self.base_radius * math.cos(theta)
            z = self.base_radius * math.sin(theta)
            uv = [0.5 + 0.5 * math.cos(theta), 0.5 + 0.5 * math.sin(theta)]
            glTexCoord2f(*uv)
            glVertex3f(x, 0.0, z)
        glEnd()

        # Верхнее основание
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0.0, 1.0, 0.0)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0.0, self.height, 0.0)  # Центр верхнего основания
        for i in range(self.slices + 1):
            theta = 2.0 * math.pi * i / self.slices
            x = self.top_radius * math.cos(theta)
            z = self.top_radius * math.sin(theta)
            uv = [0.5 + 0.5 * math.cos(theta), 0.5 + 0.5 * math.sin(theta)]
            glTexCoord2f(*uv)
            glVertex3f(x, self.height, z)
        glEnd()

    def draw_wireframe(self):
        """Рисуем каркас цилиндра (линии по рёбрам)."""
        glBegin(GL_LINES)

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

            # Линии между нижним и верхним основанием
            draw_edge([x1_base, 0.0, z1_base], [x1_top, self.height, z1_top])

            # Линии по нижнему основанию
            draw_edge([x1_base, 0.0, z1_base], [x2_base, 0.0, z2_base])

            # Линии по верхнему основанию
            draw_edge([x1_top, self.height, z1_top], [x2_top, self.height, z2_top])

        glEnd()
