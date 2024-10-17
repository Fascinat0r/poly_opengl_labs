from OpenGL.GL import *
from shapes.cube import Cube

class Scene:
    def __init__(self):
        # Здесь будут храниться объекты, добавленные в сцену
        self.objects = []
        # Добавим куб для примера
        self.cube = Cube(position=[0.0, 0.0, 0.0], scale=1.0, color=[1.0, 0.0, 0.0])

    def add_object(self, obj):
        """Добавляем объекты (кубы, сферы и т.д.) в сцену."""
        self.objects.append(obj)

    def draw_axes(self):
        """Отрисовка осей координат."""
        glBegin(GL_LINES)

        # Оси
        glColor3f(1, 0, 0)  # Ось X
        glVertex3f(-10.0, 0.0, 0.0)
        glVertex3f(10.0, 0.0, 0.0)

        glColor3f(0, 1, 0)  # Ось Y
        glVertex3f(0.0, -10.0, 0.0)
        glVertex3f(0.0, 10.0, 0.0)

        glColor3f(0, 0, 1)  # Ось Z
        glVertex3f(0.0, 0.0, -10.0)
        glVertex3f(0.0, 0.0, 10.0)

        glEnd()

    def draw_grid(self):
        """Отрисовка сетки."""
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_LINES)

        for i in range(-10, 11):
            glVertex3f(i, 0, -10)
            glVertex3f(i, 0, 10)
            glVertex3f(-10, 0, i)
            glVertex3f(10, 0, i)

        glEnd()

    def render(self):
        """Основной метод для отрисовки всей сцены."""
        self.draw_axes()
        self.draw_grid()

        # Отрисовка объектов в сцене (например, куба)
        self.cube.draw()        # Отрисовка куба
        self.cube.draw_edges()  # Отрисовка рёбер куба
        for obj in self.objects:
            obj.draw()
            obj.draw_edges()
