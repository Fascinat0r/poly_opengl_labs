import math

from OpenGL.GL import *
from lab3.shapes.shape import Shape


class Torus(Shape):
    def __init__(self, inner_radius=0.5, outer_radius=1.0, rings=30, sides=30,
                 position=[0.0, 0.0, 0.0], scale=1.0, rotation=[0.0, 0.0, 0.0], material=None):
        super().__init__(position, scale, rotation, material)
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.rings = rings
        self.sides = sides
        self.setup_mesh()

    def setup_mesh(self):
        """Создаём данные для тора: вершины и индексы."""
        self.vertices = []
        self.indices = []

        for ring in range(self.rings):
            theta = 2.0 * math.pi * ring / self.rings
            for side in range(self.sides):
                phi = 2.0 * math.pi * side / self.sides
                x = (self.outer_radius + self.inner_radius * math.cos(phi)) * math.cos(theta)
                y = (self.outer_radius + self.inner_radius * math.cos(phi)) * math.sin(theta)
                z = self.inner_radius * math.sin(phi)
                self.vertices.extend([x, y, z])

        for ring in range(self.rings):
            for side in range(self.sides):
                next_ring = (ring + 1) % self.rings
                next_side = (side + 1) % self.sides

                self.indices.extend([
                    ring * self.sides + side,
                    next_ring * self.sides + side,
                    ring * self.sides + next_side,
                    ring * self.sides + next_side,
                    next_ring * self.sides + side,
                    next_ring * self.sides + next_side
                ])

        self.vertices = (GLfloat * len(self.vertices))(*self.vertices)
        self.indices = (GLuint * len(self.indices))(*self.indices)

    def draw_mesh(self, shader):
        """Отрисовка тора."""
        glBindVertexArray(self.VAO)

        # VBO
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)

        # EBO
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices, GL_STATIC_DRAW)

        # Настройка атрибутов вершин
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), None)
        glEnableVertexAttribArray(0)

        # Отрисовка
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
