from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image


class Texture:
    def __init__(self, texture_path):
        self.texture_path = texture_path
        self.texture_id = glGenTextures(1)

    def load(self):
        image = Image.open(self.texture_path)
        img_data = image.tobytes("raw", "RGB", 0, -1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glEnable(GL_TEXTURE_2D)

    def apply(self):
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
