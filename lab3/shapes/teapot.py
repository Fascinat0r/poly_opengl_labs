from OpenGL.GL import *
from OpenGL.GLUT import *

from lab3.shapes.shape import Shape


class Teapot(Shape):
    def __init__(self, wireframe=False, position=[0.0, 0.0, 0.0], scale=1.0, rotation=[0.0, 0.0, 0.0],
                 material=None):
        super().__init__(position, scale, rotation, material=material)
        self.wireframe = wireframe  # Режим каркасной модели

    def draw(self):
        """Отрисовка чайника с заданным цветом и масштабом."""
        glPushMatrix()
        # glColor3f(self.color[0], self.color[1], self.color[2])  # Устанавливаем цвет

        if self.wireframe:
            glutWireTeapot(1.0)  # Каркасная модель чайника
        else:
            glutSolidTeapot(1.0)  # Сплошная модель чайника

        glPopMatrix()

    def draw_edges(self):
        """Каркасная модель не требует дополнительной отрисовки рёбер."""
        pass

    def draw_surface(self):
        """Сплошная модель не требует дополнительной отрисовки поверхности."""
        pass
