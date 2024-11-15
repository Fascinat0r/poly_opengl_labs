# cube.py
import numpy as np

from OpenGL.GL import *
from lab3.materials.shader import Shader
from lab3.shapes.shape import Shape


class Cube(Shape):
    def __init__(self, position=[0.0, 0.0, 0.0], scale=1.0, rotation=[0.0, 0.0, 0.0],
                 material=None):
        super().__init__(position, scale, rotation, material)
        self.vertices = [
            # positions        normals         texcoords
            -0.5, -0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 0.0,  # Front face
            0.5, -0.5, 0.5, 0.0, 0.0, 1.0, 1.0, 0.0,
            0.5, 0.5, 0.5, 0.0, 0.0, 1.0, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0, -1.0, 0.0, 0.0,  # Back face
            0.5, -0.5, -0.5, 0.0, 0.0, -1.0, 1.0, 0.0,
            0.5, 0.5, -0.5, 0.0, 0.0, -1.0, 1.0, 1.0,
            -0.5, 0.5, -0.5, 0.0, 0.0, -1.0, 0.0, 1.0,

            -0.5, 0.5, 0.5, -1.0, 0.0, 0.0, 1.0, 0.0,  # Left face
            -0.5, 0.5, -0.5, -1.0, 0.0, 0.0, 1.0, 1.0,
            -0.5, -0.5, -0.5, -1.0, 0.0, 0.0, 0.0, 1.0,
            -0.5, -0.5, 0.5, -1.0, 0.0, 0.0, 0.0, 0.0,

            0.5, 0.5, 0.5, 1.0, 0.0, 0.0, 1.0, 0.0,  # Right face
            0.5, 0.5, -0.5, 1.0, 0.0, 0.0, 1.0, 1.0,
            0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0.0, 1.0,
            0.5, -0.5, 0.5, 1.0, 0.0, 0.0, 0.0, 0.0,

            -0.5, -0.5, -0.5, 0.0, -1.0, 0.0, 0.0, 1.0,  # Bottom face
            0.5, -0.5, -0.5, 0.0, -1.0, 0.0, 1.0, 1.0,
            0.5, -0.5, 0.5, 0.0, -1.0, 0.0, 1.0, 0.0,
            -0.5, -0.5, 0.5, 0.0, -1.0, 0.0, 0.0, 0.0,

            -0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 1.0,  # Top face
            0.5, 0.5, -0.5, 0.0, 1.0, 0.0, 1.0, 1.0,
            0.5, 0.5, 0.5, 0.0, 1.0, 0.0, 1.0, 0.0,
            -0.5, 0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 0.0,
        ]
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.indices = [
            0, 1, 2, 2, 3, 0,  # Front face
            4, 5, 6, 6, 7, 4,  # Back face
            8, 9, 10, 10, 11, 8,  # Left face
            12, 13, 14, 14, 15, 12,  # Right face
            16, 17, 18, 18, 19, 16,  # Bottom face
            20, 21, 22, 22, 23, 20  # Top face
        ]
        self.indices = np.array(self.indices, dtype=np.uint32)

        self.setup_mesh()

    def setup_mesh(self):
        """Настройка VAO, VBO и EBO для куба."""
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
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * self.vertices.itemsize,
                              ctypes.c_void_p(3 * self.vertices.itemsize))
        # Текстурные координаты
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * self.vertices.itemsize,
                              ctypes.c_void_p(6 * self.vertices.itemsize))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw_mesh(self, shader: Shader):
        """Отрисовка куба с использованием шейдера."""
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
