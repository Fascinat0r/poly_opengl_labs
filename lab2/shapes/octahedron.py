import numpy as np

from OpenGL.GL import *
from lab2.shapes.shape import Shape
from lab2.shapes.utils import draw_edge, draw_triangle


class Octahedron(Shape):
    def __init__(self, position=[0.0, 0.0, 0.0], scale=1.0, rotation=[0.0, 0.0, 0.0],
                 material=None):
        super().__init__(position, scale, rotation, material=material)

    @staticmethod
    def calculate_normal(v1, v2, v3):
        """Вычисление нормали к поверхности треугольника."""
        # Векторы грани
        edge1 = np.subtract(v2, v1)
        edge2 = np.subtract(v3, v1)
        # Векторное произведение
        normal = np.cross(edge1, edge2)
        # Нормализация
        length = np.linalg.norm(normal)
        if length != 0:
            normal = normal / length
        return -normal

    def draw(self):
        """Отрисовка октаэдра с текстурой и корректными нормалями."""
        glColor3f(1.0, 1.0, 1.0)  # Устанавливаем белый цвет для текстур

        # Координаты вершин октаэдра
        v0 = [0.0, 0.5, 0.0]  # Верхняя вершина
        v1 = [0.5, 0.0, 0.5]  # Передняя-правая вершина
        v2 = [-0.5, 0.0, 0.5]  # Передняя-левая вершина
        v3 = [-0.5, 0.0, -0.5]  # Задняя-левая вершина
        v4 = [0.5, 0.0, -0.5]  # Задняя-правая вершина
        v5 = [0.0, -0.5, 0.0]  # Нижняя вершина

        glBegin(GL_TRIANGLES)

        # Верхняя пирамида
        normal = self.calculate_normal(v0, v1, v2)
        draw_triangle(v0, v1, v2, normal, [0.0, 0.0], [1.0, 0.0], [0.5, 1.0])  # Передняя грань

        normal = self.calculate_normal(v0, v2, v3)
        draw_triangle(v0, v2, v3, normal, [0.5, 1.0], [0.0, 0.0], [1.0, 0.0])  # Левая грань

        normal = self.calculate_normal(v0, v3, v4)
        draw_triangle(v0, v3, v4, normal, [1.0, 0.0], [0.5, 1.0], [0.0, 0.0])  # Задняя грань

        normal = self.calculate_normal(v0, v4, v1)
        draw_triangle(v0, v4, v1, normal, [0.0, 0.0], [1.0, 0.0], [0.5, 1.0])  # Правая грань

        # Нижняя пирамида
        normal = self.calculate_normal(v5, v1, v2)
        draw_triangle(v5, v1, v2, normal, [0.0, 0.0], [1.0, 0.0], [0.5, 1.0])  # Передняя грань

        normal = self.calculate_normal(v5, v2, v3)
        draw_triangle(v5, v2, v3, normal, [0.5, 1.0], [0.0, 0.0], [1.0, 0.0])  # Левая грань

        normal = self.calculate_normal(v5, v3, v4)
        draw_triangle(v5, v3, v4, normal, [1.0, 0.0], [0.5, 1.0], [0.0, 0.0])  # Задняя грань

        normal = self.calculate_normal(v5, v4, v1)
        draw_triangle(v5, v4, v1, normal, [0.0, 0.0], [1.0, 0.0], [0.5, 1.0])  # Правая грань

        glEnd()

    def draw_edges(self):
        """Отрисовка рёбер октаэдра (контуров)."""
        glPushMatrix()
        glColor3f(0.0, 0.0, 0.0)  # Чёрный цвет для рёбер

        # Координаты вершин
        v0 = [0.0, 0.5, 0.0]  # Верхняя вершина
        v1 = [0.5, 0.0, 0.5]  # Передняя-правая вершина
        v2 = [-0.5, 0.0, 0.5]  # Передняя-левая вершина
        v3 = [-0.5, 0.0, -0.5]  # Задняя-левая вершина
        v4 = [0.5, 0.0, -0.5]  # Задняя-правая вершина
        v5 = [0.0, -0.5, 0.0]  # Нижняя вершина

        glBegin(GL_LINES)

        # Верхние рёбра
        draw_edge(v0, v1)
        draw_edge(v0, v2)
        draw_edge(v0, v3)
        draw_edge(v0, v4)

        # Нижние рёбра
        draw_edge(v5, v1)
        draw_edge(v5, v2)
        draw_edge(v5, v3)
        draw_edge(v5, v4)

        # Горизонтальные рёбра
        draw_edge(v1, v2)
        draw_edge(v2, v3)
        draw_edge(v3, v4)
        draw_edge(v4, v1)

        glEnd()
        glPopMatrix()
