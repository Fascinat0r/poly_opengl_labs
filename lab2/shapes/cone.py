import math
from OpenGL.GL import *
from lab2.shapes.shape import Shape
from lab2.shapes.utils import draw_edge, batch_draw_triangles


class Cone(Shape):
    def __init__(self, base_radius=1.0, height=2.0, slices=30, position=[0.0, 0.0, 0.0], scale=1.0,
                 rotation=[0.0, 0.0, 0.0], material=None):
        super().__init__(position, scale, rotation, material=material)
        self.base_radius = base_radius  # Радиус основания конуса
        self.height = height  # Высота конуса
        self.slices = slices  # Количество сегментов по окружности

    def draw(self):
        """Отрисовка поверхности конуса."""
        self.draw_surface()

    def draw_edges(self):
        """Отрисовка каркасных рёбер конуса."""
        glColor3f(0.0, 0.0, 0.0)  # Цвет рёбер — чёрный
        self.draw_wireframe()

    def draw_surface(self):
        """Рисуем поверхность конуса с использованием batch."""
        triangles = []

        # Вершина конуса
        tip = [0.0, self.height, 0.0]

        # Отрисовка боковых поверхностей
        for i in range(self.slices):
            theta = 2.0 * math.pi * i / self.slices
            next_theta = 2.0 * math.pi * (i + 1) / self.slices

            # Вершины на основании
            x1 = self.base_radius * math.cos(theta)
            z1 = self.base_radius * math.sin(theta)
            x2 = self.base_radius * math.cos(next_theta)
            z2 = self.base_radius * math.sin(next_theta)

            # Нормаль для боковой поверхности
            normal = [x1 + x2, self.height, z1 + z2]
            length = math.sqrt(normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2)
            normal = [n / length for n in normal]

            # Текстурные координаты
            uv_tip = [0.5, 1.0]
            uv1 = [i / self.slices, 0.0]
            uv2 = [(i + 1) / self.slices, 0.0]

            # Добавляем треугольник в список
            triangles.append((tip, [x1, 0.0, z1], [x2, 0.0, z2], normal, uv_tip, uv1, uv2))

        batch_draw_triangles(triangles)

        # Основание конуса
        glBegin(GL_TRIANGLE_FAN)
        center_normal = [0.0, -1.0, 0.0]  # Нормаль для основания
        glNormal3fv(center_normal)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0.0, 0.0, 0.0)  # Центр основания
        for i in range(self.slices + 1):
            theta = 2.0 * math.pi * i / self.slices
            x = self.base_radius * math.cos(theta)
            z = self.base_radius * math.sin(theta)
            uv = [0.5 + 0.5 * math.cos(theta), 0.5 + 0.5 * math.sin(theta)]
            glTexCoord2f(*uv)
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
            draw_edge(tip, [x1, 0.0, z1])

            # Линии по основанию
            draw_edge([x1, 0.0, z1], [x2, 0.0, z2])

        glEnd()
