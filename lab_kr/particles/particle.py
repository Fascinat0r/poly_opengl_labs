# particles/particle.py
import glm

from OpenGL.GL import *
from lab_kr.particles.trail import Trail


class Particle:
    def __init__(self, position, velocity, size, color, lifetime, has_trail=True):
        self.position = glm.vec3(*position)
        self.velocity = glm.vec3(*velocity)
        self.size = size
        self.color = glm.vec4(*color)
        self.lifetime = lifetime
        self.age = 0.0
        self.has_trail = has_trail
        self.trail = Trail(self.position) if self.has_trail else None

    def update(self, delta_time, acceleration):
        self.velocity += glm.vec3(*acceleration) * delta_time
        self.position += self.velocity * delta_time
        self.age += delta_time
        if self.has_trail:
            self.trail.update(self.position)

    def is_alive(self):
        return self.age < self.lifetime

    def get_transparency(self):
        # Прозрачность уменьшается по мере старения
        return max(0.0, 1.0 - self.age / self.lifetime)

    def render(self, shader):
        shader.set_vec4("particleColor", glm.vec4(self.color.x, self.color.y, self.color.z, self.get_transparency()))
        # Рендер частицы как точки или квадрата
        glPointSize(self.size)
        glBegin(GL_POINTS)
        glVertex3f(self.position.x, self.position.y, self.position.z)
        glEnd()
        if self.has_trail:
            self.trail.render(shader)
