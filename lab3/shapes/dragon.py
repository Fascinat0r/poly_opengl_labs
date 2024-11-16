import numpy as np
from stl import mesh

from OpenGL.GL import *
from lab3.shapes.shape import Shape


class Dragon(Shape):
    def __init__(self, position=[0.0, 0.0, 0.0], scale=1.0, rotation=[0.0, 0.0, 0.0], material=None):
        super().__init__(position, scale, rotation, material)
        self.stl_path = "../data/models/dragon.stl"
        self.setup_mesh()

    def setup_mesh(self):
        """Загружает STL модель и создаёт данные для отображения в OpenGL."""
        # Загружаем STL модель
        model = mesh.Mesh.from_file(self.stl_path)

        # Собираем вершины, нормали и индексы
        self.vertices = []
        self.indices = []

        for i, triangle in enumerate(model.vectors):
            normal = model.normals[i]
            for vertex in triangle:
                self.vertices.extend([*vertex, *normal, 0.0, 0.0])  # Добавляем временные UV
            self.indices.extend([i * 3, i * 3 + 1, i * 3 + 2])

        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.indices = np.array(self.indices, dtype=np.uint32)

        glBindVertexArray(self.VAO)

        # VBO
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # EBO
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        # Настройка атрибутов вершин
        # Позиции
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * self.vertices.itemsize, ctypes.c_void_p(0))
        # Нормали
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * self.vertices.itemsize,
                              ctypes.c_void_p(3 * self.vertices.itemsize))
        # Текстурные координаты
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * self.vertices.itemsize,
                              ctypes.c_void_p(6 * self.vertices.itemsize))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw_mesh(self, shader):
        """Отрисовка STL модели."""
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
