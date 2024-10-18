from OpenGL.GL import *

from app.shapes.shape import Shape


class Cube(Shape):
    def __init__(self, position=[0.0, 0.0, 0.0], scale=1.0, color=[1.0, 1.0, 1.0], rotation=[0.0, 0.0, 0.0]):
        super().__init__(position, scale, color, rotation)

    def draw(self):
        """Отрисовка куба с заданным цветом и масштабом."""
        glPushMatrix()  # Сохраняем текущее состояние матрицы
        glColor3f(self.color[0], self.color[1], self.color[2])  # Устанавливаем цвет

        glBegin(GL_QUADS)

        # Вершины куба с центром в (0, 0, 0)
        # Передняя грань
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)

        # Задняя грань
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)

        # Левая грань
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, -0.5)

        # Правая грань
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)

        # Верхняя грань
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, -0.5)

        # Нижняя грань
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)

        glEnd()
        glPopMatrix()  # Восстанавливаем матрицу

    def draw_edges(self):
        """Отрисовка рёбер куба (контуров)."""
        glPushMatrix()
        glColor3f(0.0, 0.0, 0.0)  # Цвет рёбер — чёрный

        glBegin(GL_LINES)

        # Ребра куба с центром в (0, 0, 0)
        # Передняя грань
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)

        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)

        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)

        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)

        # Задняя грань
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)

        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)

        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)

        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, -0.5, -0.5)

        # Соединения передней и задней граней
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, -0.5)

        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, -0.5)

        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, -0.5)

        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, -0.5)

        glEnd()
        glPopMatrix()


def update(self):
    pass
