import math

from OpenGL.GL import *

from lab2.shapes.shape import Shape
from lab2.shapes.utils import draw_triangle, draw_edge, batch_draw_triangles


class Torus(Shape):
    def __init__(self, inner_radius=0.5, outer_radius=1.0, rings=30, sides=30, position=[0.0, 0.0, 0.0], scale=1.0,
                 rotation=[0.0, 0.0, 0.0], material=None):
        super().__init__(position, scale, rotation, material=material)
        self.inner_radius = inner_radius  # Внутренний радиус тора
        self.outer_radius = outer_radius  # Внешний радиус тора
        self.rings = rings  # Количество сегментов по кольцу
        self.sides = sides  # Количество сегментов по кругу

    def draw(self):
        """Отрисовка тора с заданным цветом."""
        glPushMatrix()
        self.draw_surface()
        glPopMatrix()

    def draw_edges(self):
        """Отрисовка каркасных рёбер тора."""
        glPushMatrix()
        glColor3f(0.0, 0.0, 0.0)  # Цвет рёбер — чёрный
        self.draw_wireframe()
        glPopMatrix()

    def draw_surface(self):
        """Рисуем поверхность тора в виде треугольников."""
        triangles = []
        glBegin(GL_TRIANGLES)
        for i in range(self.rings):
            for j in range(self.sides):
                # Координаты текущей вершины и соседей
                p1, uv1 = self.vertex(i, j)
                p2, uv2 = self.vertex(i + 1, j)
                p3, uv3 = self.vertex(i + 1, j + 1)
                p4, uv4 = self.vertex(i, j + 1)

                # Нормали для каждой вершины
                n1 = self.normal(i, j)
                n2 = self.normal(i + 1, j)
                n3 = self.normal(i + 1, j + 1)
                n4 = self.normal(i, j + 1)

                # Рисуем два треугольника
                triangles.append((p1, p2, p3, n1, uv1, uv2, uv3))
                triangles.append((p1, p3, p4, n1, uv1, uv3, uv4))
        batch_draw_triangles(triangles)
        glEnd()

    def draw_wireframe(self):
        """Рисуем каркас тора (линии по рёбрам)."""
        glBegin(GL_LINES)
        for i in range(self.rings):
            for j in range(self.sides):
                # Координаты текущей вершины и соседей
                p1, _ = self.vertex(i, j)
                p2, _ = self.vertex(i + 1, j)
                p3, _ = self.vertex(i, j + 1)

                # Линии вдоль кольца
                draw_edge(p1, p2)
                # Линии вдоль бокового сегмента
                draw_edge(p1, p3)
        glEnd()

    def vertex(self, ring, side):
        """Возвращает координаты вершины и текстурные координаты."""
        theta = 2.0 * math.pi * (ring % self.rings) / self.rings
        phi = 2.0 * math.pi * (side % self.sides) / self.sides
        x = (self.outer_radius + self.inner_radius * math.cos(phi)) * math.cos(theta)
        y = (self.outer_radius + self.inner_radius * math.cos(phi)) * math.sin(theta)
        z = self.inner_radius * math.sin(phi)
        u = ring / self.rings
        v = side / self.sides
        return [x, y, z], [u, v]

    def normal(self, ring, side):
        """Возвращает нормаль к вершине."""
        theta = 2.0 * math.pi * (ring % self.rings) / self.rings
        phi = 2.0 * math.pi * (side % self.sides) / self.sides
        x = math.cos(phi) * math.cos(theta)
        y = math.cos(phi) * math.sin(theta)
        z = math.sin(phi)
        return [x, y, z]
