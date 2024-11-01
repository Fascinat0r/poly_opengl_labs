from OpenGL.GL import *
from OpenGL.GL.framebuffer import glGenFramebuffers, glBindFramebuffer, glFramebufferTexture2D
from OpenGL.GL.texture import glTexImage2D, glGenTextures

class ShadowMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.shadow_map_fbo = glGenFramebuffers(1)
        self.shadow_map_texture = glGenTextures(1)
        self.setup_shadow_map()

    def setup_shadow_map(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.shadow_map_fbo)
        glBindTexture(GL_TEXTURE_2D, self.shadow_map_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, self.width, self.height, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.shadow_map_texture, 0)
        glDrawBuffer(GL_NONE)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def render_shadow_map(self, light):
        glBindFramebuffer(GL_FRAMEBUFFER, self.shadow_map_fbo)
        glClear(GL_DEPTH_BUFFER_BIT)
        # Set up light's view and projection matrices, render scene
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
