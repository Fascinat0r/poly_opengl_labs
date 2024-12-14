import math

import glm
from OpenGL.GL import *

from lab_kr.shapes.shape import Shape


class Cylinder(Shape):
    def __init__(self, base_radius=1.0, top_radius=1.0, height=2.0, slices=30,
                 position=[0.0, 0.0, 0.0], scale=1.0, rotation=[0.0, 0.0, 0.0], material=None):
        super().__init__(position, scale, rotation, material=material)
        self.base_radius = base_radius
        self.top_radius = top_radius
        self.height = height
        self.slices = slices
        self.setup_mesh()

    def setup_mesh(self):
        """Создаём данные для цилиндра: вершины, нормали, текстурные координаты и индексы."""
        self.vertices = []
        self.indices = []

        # Вершины боковой поверхности
        for i in range(self.slices):
            theta = 2.0 * math.pi * i / self.slices
            next_theta = 2.0 * math.pi * (i + 1) / self.slices

            # Нижняя окружность
            x1_base = self.base_radius * math.cos(theta)
            z1_base = self.base_radius * math.sin(theta)
            x2_base = self.base_radius * math.cos(next_theta)
            z2_base = self.base_radius * math.sin(next_theta)

            # Верхняя окружность
            x1_top = self.top_radius * math.cos(theta)
            z1_top = self.top_radius * math.sin(theta)
            x2_top = self.top_radius * math.cos(next_theta)
            z2_top = self.top_radius * math.sin(next_theta)

            # Нормали для боковой поверхности
            normal1 = glm.normalize(glm.vec3(x1_base, 0.0, z1_base))
            normal2 = glm.normalize(glm.vec3(x2_base, 0.0, z2_base))

            # Текстурные координаты
            u1 = i / self.slices
            u2 = (i + 1) / self.slices
            v_base = 0.0
            v_top = 1.0

            # Добавляем вершины (нижняя и верхняя точки текущего сегмента)
            self.vertices.extend([x1_base, 0.0, z1_base, normal1.x, normal1.y, normal1.z, u1, v_base])
            self.vertices.extend([x1_top, self.height, z1_top, normal1.x, normal1.y, normal1.z, u1, v_top])

            self.vertices.extend([x2_base, 0.0, z2_base, normal2.x, normal2.y, normal2.z, u2, v_base])
            self.vertices.extend([x2_top, self.height, z2_top, normal2.x, normal2.y, normal2.z, u2, v_top])

            # Индексы для двух треугольников текущего сегмента
            base_index = i * 4
            self.indices.extend([
                base_index, base_index + 1, base_index + 2,
                            base_index + 2, base_index + 1, base_index + 3
            ])

        # Центр нижней окружности
        base_center_index = len(self.vertices) // 8
        self.vertices.extend([0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.5, 0.5])

        # Вершины нижней окружности
        for i in range(self.slices):
            theta = 2.0 * math.pi * i / self.slices
            x = self.base_radius * math.cos(theta)
            z = self.base_radius * math.sin(theta)
            uv = [0.5 + 0.5 * math.cos(theta), 0.5 + 0.5 * math.sin(theta)]
            self.vertices.extend([x, 0.0, z, 0.0, -1.0, 0.0, uv[0], uv[1]])

        # Индексы для нижней окружности
        for i in range(1, self.slices + 1):
            next_i = 1 if i == self.slices else i + 1
            self.indices.extend([base_center_index, base_center_index + i, base_center_index + next_i])

        # Центр верхней окружности
        top_center_index = len(self.vertices) // 8
        self.vertices.extend([0.0, self.height, 0.0, 0.0, 1.0, 0.0, 0.5, 0.5])

        # Вершины верхней окружности
        for i in range(self.slices):
            theta = 2.0 * math.pi * i / self.slices
            x = self.top_radius * math.cos(theta)
            z = self.top_radius * math.sin(theta)
            uv = [0.5 + 0.5 * math.cos(theta), 0.5 + 0.5 * math.sin(theta)]
            self.vertices.extend([x, self.height, z, 0.0, 1.0, 0.0, uv[0], uv[1]])

        # Индексы для верхней окружности
        for i in range(1, self.slices + 1):
            next_i = 1 if i == self.slices else i + 1
            self.indices.extend([top_center_index, top_center_index + next_i, top_center_index + i])

        self.vertices = (GLfloat * len(self.vertices))(*self.vertices)
        self.indices = (GLuint * len(self.indices))(*self.indices)

    def draw_mesh(self, shader):
        """Отрисовка цилиндра."""
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
