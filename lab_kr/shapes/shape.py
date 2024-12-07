# shape.py
from abc import ABC, abstractmethod

import glm

from OpenGL.GL import *
from lab_kr.materials.material import Material
from lab_kr.materials.shader import Shader


class Shape(ABC):
    def __init__(self, position, scale, rotation, material=None):
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.material = material if material else Material()

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)  # Для индексированных данных, если необходимо

    @abstractmethod
    def setup_mesh(self):
        """Настройка VAO, VBO, EBO для геометрии."""
        pass

    @abstractmethod
    def draw_mesh(self, shader: Shader):
        """Отрисовка геометрии с использованием шейдера."""
        pass

    def render(self, shader: Shader):
        """Отрисовка фигуры с применением трансформаций и материала."""
        # Создаем матрицу модели
        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(*self.position))
        model = glm.rotate(model, glm.radians(self.rotation[0]), glm.vec3(1.0, 0.0, 0.0))
        model = glm.rotate(model, glm.radians(self.rotation[1]), glm.vec3(0.0, 1.0, 0.0))
        model = glm.rotate(model, glm.radians(self.rotation[2]), glm.vec3(0.0, 0.0, 1.0))
        model = glm.scale(model, glm.vec3(self.scale))

        shader.set_mat4("model", model)

        # Применяем материал
        self.material.apply(shader)

        # Отрисовка геометрии
        self.draw_mesh(shader)

        # Очистка материала
        self.material.cleanup(shader)
