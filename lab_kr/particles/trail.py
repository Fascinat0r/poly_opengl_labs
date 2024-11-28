# particles/trail.py
import glm

from OpenGL.GL import *


class Trail:
    def __init__(self, initial_position, length=5):
        self.positions = [glm.vec3(*initial_position)] * length
        self.length = length

    def update(self, new_position):
        self.positions.pop(0)
        self.positions.append(glm.vec3(*new_position))

    def render(self, shader):
        glBegin(GL_LINE_STRIP)
        for pos in self.positions:
            glVertex3f(pos.x, pos.y, pos.z)
        glEnd()
