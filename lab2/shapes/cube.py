from OpenGL.GL import *
from lab2.shapes.shape import Shape
from lab2.shapes.utils import draw_quad, draw_edge, draw_triangle


class Cube(Shape):
    def __init__(self, position=[0.0, 0.0, 0.0], scale=1.0, rotation=[0.0, 0.0, 0.0],
                 material=None):
        super().__init__(position, scale, rotation, material=material)

    def draw(self):
        """Отрисовка куба с текстурой и нормалями для корректного освещения."""
        glColor3f(1.0, 1.0, 1.0)  # Устанавливаем белый цвет для текстур

        # Координаты вершин куба
        v0 = [-0.5, -0.5, -0.5]
        v1 = [0.5, -0.5, -0.5]
        v2 = [0.5, 0.5, -0.5]
        v3 = [-0.5, 0.5, -0.5]
        v4 = [-0.5, -0.5, 0.5]
        v5 = [0.5, -0.5, 0.5]
        v6 = [0.5, 0.5, 0.5]
        v7 = [-0.5, 0.5, 0.5]

        # Грани куба
        glBegin(GL_QUADS)

        # Передняя грань
        draw_quad(v4, v5, v6, v7, [0.0, 0.0, 1.0], [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0])

        # Задняя грань
        draw_quad(v0, v1, v2, v3, [0.0, 0.0, -1.0], [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0])

        # Левая грань
        draw_quad(v0, v4, v7, v3, [-1.0, 0.0, 0.0], [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0])

        # Правая грань
        draw_quad(v1, v5, v6, v2, [1.0, 0.0, 0.0], [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0])

        # Верхняя грань
        draw_quad(v3, v7, v6, v2, [0.0, 1.0, 0.0], [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0])

        # Нижняя грань
        draw_quad(v0, v4, v5, v1, [0.0, -1.0, 0.0], [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0])

        glEnd()

    def draw_edges(self):
        """Отрисовка рёбер куба (контуров)."""
        glPushMatrix()
        glColor3f(0.0, 0.0, 0.0)  # Чёрный цвет для рёбер

        # Координаты вершин куба
        v0 = [-0.5, -0.5, -0.5]
        v1 = [0.5, -0.5, -0.5]
        v2 = [0.5, 0.5, -0.5]
        v3 = [-0.5, 0.5, -0.5]
        v4 = [-0.5, -0.5, 0.5]
        v5 = [0.5, -0.5, 0.5]
        v6 = [0.5, 0.5, 0.5]
        v7 = [-0.5, 0.5, 0.5]

        glBegin(GL_LINES)

        # Рёбра передней грани
        draw_edge(v4, v5)
        draw_edge(v5, v6)
        draw_edge(v6, v7)
        draw_edge(v7, v4)

        # Рёбра задней грани
        draw_edge(v0, v1)
        draw_edge(v1, v2)
        draw_edge(v2, v3)
        draw_edge(v3, v0)

        # Соединительные рёбра
        draw_edge(v0, v4)
        draw_edge(v1, v5)
        draw_edge(v2, v6)
        draw_edge(v3, v7)

        glEnd()
        glPopMatrix()
