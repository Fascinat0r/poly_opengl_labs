# scene.py
from math import sqrt

import glm

from OpenGL.GL import *
from OpenGL.GLUT import *
from lab3.light.directional_light import DirectionalLight  # Импортируйте новый класс
from lab3.materials.depth_map import DepthMap
from lab3.materials.shader import Shader


class Scene:
    def __init__(self):
        # Камера сцены
        self.camera = None

        # Свет в сцене
        self.lights = []

        # Список объектов в сцене
        self.objects = []
        # Список анимаций, привязанных к объектам сцены
        self.animations = []
        # Время последней отрисовки сцены
        self.last_update_time = glutGet(GLUT_ELAPSED_TIME)

        # Настраиваем темную сцену
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Фоновый черный цвет

        # Создаем карту глубины для теней
        self.depth_map = DepthMap()
        self.depth_map.width = 1024
        self.depth_map.height = 1024

    def set_camera(self, camera):
        """Устанавливаем камеру для сцены."""
        self.camera = camera

    def add_light(self, light: DirectionalLight):  # Измените тип
        """Добавляем направленный источник света в сцену."""
        self.lights.append(light)

    def add_object(self, obj):
        """Добавляем объекты (кубы, конусы и т.д.) в сцену."""
        self.objects.append(obj)

    def add_animation(self, animation):
        """Добавляем анимацию в сцену."""
        self.animations.append(animation)

    def draw_axes(self):
        """Отрисовка осей координат."""
        glBegin(GL_LINES)

        # Оси
        glColor3f(1, 0, 0)  # Ось X
        glVertex3f(-10.0, 0.0, 0.0)
        glVertex3f(10.0, 0.0, 0.0)

        glColor3f(0, 1, 0)  # Ось Y
        glVertex3f(0.0, -10.0, 0.0)
        glVertex3f(0.0, 10.0, 0.0)

        glColor3f(0, 0, 1)  # Ось Z
        glVertex3f(0.0, 0.0, -10.0)
        glVertex3f(0.0, 0.0, 10.0)

        glEnd()

    def draw_grid(self):
        """Отрисовка сетки."""
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_LINES)

        for i in range(-10, 11):
            glVertex3f(i, 0, -10)
            glVertex3f(i, 0, 10)
            glVertex3f(-10, 0, i)
            glVertex3f(10, 0, i)

        glEnd()

    def sort_objects(self):
        """Разделяет объекты на непрозрачные и прозрачные и сортирует прозрачные по расстоянию до камеры."""
        opaque_objects = [obj for obj in self.objects if not obj.material.transparent]
        transparent_objects = [obj for obj in self.objects if obj.material.transparent]

        # Сортируем прозрачные объекты по убыванию расстояния до камеры
        transparent_objects.sort(key=lambda obj: -self.distance_to_camera(obj.position))

        return opaque_objects, transparent_objects

    def distance_to_camera(self, position):
        """Вычисляет расстояние от позиции до камеры."""
        cam_pos = self.camera.position
        return sqrt((position[0] - cam_pos.x) ** 2 +
                    (position[1] - cam_pos.y) ** 2 +
                    (position[2] - cam_pos.z) ** 2)

    def update_animations(self):
        """Обновление всех анимаций с учетом времени."""
        current_time = glutGet(GLUT_ELAPSED_TIME)
        delta_time = (current_time - self.last_update_time) / 1000.0
        self.last_update_time = current_time

        # Обновляем каждую анимацию, передавая delta_time
        for animation in self.animations:
            animation.update(animation.target_object, delta_time)

    def render_depth_map(self, depth_shader: Shader):
        """Рендеринг сцены для создания карты глубины."""
        self.depth_map.bind_for_writing()
        glClear(GL_DEPTH_BUFFER_BIT)

        depth_shader.use()

        if not self.lights:
            print("No lights in the scene for depth map.")
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
        depth_shader.set_mat4("lightSpaceMatrix", light_space_matrix)

        # Рендерим все объекты
        for obj in self.objects:
            obj.render(depth_shader)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def render_scene(self, shader: Shader):
        """Основной проход рендеринга сцены с тенями."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Устанавливаем матрицу вида и проекции от камеры
        shader.use()
        shader.set_mat4("view", self.camera.get_view_matrix())
        shader.set_mat4("projection", self.camera.get_projection_matrix())

        if not self.lights:
            print("No lights added to the scene.")
            return

        # Предполагаем, что у нас один направленный свет
        light = self.lights[0]

        # Настраиваем lightSpaceMatrix на основе направления света
        light_projection = glm.ortho(-10.0, 10.0, -10.0, 10.0, 1.0, 20.0)
        light_dir = glm.normalize(glm.vec3(*light.direction))
        light_position = glm.vec3(-light_dir.x * 10.0, -light_dir.y * 10.0, -light_dir.z * 10.0)
        light_view = glm.lookAt(light_position, glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))
        light_space_matrix = light_projection * light_view
        shader.set_mat4("lightSpaceMatrix", light_space_matrix)

        # Передаём параметры направленного света
        light.apply(shader)
        shader.set_vec3("viewPos", self.camera.position)

        # Привязываем карту глубины
        self.depth_map.bind_for_reading(unit=1)
        shader.set_int("shadowMap", 1)

        # Рендерим объекты
        for obj in self.objects:
            obj.render(shader)
