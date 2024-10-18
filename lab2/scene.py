from OpenGL.GL import *
from OpenGL.GLUT import *


class Scene:
    def __init__(self):
        # Список объектов в сцене
        self.objects = []
        # Список анимаций, привязанных к объектам сцены
        self.animations = []
        # Время последней отрисовки сцены
        self.last_update_time = glutGet(GLUT_ELAPSED_TIME)

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

    def update_animations(self):
        """Обновление всех анимаций с учетом времени."""
        current_time = glutGet(GLUT_ELAPSED_TIME)
        delta_time = (current_time - self.last_update_time) / 1000.0
        self.last_update_time = current_time

        # Обновляем каждую анимацию, передавая delta_time
        for animation in self.animations:
            animation.update(animation.target_object, delta_time)
