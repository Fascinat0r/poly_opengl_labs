import math
from OpenGL.GL import *
from lab3.shapes.shape import Shape


class Cone(Shape):
    def __init__(self, base_radius=1.0, height=2.0, slices=30, position=[0.0, 0.0, 0.0], scale=1.0,
                 rotation=[0.0, 0.0, 0.0], material=None):
        super().__init__(position, scale, rotation, material=material)
        self.base_radius = base_radius
        self.height = height
        self.slices = slices
        self.setup_mesh()

    def setup_mesh(self):
        """Создаём данные для конуса: вершины и индексы."""
        self.vertices = []
        self.indices = []

        # Вершина конуса
        tip_index = 0
        self.vertices.extend([0.0, self.height, 0.0])

        # Базовые вершины
        for i in range(self.slices):
            theta = 2.0 * math.pi * i / self.slices
            x = self.base_radius * math.cos(theta)
            z = self.base_radius * math.sin(theta)
            self.vertices.extend([x, 0.0, z])

        # Индексы боковых граней
        for i in range(1, self.slices + 1):
            next_i = 1 if i == self.slices else i + 1
            self.indices.extend([tip_index, i, next_i])

        # Индексы основания
        center_index = len(self.vertices) // 3
        self.vertices.extend([0.0, 0.0, 0.0])  # Центр основания
        for i in range(1, self.slices + 1):
            next_i = 1 if i == self.slices else i + 1
            self.indices.extend([center_index, next_i, i])

        self.vertices = (GLfloat * len(self.vertices))(*self.vertices)
        self.indices = (GLuint * len(self.indices))(*self.indices)

    def draw_mesh(self, shader):
        """Отрисовка конуса."""
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
