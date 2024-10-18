from OpenGL.GL import *
from OpenGL.GLUT import *


class Material:
    def __init__(self, ambient=[0.2, 0.2, 0.2, 1.0], diffuse=[0.8, 0.8, 0.8, 1.0],
                 specular=[1.0, 1.0, 1.0, 1.0], shininess=32.0, transparency=1.0):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.transparency = transparency

    def apply(self):
        """Применение материала."""
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, self.ambient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.diffuse)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, self.specular)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, self.shininess)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE,
                     [self.diffuse[0], self.diffuse[1], self.diffuse[2], self.transparency])
