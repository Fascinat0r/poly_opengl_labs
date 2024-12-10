# particles/particle.py
import glm

from OpenGL.GL import *
from lab_kr.particles.trail import Trail


class Particle:
    def __init__(self, position, velocity, size, color, lifetime, has_trail=True):
        self.position = glm.vec3(*position)
        self.velocity = glm.vec3(*velocity)
        self.size = size
        # Нормализуем цвет, если он задан в диапазоне [0, 255]
        self.color = glm.vec4(color[0], color[1], color[2], color[3])
        self.lifetime = lifetime
        self.age = 0.0
        self.has_trail = has_trail
        self.trail = Trail(self.position) if self.has_trail else None

        # Рассчитываем, на сколько уменьшать скорость при каждом обновлении
        self.speed_increment = 10 * glm.length(self.velocity) / self.lifetime


    def update(self, delta_time, acceleration):
        self.color = self.color + glm.vec4(0, 1 * delta_time, 0, 0)

        self.velocity += glm.vec3(*acceleration) * delta_time
        current_speed = glm.length(self.velocity)
        new_speed = max(0, current_speed + self.speed_increment * delta_time)
        self.velocity = glm.normalize(self.velocity) * new_speed
        self.position += self.velocity * delta_time
        self.age += delta_time
        if self.has_trail:
            self.trail.update(self.position)

        # Обновляем позицию
        self.position += self.velocity * delta_time
        self.age += delta_time

        # Обновляем след, если он есть
        if self.has_trail:
            self.trail.update(self.position)

    def is_alive(self):
        return self.age < self.lifetime

    def render(self, shader):
        # Устанавливаем цвет частицы с текущей прозрачностью
        shader.set_vec4("particleColor", glm.vec4(self.color.x, self.color.y, self.color.z, self.color.w))
        # Устанавливаем размер точки
        glPointSize(self.size)
        # Рендерим частицу как точку
        glBegin(GL_POINTS)
        glVertex3f(self.position.x, self.position.y, self.position.z)
        glEnd()
        # Рендерим след, если он есть
        if self.has_trail:
            self.trail.render(shader)
