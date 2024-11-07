from OpenGL.GL import *

from lab3.shapes.shape import Shape


class Cube(Shape):
    def __init__(self, position=[0.0, 0.0, 0.0], scale=1.0, rotation=[0.0, 0.0, 0.0],
                 material=None):
        super().__init__(position, scale, rotation, material=material)

    def draw(self):
        """Отрисовка куба с текстурой и нормалями для корректного освещения."""

        #self.material.apply()  # Применение материала

        glColor3f(1.0, 1.0, 1.0)  # Устанавливаем белый цвет, чтобы не искажать текстуру

        glBegin(GL_QUADS)

        # Передняя грань с нормалью
        glNormal3f(0.0, 0.0, 1.0)  # Нормаль для передней грани
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(-0.5, 0.5, 0.5)

        # Задняя грань с нормалью
        glNormal3f(0.0, 0.0, -1.0)  # Нормаль для задней грани
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(0.5, 0.5, -0.5)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(-0.5, 0.5, -0.5)

        # Левая грань с нормалью
        glNormal3f(-1.0, 0.0, 0.0)  # Нормаль для левой грани
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(-0.5, 0.5, -0.5)

        # Правая грань с нормалью
        glNormal3f(1.0, 0.0, 0.0)  # Нормаль для правой грани
        glTexCoord2f(0.0, 0.0);
        glVertex3f(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(0.5, 0.5, -0.5)

        # Верхняя грань с нормалью
        glNormal3f(0.0, 1.0, 0.0)  # Нормаль для верхней грани
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-0.5, 0.5, -0.5)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(-0.5, 0.5, 0.5)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(0.5, 0.5, -0.5)

        # Нижняя грань с нормалью
        glNormal3f(0.0, -1.0, 0.0)  # Нормаль для нижней грани
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0);
        glVertex3f(0.5, -0.5, 0.5)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(0.5, -0.5, -0.5)

        glEnd()

        # glDisable(GL_TEXTURE_2D)  # Отключаем текстурирование
        # self.material.cleanup()  # Очистка после рендеринга

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
