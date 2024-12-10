# point.py
import glm
from OpenGL.GL import *
from lab_kr.materials.shader import Shader
from lab_kr.shapes.shape import Shape


class Point(Shape):
    def __init__(self, position=[0.0, 0.0, 0.0], size=10.0, color=[1.0, 1.0, 1.0, 1.0]):
        """
        Класс, представляющий точку на сцене.
        :param position: Позиция точки [x, y, z].
        :param size: Размер точки.
        :param color: Цвет точки [R, G, B, A] в диапазоне [0.0, 1.0].
        """
        super().__init__(position, scale=1.0, rotation=[0.0, 0.0, 0.0], material=None)
        self.size = size
        self.color = glm.vec4(color[0], color[1], color[2], color[3])

    def setup_mesh(self):
        """Для точки не требуется создавать VAO, VBO или EBO, так как это одиночная вершина."""
        pass

    def draw_mesh(self, shader: Shader):
        """Отрисовка точки с использованием шейдера."""
        glPointSize(self.size)  # Устанавливаем размер точки
        glBegin(GL_POINTS)
        glColor4f(self.color.r, self.color.g, self.color.b, self.color.a)  # Устанавливаем цвет точки
        glVertex3f(self.position[0], self.position[1], self.position[2])  # Позиция точки
        glEnd()

    def render(self, shader: Shader):
        """Отрисовка точки. Учитываются только позиция и цвет, без трансформаций."""
        self.draw_mesh(shader)
