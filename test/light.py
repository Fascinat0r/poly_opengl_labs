# light.py
from OpenGL.GL import *
import numpy as np

class PointLight:
    def __init__(self, position, shadow_map_size=1024):
        self.position = position
        self.shadow_map_size = shadow_map_size

        # Создаем FBO для теневой карты
        self.shadow_fbo = glGenFramebuffers(1)
        self.shadow_map = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.shadow_map)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, shadow_map_size, shadow_map_size, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, np.array([1.0, 1.0, 1.0, 1.0]))

        glBindFramebuffer(GL_FRAMEBUFFER, self.shadow_fbo)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.shadow_map, 0)
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def bind_for_shadow_pass(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.shadow_fbo)
        glViewport(0, 0, self.shadow_map_size, self.shadow_map_size)
        glClear(GL_DEPTH_BUFFER_BIT)

    def unbind_after_shadow_pass(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
