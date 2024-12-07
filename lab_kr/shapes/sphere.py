import math

from OpenGL.GL import *
from lab_kr.shapes.shape import Shape


class Sphere(Shape):
    def __init__(self, radius=1.0, stacks=20, slices=20, position=[0.0, 0.0, 0.0], scale=1.0,
                 rotation=[0.0, 0.0, 0.0], material=None):
        super().__init__(position, scale, rotation, material)
        self.radius = radius
        self.stacks = stacks
        self.slices = slices
        self.setup_mesh()

    def setup_mesh(self):
        """Создаём данные для сферы: вершины, нормали, текстурные координаты и индексы."""
        self.vertices = []
        self.indices = []

        # Создание вершин и текстурных координат
        for stack in range(self.stacks + 1):
            phi = math.pi * stack / self.stacks
            sin_phi = math.sin(phi)
            cos_phi = math.cos(phi)

            for slice in range(self.slices + 1):
                theta = 2.0 * math.pi * slice / self.slices
                sin_theta = math.sin(theta)
                cos_theta = math.cos(theta)

                # Координаты вершины
                x = self.radius * sin_phi * cos_theta
                y = self.radius * cos_phi
                z = self.radius * sin_phi * sin_theta

                # Нормаль (такая же, как координата вершины, но нормализованная)
                nx = sin_phi * cos_theta
                ny = cos_phi
                nz = sin_phi * sin_theta

                # Текстурные координаты
                u = slice / self.slices
                v = stack / self.stacks

                self.vertices.extend([x, y, z, nx, ny, nz, u, v])

        # Создание индексов
        for stack in range(self.stacks):
            for slice in range(self.slices):
                first = stack * (self.slices + 1) + slice
                second = first + self.slices + 1

                # Треугольники для текущего квадрата
                self.indices.extend([first, second, first + 1])
                self.indices.extend([second, second + 1, first + 1])

        self.vertices = (GLfloat * len(self.vertices))(*self.vertices)
        self.indices = (GLuint * len(self.indices))(*self.indices)

    def draw_mesh(self, shader):
        """Отрисовка сферы."""
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
