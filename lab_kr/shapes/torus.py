import math

from OpenGL.GL import *
from lab_kr.shapes.shape import Shape


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
        """Создаём данные для тора: вершины, нормали, текстурные координаты и индексы."""
        self.vertices = []
        self.indices = []

        for ring in range(self.rings):
            theta = 2.0 * math.pi * ring / self.rings
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            for side in range(self.sides):
                phi = 2.0 * math.pi * side / self.sides
                cos_phi = math.cos(phi)
                sin_phi = math.sin(phi)

                # Вычисляем позицию вершины
                x = (self.outer_radius + self.inner_radius * cos_phi) * cos_theta
                y = (self.outer_radius + self.inner_radius * cos_phi) * sin_theta
                z = self.inner_radius * sin_phi

                # Вычисляем нормаль
                nx = cos_phi * cos_theta
                ny = cos_phi * sin_theta
                nz = sin_phi

                # Вычисляем текстурные координаты
                u = ring / self.rings
                v = side / self.sides

                self.vertices.extend([x, y, z, nx, ny, nz, u, v])

        for ring in range(self.rings):
            for side in range(self.sides):
                next_ring = (ring + 1) % self.rings
                next_side = (side + 1) % self.sides

                # Индексы для текущего и следующего кольца и сегмента
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
        # Позиции
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(0))
        # Нормали
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(3 * sizeof(GLfloat)))
        # Текстурные координаты
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(6 * sizeof(GLfloat)))

        # Отрисовка
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
