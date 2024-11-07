from math import sqrt

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from lab3.light.point_light import PointLight


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

        # Настраиваем проекционную матрицу
        glMatrixMode(GL_PROJECTION)
        # Сбрасываем матрицу
        glLoadIdentity()
        # Устанавливаем перспективу
        gluPerspective(45, 800 / 600, 0.1, 100.0)
        # Возвращаемся к модельной матрице
        glMatrixMode(GL_MODELVIEW)

    def set_camera(self, camera):
        """Устанавливаем камеру для сцены."""
        self.camera = camera

    def add_light(self, light: PointLight):
        """Добавляем источник света в сцену."""
        light.apply()
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

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Устанавливаем матрицу вида для камеры
        position, target, up = self.camera.get_view_matrix()
        gluLookAt(position[0], position[1], position[2], target[0], target[1], target[2], up[0], up[1], up[2])

        # Обновляем анимации в сцене
        self.update_animations()

        # Отрисовываем сетку и оси
        self.draw_grid()
        self.draw_axes()

        # Рисуем индикатор источника света
        for light in self.lights:
            light.draw_indicator()

        # Разделяем и сортируем объекты
        opaque_objects, transparent_objects = self.sort_objects()

        # Рендер непрозрачных объектов
        for obj in opaque_objects:
            obj.render()

        # Рендер прозрачных объектов в правильном порядке
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(GL_FALSE)  # Отключаем запись в буфер глубины для прозрачных объектов

        for obj in transparent_objects:
            obj.render()

        glDepthMask(GL_TRUE)  # Восстанавливаем запись в буфер глубины
        glDisable(GL_BLEND)

        glutSwapBuffers()

    def update_animations(self):
        """Обновление всех анимаций с учетом времени."""
        current_time = glutGet(GLUT_ELAPSED_TIME)
        delta_time = (current_time - self.last_update_time) / 1000.0
        self.last_update_time = current_time

        # Обновляем каждую анимацию, передавая delta_time
        for animation in self.animations:
            animation.update(animation.target_object, delta_time)
