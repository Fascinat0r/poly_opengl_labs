# particles/particle.py
import glm
from OpenGL.GL import *

from lab_kr.particles.trail import Trail


class Particle:
    def __init__(self, position, velocity, size, color, lifetime,
                 color_fading=False, transparency_radius=None, has_trail=False):
        self.start_position = glm.vec3(*position)
        self.position = glm.vec3(*position)
        self.velocity = glm.vec3(*velocity)
        self.size = size
        # Нормализуем цвет, если он задан в диапазоне [0, 255]
        self.color = glm.vec4(color[0], color[1], color[2], color[3])
        self.lifetime = lifetime
        self.age = 0.0
        self.color_fading = color_fading
        self.transparency_radius = transparency_radius
        self.has_trail = has_trail
        self.trail = Trail(self.position, 16) if self.has_trail else None

    def update(self, delta_time, acceleration):
        # Обновляем позицию и находим новую скорость
        self.position += self.velocity * delta_time + glm.vec3(*acceleration) * (delta_time ** 2) / 2
        self.velocity += glm.vec3(*acceleration) * delta_time

        self.age += delta_time

        # Обновляем след, если он есть
        if self.has_trail:
            self.trail.update(self.position)

    def is_alive(self):
        return self.age < self.lifetime

    def get_transparency(self):
        """
        Прозрачность уменьшается либо по мере старения, либо по мере удаления от эмиттера, если
        задан максимальный радиус удаления от эмиттера.
        """
        if self.transparency_radius is None:
            return max(0.0, 1.0 - self.age / self.lifetime)
        elif self.transparency_radius != 0.0:
            return max(0.0, 1.0 - glm.length(self.start_position - self.position) / self.transparency_radius)
        else:
            return 0.0

    def get_color(self):
        """Цвет затухает со временем жизни, если указан параметр для такого поведения."""
        if self.color_fading:
            return [
                self.color.x - self.color.x / self.lifetime * self.age,
                self.color.y - self.color.y / self.lifetime * self.age,
                self.color.z - self.color.z / self.lifetime * self.age,
            ]
        else:
            return [self.color.x, self.color.y, self.color.z]


    def render(self, shader):
        # Устанавливаем цвет частицы с текущей прозрачностью
        shader.set_vec4('particleColor', glm.vec4(*self.get_color(), self.get_transparency()))
        # Устанавливаем размер точки
        glPointSize(self.size)
        # Рендерим частицу как точку
        glBegin(GL_POINTS)
        glVertex3f(self.position.x, self.position.y, self.position.z)
        glEnd()
        # Рендерим след, если он есть
        if self.has_trail:
            self.trail.render(shader)
