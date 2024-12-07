# material.py
import OpenGL.GL as gl
from lab_kr.materials.shader import Shader


class Material:
    def __init__(self, ambient=[1.0, 1.0, 1.0], diffuse=[1.0, 1.0, 1.0],
                 specular=[1.0, 1.0, 1.0], shininess=32.0,
                 texture=None, transparent=False):
        """
        Конструктор материала.

        :param ambient: Окружающий цвет [R, G, B].
        :param diffuse: Рассеянный цвет [R, G, B].
        :param specular: Зеркальный цвет [R, G, B].
        :param shininess: Коэффициент блеска.
        :param texture: ID текстуры, если есть.
        :param transparent: Флаг прозрачности.
        """
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.texture = texture
        self.transparent = transparent

    def apply(self, shader: Shader):
        """Применение материала к шейдеру."""
        shader.set_vec3("material.ambient", self.ambient)
        shader.set_vec3("material.diffuse", self.diffuse)
        shader.set_vec3("material.specular", self.specular)
        shader.set_float("material.shininess", self.shininess)

        if self.texture:
            shader.set_int("diffuseTexture", 0)
            gl.glActiveTexture(gl.GL_TEXTURE0)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
        else:
            shader.set_int("diffuseTexture", 0)
            gl.glBindTexture(gl.GL_TEXTURE_2D, 0)  # Отключаем текстуру

    def cleanup(self, shader: Shader):
        """Очистка текстуры после рендеринга."""
        if self.texture:
            gl.glActiveTexture(gl.GL_TEXTURE0)
            gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
