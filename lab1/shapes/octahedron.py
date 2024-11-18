from OpenGL.GL import *

from lab1.shapes.shape import Shape


class Octahedron(Shape):
    def __init__(self, position=[0.0, 0.0, 0.0], scale=1.0, color=[1.0, 1.0, 1.0], rotation=[0.0, 0.0, 0.0]):
        super().__init__(position, scale, color, rotation)

    def draw(self):
        """Отрисовка октаэдра с заданным цветом."""
        glPushMatrix()  # Сохраняем текущее состояние матрицы
        glTranslatef(self.position[0], self.position[1], self.position[2])  # Перемещаем октаэдр
        glScalef(self.scale, self.scale, self.scale)  # Масштабируем октаэдр
        glColor3f(self.color[0], self.color[1], self.color[2])  # Устанавливаем цвет

        glBegin(GL_TRIANGLES)

        # Вершины октаэдра
        v0 = [0.0, 1.0, 0.0]
        v1 = [1.0, 0.0, 0.0]
        v2 = [0.0, 0.0, 1.0]
        v3 = [-1.0, 0.0, 0.0]
        v4 = [0.0, 0.0, -1.0]
        v5 = [0.0, -1.0, 0.0]

        # Верхняя пирамида
        self.draw_triangle(v0, v1, v2)
        self.draw_triangle(v0, v2, v3)
        self.draw_triangle(v0, v3, v4)
        self.draw_triangle(v0, v4, v1)

        # Нижняя пирамида
        self.draw_triangle(v5, v1, v2)
        self.draw_triangle(v5, v2, v3)
        self.draw_triangle(v5, v3, v4)
        self.draw_triangle(v5, v4, v1)

        glEnd()
        glPopMatrix()

    def draw_edges(self):
        """Отрисовка рёбер октаэдра (контуров)."""
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glScalef(self.scale, self.scale, self.scale)
        glColor3f(0.0, 0.0, 0.0)  # Цвет рёбер — черный

        glBegin(GL_LINES)

        # Вершины октаэдра
        v0 = [0.0, 1.0, 0.0]
        v1 = [1.0, 0.0, 0.0]
        v2 = [0.0, 0.0, 1.0]
        v3 = [-1.0, 0.0, 0.0]
        v4 = [0.0, 0.0, -1.0]
        v5 = [0.0, -1.0, 0.0]

        # Верхняя пирамида
        self.draw_line(v0, v1)
        self.draw_line(v0, v2)
        self.draw_line(v0, v3)
        self.draw_line(v0, v4)

        # Нижняя пирамида
        self.draw_line(v5, v1)
        self.draw_line(v5, v2)
        self.draw_line(v5, v3)
        self.draw_line(v5, v4)

        # Соединяем вершины
        self.draw_line(v1, v2)
        self.draw_line(v2, v3)
        self.draw_line(v3, v4)
        self.draw_line(v4, v1)

        glEnd()
        glPopMatrix()

    def draw_triangle(self, v1, v2, v3):
        """Отрисовка одного треугольника."""
        glVertex3fv(v1)
        glVertex3fv(v2)
        glVertex3fv(v3)

    def draw_line(self, v1, v2):
        """Отрисовка одного ребра."""
        glVertex3fv(v1)
        glVertex3fv(v2)
