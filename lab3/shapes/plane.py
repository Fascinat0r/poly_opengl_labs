# plane.py
import numpy as np
from OpenGL.GL import *
from lab3.shapes.shape import Shape


class Plane(Shape):
    def __init__(self, position=[0.0, 0.0, 0.0], scale=1.0, rotation=[0.0, 0.0, 0.0], material=None):
        super().__init__(position, scale, rotation, material)
        self.vertices = [
            # positions         normals         texcoords
            -0.5, 0.0, -0.5,   0.0, 1.0, 0.0,  0.0, 0.0,  # Bottom-left
             0.5, 0.0, -0.5,   0.0, 1.0, 0.0,  1.0, 0.0,  # Bottom-right
             0.5, 0.0,  0.5,   0.0, 1.0, 0.0,  1.0, 1.0,  # Top-right
            -0.5, 0.0,  0.5,   0.0, 1.0, 0.0,  0.0, 1.0   # Top-left
        ]
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.indices = [
            0, 1, 2,  # First triangle
            2, 3, 0   # Second triangle
        ]
        self.indices = np.array(self.indices, dtype=np.uint32)

        self.setup_mesh()

    def setup_mesh(self):
        """Настройка VAO, VBO и EBO для плоскости."""
        glBindVertexArray(self.VAO)

        # VBO
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # EBO
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        # Атрибуты вершин
        # Позиции
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * self.vertices.itemsize, ctypes.c_void_p(0))
        # Нормали
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * self.vertices.itemsize, ctypes.c_void_p(3 * self.vertices.itemsize))
        # Текстурные координаты
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * self.vertices.itemsize, ctypes.c_void_p(6 * self.vertices.itemsize))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw_mesh(self, shader):
        """Отрисовка плоскости с использованием шейдера."""
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
