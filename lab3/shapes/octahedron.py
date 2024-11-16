from OpenGL.GL import *
from lab3.shapes.shape import Shape


class Octahedron(Shape):
    def __init__(self, position=[0.0, 0.0, 0.0], scale=1.0, rotation=[0.0, 0.0, 0.0], material=None):
        super().__init__(position, scale, rotation, material)
        self.setup_mesh()

    def setup_mesh(self):
        """Создаём данные для октаэдра: вершины, нормали, текстурные координаты и индексы."""
        self.vertices = []
        self.indices = []

        # Вершины октаэдра с нормалями и текстурными координатами
        vertex_data = [
            # Позиция, Нормаль, UV
            [0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.5, 1.0],  # Top vertex
            [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.5],  # Right
            [0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.5, 0.5],  # Front
            [-1.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.5],  # Left
            [0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.5, 0.0],  # Back
            [0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.5, 0.0],  # Bottom vertex
        ]

        # Добавляем вершины в список
        for vertex in vertex_data:
            self.vertices.extend(vertex)

        # Индексы граней (треугольников)
        self.indices = [
            0, 1, 2,  # Top-Right-Front
            0, 2, 3,  # Top-Front-Left
            0, 3, 4,  # Top-Left-Back
            0, 4, 1,  # Top-Back-Right
            5, 2, 1,  # Bottom-Front-Right
            5, 3, 2,  # Bottom-Left-Front
            5, 4, 3,  # Bottom-Back-Left
            5, 1, 4  # Bottom-Right-Back
        ]

        self.vertices = (GLfloat * len(self.vertices))(*self.vertices)
        self.indices = (GLuint * len(self.indices))(*self.indices)

    def draw_mesh(self, shader):
        """Отрисовка октаэдра."""
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
