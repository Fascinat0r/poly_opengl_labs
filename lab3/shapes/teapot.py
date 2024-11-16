from OpenGL.GL import *
from OpenGL.GLUT import *
from lab3.shapes.shape import Shape


class Teapot(Shape):
    def __init__(self, wireframe=False, position=[0.0, 0.0, 0.0], scale=1.0, rotation=[0.0, 0.0, 0.0], material=None):
        super().__init__(position, scale, rotation, material)
        self.wireframe = wireframe

    def setup_mesh(self):
        """Настройка меша для чайника не требуется."""
        pass

    def draw_mesh(self, shader):
        """Отрисовка чайника."""
        if self.wireframe:
            glutWireTeapot(1.0)
        else:
            glutSolidTeapot(1.0)
