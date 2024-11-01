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

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        position, target, up = self.camera.get_view_matrix()
        gluLookAt(position[0], position[1], position[2], target[0], target[1], target[2], up[0], up[1], up[2])

        # Обновляем анимации в сцене
        self.update_animations()

        # Включаем режим прозрачности
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Включаем глубинный тест
        glEnable(GL_DEPTH_TEST)

        # Включаем запись в буфер глубины снова
        glDepthMask(GL_TRUE)

        # Рисуем индикатор источника света
        for light in self.lights:
            light.draw_indicator()

        # Render opaque objects first
        for obj in self.objects:
            if not obj.material or obj.material.transparency == 1.0:
                obj.render()

        # Then render transparent objects
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(GL_FALSE)  # Disable depth buffer writing
        for obj in self.objects:
            if obj.material and obj.material.transparency < 1.0:
                obj.render()

        glDepthMask(GL_TRUE)  # Re-enable depth buffer writing
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
