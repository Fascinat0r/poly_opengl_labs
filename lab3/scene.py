# scene.py
from math import sqrt

from OpenGL.GL import *
from OpenGL.GLUT import *
from lab3.light.point_light import PointLight
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

    def add_light(self, light: PointLight):
        """Добавляем источник света в сцену."""
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
        return sqrt((position[0] - cam_pos[0]) ** 2 +
                    (position[1] - cam_pos[1]) ** 2 +
                    (position[2] - cam_pos[2]) ** 2)

    def update_animations(self):
        """Обновление всех анимаций с учетом времени."""
        current_time = glutGet(GLUT_ELAPSED_TIME)
        delta_time = (current_time - self.last_update_time) / 1000.0
        self.last_update_time = current_time

        # Обновляем каждую анимацию, передавая delta_time
        for animation in self.animations:
            animation.update(animation.target_object, delta_time)

    def render_depth_map(self, shader: Shader):
        """Рендеринг сцены для создания карты глубины."""
        self.depth_map.bind_for_writing()
        glClear(GL_DEPTH_BUFFER_BIT)

        # Используем шейдер для глубины
        shader.use()

        # Настройка матриц для всех объектов
        for obj in self.objects:
            obj.render(shader)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def render_scene(self, shader: Shader):
        """Основной проход рендеринга сцены с тенями."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Устанавливаем матрицу вида и проекции от камеры
        shader.use()
        shader.set_mat4("view", self.camera.get_view_matrix())
        shader.set_mat4("projection", self.camera.get_projection_matrix())

        # Привязываем карту глубины как текстуру
        self.depth_map.bind_for_reading(unit=1)
        shader.set_int("shadowMap", 1)  # Текстурный блок 1

        # Устанавливаем позиции и цвет света
        for i, light in enumerate(self.lights):
            shader.set_vec3("lightPos", light.position[:3])  # Предполагаем, что light.position — это список
            shader.set_vec3("viewPos", self.camera.position)  # Исправлено: напрямую передаём glm.vec3
            shader.set_vec3("lightColor", light.diffuse[:3])

        # Рендерим все объекты
        for obj in self.objects:
            obj.render(shader)
