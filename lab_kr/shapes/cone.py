import math

import glm

from OpenGL.GL import *
from lab_kr.shapes.shape import Shape


class Cone(Shape):
    def __init__(self, base_radius=1.0, height=2.0, slices=30, position=[0.0, 0.0, 0.0], scale=1.0,
                 rotation=[0.0, 0.0, 0.0], material=None):
        super().__init__(position, scale, rotation, material=material)
        self.base_radius = base_radius
        self.height = height
        self.slices = slices
        self.setup_mesh()

    def setup_mesh(self):
        """Создаём данные для конуса: вершины, текстурные координаты и индексы."""
        self.vertices = []
        self.indices = []

        # Вершина конуса
        self.vertices.extend([0.0, self.height, 0.0, 0.0, 1.0, 0.0, 0.5, 1.0])  # Позиция, нормаль, UV (0.5, 1.0)

        # Базовые вершины и нормали
        for i in range(self.slices):
            theta = 2.0 * math.pi * i / self.slices
            x = self.base_radius * math.cos(theta)
            z = self.base_radius * math.sin(theta)

            # Нормаль для боковой грани
            side_normal = glm.normalize(glm.vec3(x, self.height, z))

            # Текстурные координаты UV
            u = i / self.slices
            v = 0.0

            self.vertices.extend([x, 0.0, z, side_normal.x, side_normal.y, side_normal.z, u, v])

        # Индексы боковых граней
        for i in range(1, self.slices + 1):
            next_i = 1 if i == self.slices else i + 1
            self.indices.extend([0, i, next_i])

        # Центр основания
        center_index = len(self.vertices) // 8  # Каждый вершинный атрибут состоит из 8 элементов
        self.vertices.extend([0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.5, 0.5])  # Центр основания: нормаль вниз, UV (0.5, 0.5)

        # Индексы основания
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
