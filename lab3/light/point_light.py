# point_light.py
from OpenGL.GL import *
from OpenGL.GLUT import *
from lab3.materials.shader import Shader


class PointLight:
    def __init__(self, position=[0.0, 0.0, 1.0],
                 ambient=[0.05, 0.05, 0.05],
                 diffuse=[1.0, 1.0, 1.0],
                 specular=[1.0, 1.0, 1.0],
                 attenuation=[1.0, 0.09, 0.032]):
        """
        :param position: Позиция источника света [x, y, z].
        :param ambient: Окружающий свет [R, G, B].
        :param diffuse: Рассеянный свет [R, G, B].
        :param specular: Зеркальный свет [R, G, B].
        :param attenuation: Аттенюация [constant, linear, quadratic].
        """
        self.position = position
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.attenuation = attenuation

    def apply(self, shader: Shader, index: int):
        """Передача параметров света в шейдер."""
        shader.set_vec3(f"lights[{index}].position", self.position)
        shader.set_vec3(f"lights[{index}].ambient", self.ambient)
        shader.set_vec3(f"lights[{index}].diffuse", self.diffuse)
        shader.set_vec3(f"lights[{index}].specular", self.specular)
        shader.set_float(f"lights[{index}].constant", self.attenuation[0])
        shader.set_float(f"lights[{index}].linear", self.attenuation[1])
        shader.set_float(f"lights[{index}].quadratic", self.attenuation[2])

    def draw_indicator(self):
        """Рисование индикатора источника света в виде маленькой сферы."""
        glPushMatrix()
        # Перемещаемся в позицию источника света
        glTranslatef(*self.position)

        # Отключаем освещение, чтобы индикатор не подвергался влиянию света
        glDisable(GL_LIGHTING)

        # Рисуем маленькую сферу в месте источника света того же цвета, что и сам источник
        glColor3f(*self.diffuse)
        glutSolidSphere(0.1, 20, 20)  # Радиус 0.1, деление 20x20

        # Включаем освещение обратно
        glEnable(GL_LIGHTING)
        glPopMatrix()

    def set_position(self, position):
        self.position = position
