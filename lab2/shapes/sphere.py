import math

from OpenGL.GL import *
from lab2.shapes.shape import Shape
from lab2.shapes.utils import draw_edge, batch_draw_triangles


class Sphere(Shape):
    def __init__(self, radius=1.0, stacks=20, slices=20, position=[0.0, 0.0, 0.0], scale=1.0,
                 rotation=[0.0, 0.0, 0.0], material=None):
        super().__init__(position, scale, rotation, material=material)
        self.radius = radius  # Радиус сферы
        self.stacks = stacks  # Количество параллелей
        self.slices = slices  # Количество меридианов

    def draw(self):
        """Отрисовка сферы с использованием материала."""
        glColor3f(1.0, 1.0, 1.0)  # Устанавливаем белый цвет для текстур
        self.draw_surface()

    def draw_edges(self):
        """Отрисовка каркасных рёбер сферы."""
        glColor3f(0.0, 0.0, 0.0)  # Чёрный цвет для рёбер
        self.draw_wireframe()

    def draw_surface(self):
        """Рисуем поверхность сферы с использованием batch."""
        triangles = []
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
                v4 = self.vertex(theta2, phi2)

                # Нормали для каждой вершины
                n1 = self.normal(v1)
                n3 = self.normal(v3)

                # Текстурные координаты
                uv1 = [slice / self.slices, stack / self.stacks]
                uv2 = [(slice + 1) / self.slices, stack / self.stacks]
                uv3 = [slice / self.slices, (stack + 1) / self.stacks]
                uv4 = [(slice + 1) / self.slices, (stack + 1) / self.stacks]

                # Добавляем два треугольника в список
                triangles.append((v1, v2, v3, n1, uv1, uv2, uv3))
                triangles.append((v3, v2, v4, n3, uv3, uv2, uv4))

        batch_draw_triangles(triangles)

    def draw_wireframe(self):
        """Рисуем каркас сферы."""
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
                draw_edge(v1, v3)

                # Линии по параллелям
                draw_edge(v1, v2)
        glEnd()

    def vertex(self, theta, phi):
        """Вычисляет координаты вершины на сфере."""
        x = self.radius * math.sin(phi) * math.cos(theta)
        y = self.radius * math.cos(phi)
        z = self.radius * math.sin(phi) * math.sin(theta)
        return [x, y, z]

    def normal(self, vertex):
        """Вычисляет нормаль для вершины (нормализация координат)."""
        length = math.sqrt(vertex[0] ** 2 + vertex[1] ** 2 + vertex[2] ** 2)
        return [vertex[0] / length, vertex[1] / length, vertex[2] / length]
