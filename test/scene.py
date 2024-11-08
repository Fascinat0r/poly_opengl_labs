# scene.py
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *

from camera import Camera
from light import PointLight


class Scene:
    def __init__(self):
        # Настройка камеры
        self.camera = Camera(np.array([5.0, 5.0, 5.0]), np.array([0.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]))

        # Настройка света
        self.light = PointLight(np.array([3.0, 5.0, 2.0]))

        # Компиляция шейдеров
        self.shadow_shader = self.compile_shader("../data/shaders/shadow_vertex.glsl", "../data/shaders/shadow_fragment.glsl")
        self.main_shader = self.compile_shader("../data/shaders/scene_vertex.glsl", "../data/shaders/scene_fragment.glsl")

    def compile_shader(self, vertex_path, fragment_path):
        # Функция компиляции шейдера
        pass

    def render_shadow_pass(self):
        self.light.bind_for_shadow_pass()
        glUseProgram(self.shadow_shader)

        # Передаем матрицу lightSpaceMatrix
        light_projection = self.light_projection()
        light_view = self.light_view()
        light_space_matrix = np.dot(light_projection, light_view)
        glUniformMatrix4fv(glGetUniformLocation(self.shadow_shader, "lightSpaceMatrix"), 1, GL_FALSE,
                           light_space_matrix)

        # Рендерим объекты в shadow map
        self.render_objects()
        self.light.unbind_after_shadow_pass()

    def render_main_pass(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.main_shader)

        # Настройка матриц камеры
        projection_matrix = self.camera.get_projection_matrix(45, 800 / 600, 0.1, 100)
        view_matrix = self.camera.get_view_matrix()
        glUniformMatrix4fv(glGetUniformLocation(self.main_shader, "projection"), 1, GL_FALSE, projection_matrix)
        glUniformMatrix4fv(glGetUniformLocation(self.main_shader, "view"), 1, GL_FALSE, view_matrix)

        # Передаем lightSpaceMatrix и shadowMap
        light_projection = self.light_projection()
        light_view = self.light_view()
        light_space_matrix = np.dot(light_projection, light_view)
        glUniformMatrix4fv(glGetUniformLocation(self.main_shader, "lightSpaceMatrix"), 1, GL_FALSE, light_space_matrix)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.light.shadow_map)
        glUniform1i(glGetUniformLocation(self.main_shader, "shadowMap"), 1)

        # Отрисовка объектов
        self.render_objects()
        glutSwapBuffers()

    def light_projection(self):
        return np.array([
            [1.0 / 10, 0, 0, 0],
            [0, 1.0 / 10, 0, 0],
            [0, 0, -2 / (50 - 1), -(50 + 1) / (50 - 1)],
            [0, 0, 0, 1]
        ], dtype=np.float32)

    def light_view(self):
        return self.camera.get_view_matrix()  # или другой view_matrix для света

    def render_objects(self):
        # Здесь отрисовываем два куба
        pass
