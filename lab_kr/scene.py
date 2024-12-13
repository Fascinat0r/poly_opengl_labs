# scene.py
from typing import List

import glm
from OpenGL.GL import *
from OpenGL.GLUT import *

from lab_kr.light.directional_light import DirectionalLight
from lab_kr.materials.depth_map import DepthMap
from lab_kr.materials.shader import Shader
from lab_kr.particles.anti_attractor import AntiAttractorHandler
from lab_kr.particles.particle_system import ParticleSystem
from lab_kr.shapes.shape import Shape


class Scene:
    def __init__(self):
        # Камера сцены
        self.camera = None

        # Свет в сцене
        self.lights: List[DirectionalLight] = []

        # Список объектов в сцене
        self.objects: List[Shape] = []

        # Система частиц в сцене
        self.particle_system = None
        # Время последней отрисовки сцены
        self.last_update_time = glutGet(GLUT_ELAPSED_TIME)

        # Настраиваем задний фон как небо
        glClearColor(135.0 / 255.0, 206.0 / 255.0, 235.0 / 255.0, 1.0)  # Фоновый голубой цвет

        # Создаем карту глубины для теней
        self.depth_map = DepthMap()
        self.depth_map.width = 1024
        self.depth_map.height = 1024

    def set_camera(self, camera):
        """Устанавливаем камеру для сцены."""
        self.camera = camera

    def add_light(self, light: DirectionalLight):
        """Добавляем направленный источник света в сцену."""
        self.lights.append(light)

    def add_object(self, obj):
        """Добавляем объекты (кубы, конусы и т.д.) в сцену."""
        self.objects.append(obj)

    def get_delta_time(self):
        current_time = glutGet(GLUT_ELAPSED_TIME)
        delta_time = (current_time - self.last_update_time) / 1000.0
        self.last_update_time = current_time
        return delta_time

    def update_animations(self):
        """Обновление всех анимаций с учетом времени."""
        delta_time = self.get_delta_time()

        if self.particle_system:
            self.particle_system.update(delta_time)

    def render_depth_map(self, depth_shader: Shader):
        """Рендеринг сцены для создания карты глубины."""
        self.depth_map.bind_for_writing()
        glClear(GL_DEPTH_BUFFER_BIT)

        depth_shader.use()

        if not self.lights:
            print('No lights in the scene for depth map.')
            return

        # Предполагаем, что у нас один направленный свет
        light = self.lights[0]

        # Настраиваем lightSpaceMatrix на основе направления света.
        # Используем ортографическую проекцию для направленного света
        light_projection = glm.ortho(-10.0, 10.0, -10.0, 10.0, 1.0, 20.0)
        # Направление света
        light_dir = glm.normalize(glm.vec3(*light.direction))
        # Создаём матрицу вида из направления света
        # Для направленного света позиция может быть удалена, например, позиция = -light_dir * некоторый масштаб
        light_position = glm.vec3(-light_dir.x * 10.0, -light_dir.y * 10.0, -light_dir.z * 10.0)
        light_view = glm.lookAt(light_position, glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))
        light_space_matrix = light_projection * light_view
        depth_shader.set_mat4('lightSpaceMatrix', light_space_matrix)

        # Рендерим все объекты
        for obj in self.objects:
            obj.render(depth_shader)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def render_scene(self, shader: Shader):
        """Основной проход рендеринга сцены с тенями."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Устанавливаем матрицу вида и проекции от камеры
        shader.use()
        shader.set_mat4('view', self.camera.get_view_matrix())
        shader.set_mat4('projection', self.camera.get_projection_matrix())

        if not self.lights:
            print('No lights added to the scene.')
            return

        # Предполагаем, что у нас один направленный свет
        light = self.lights[0]

        # Настраиваем lightSpaceMatrix на основе направления света
        light_projection = glm.ortho(-10.0, 10.0, -10.0, 10.0, 1.0, 20.0)
        light_dir = glm.normalize(glm.vec3(*light.direction))
        light_position = glm.vec3(-light_dir.x * 10.0, -light_dir.y * 10.0, -light_dir.z * 10.0)
        light_view = glm.lookAt(light_position, glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))
        light_space_matrix = light_projection * light_view
        shader.set_mat4('lightSpaceMatrix', light_space_matrix)

        # Передаём параметры направленного света
        light.apply(shader)
        shader.set_vec3('viewPos', self.camera.position)

        # Привязываем карту глубины
        self.depth_map.bind_for_reading(unit=1)
        shader.set_int('shadowMap', 1)

        # Рендерим объекты
        for obj in self.objects:
            obj.render(shader)

    def initialize_particle_system(self, range_of_effect=5.0):
        anti_attractor_handler = AntiAttractorHandler(self.objects, range_of_effect)
        self.particle_system = ParticleSystem(anti_attractor_handler)

    def add_emitter_to_particle_system(self, emitter):
        if self.particle_system is None:
            self.initialize_particle_system()
        self.particle_system.add_emitter(emitter)
