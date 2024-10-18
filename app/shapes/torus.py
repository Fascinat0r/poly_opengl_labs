import math

from OpenGL.GL import *

from app.shapes.shape import Shape


class Torus(Shape):
    def __init__(self, inner_radius=0.5, outer_radius=1.0, rings=30, sides=30, position=[0.0, 0.0, 0.0], scale=1.0,
                 color=[1.0, 1.0, 1.0], rotation=[0.0, 0.0, 0.0]):
        super().__init__(position, scale, color, rotation)
        self.inner_radius = inner_radius  # Внутренний радиус тора
        self.outer_radius = outer_radius  # Внешний радиус тора
        self.rings = rings  # Количество сегментов по кольцу
        self.sides = sides  # Количество сегментов по кругу

    def draw(self):
        """Отрисовка тора с заданным цветом."""
        glPushMatrix()

        glColor3f(self.color[0], self.color[1], self.color[2])  # Устанавливаем цвет
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
        glBegin(GL_QUADS)
        for i in range(self.rings):
            for j in range(self.sides):
                self.quad_vertex(i, j)
                self.quad_vertex(i + 1, j)
                self.quad_vertex(i + 1, j + 1)
                self.quad_vertex(i, j + 1)
        glEnd()

    def draw_wireframe(self):
        """Рисуем каркас тора (линии по рёбрам)."""
        glBegin(GL_LINES)
        for i in range(self.rings):
            for j in range(self.sides):
                self.line_vertex(i, j)
                self.line_vertex(i + 1, j)
                self.line_vertex(i, j)
                self.line_vertex(i, j + 1)
        glEnd()

    def quad_vertex(self, ring, side):
        """Отрисовка вершины тора для поверхности."""
        theta = 2.0 * math.pi * ring / self.rings
        phi = 2.0 * math.pi * side / self.sides
        x = (self.outer_radius + self.inner_radius * math.cos(phi)) * math.cos(theta)
        y = (self.outer_radius + self.inner_radius * math.cos(phi)) * math.sin(theta)
        z = self.inner_radius * math.sin(phi)
        glVertex3f(x, y, z)

    def line_vertex(self, ring, side):
        """Отрисовка вершины тора для рёбер."""
        theta = 2.0 * math.pi * ring / self.rings
        phi = 2.0 * math.pi * side / self.sides
        x = (self.outer_radius + self.inner_radius * math.cos(phi)) * math.cos(theta)
        y = (self.outer_radius + self.inner_radius * math.cos(phi)) * math.sin(theta)
        z = self.inner_radius * math.sin(phi)
        glVertex3f(x, y, z)
