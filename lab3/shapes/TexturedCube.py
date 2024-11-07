from OpenGL.GL import *
from OpenGL.GLUT import *

from lab3.shapes.shape import Shape


class TexturedCube(Shape):
    def __init__(self, position=[0.0, 0.0, 0.0], scale=1.0, rotation=[0.0, 0.0, 0.0],
                 material=None):
        super().__init__(position, scale, rotation, material=material)

    def draw(self):
        """Отрисовка куба с текстурой."""
        #if self.texture:
        #    self.apply_texture()

        # Убедимся, что мы не устанавливаем лишний цвет, который может искажать текстуру
        glColor3f(1.0, 1.0, 1.0)  # Устанавливаем белый цвет, чтобы не искажать текстуру

        glBegin(GL_QUADS)

        # Передняя грань
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(-0.5, 0.5, 0.5)

        # Задняя грань
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(0.5, 0.5, -0.5)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(-0.5, 0.5, -0.5)

        # Левая грань
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(-0.5, 0.5, -0.5)

        # Правая грань
        glTexCoord2f(0.0, 0.0);
        glVertex3f(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(0.5, 0.5, -0.5)

        # Верхняя грань
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-0.5, 0.5, -0.5)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(-0.5, 0.5, 0.5)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(0.5, 0.5, -0.5)

        # Нижняя грань
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(0.5, -0.5, 0.5)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(0.5, -0.5, -0.5)

        glEnd()

    def draw_edges(self):
        pass
