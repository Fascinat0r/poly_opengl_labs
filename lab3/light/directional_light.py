# lab3/light/directional_light.py
from lab3.materials.shader import Shader


class DirectionalLight:
    def __init__(self, direction, ambient=[0.05, 0.05, 0.05],
                 diffuse=[1.0, 1.0, 1.0],
                 specular=[1.0, 1.0, 1.0]):
        """
        :param direction: Направление света [x, y, z].
        :param ambient: Окружающий свет [R, G, B].
        :param diffuse: Рассеянный свет [R, G, B].
        :param specular: Зеркальный свет [R, G, B].
        """
        self.direction = direction
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular

    def apply(self, shader: Shader):
        """Передача параметров направленного света в шейдер."""
        shader.set_vec3("dirLight.direction", self.direction)
        shader.set_vec3("dirLight.ambient", self.ambient)
        shader.set_vec3("dirLight.diffuse", self.diffuse)
        shader.set_vec3("dirLight.specular", self.specular)
