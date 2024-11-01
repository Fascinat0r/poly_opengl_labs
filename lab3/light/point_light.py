from OpenGL.GL import *
from OpenGL.GLUT import *


class PointLight:
    def __init__(self, light_id, position=[0.0, 0.0, 1.0, 1.0],
                 ambient=[0.05, 0.05, 0.05, 1.0],
                 diffuse=[1.0, 1.0, 1.0, 1.0],
                 specular=[1.0, 1.0, 1.0, 1.0],
                 attenuation=[1.0, 0.1, 0.01]):
        """
        light_id: ID источника света (например, GL_LIGHT0).
        position: Позиция источника света [x, y, z, w]. w = 1 для точечного источника.
        ambient: Фоновое освещение.
        diffuse: Рассеянный свет.
        specular: Зеркальный свет.
        attenuation: Аттенюация (затухание света) [constant, linear, quadratic].
        """
        self.light_id = light_id
        self.position = position
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.attenuation = attenuation

    def apply(self):
        """Применение параметров точечного источника света."""
        glEnable(self.light_id)
        glLightfv(self.light_id, GL_POSITION, self.position)
        glLightfv(self.light_id, GL_AMBIENT, self.ambient)
        glLightfv(self.light_id, GL_DIFFUSE, self.diffuse)
        glLightfv(self.light_id, GL_SPECULAR, self.specular)

        # Задаем параметры затухания света
        glLightf(self.light_id, GL_CONSTANT_ATTENUATION, self.attenuation[0])
        glLightf(self.light_id, GL_LINEAR_ATTENUATION, self.attenuation[1])
        glLightf(self.light_id, GL_QUADRATIC_ATTENUATION, self.attenuation[2])

    def set_position(self, position):
        """Обновление позиции источника света."""
        self.position = position
        glLightfv(self.light_id, GL_POSITION, self.position)

    def draw_indicator(self):
        """Рисование индикатора источника света в виде маленькой сферы."""
        glPushMatrix()
        # Перемещаемся в позицию источника света
        glTranslatef(self.position[0], self.position[1], self.position[2])

        # Отключаем освещение, чтобы индикатор не подвергался влиянию света
        glDisable(GL_LIGHTING)

        # Рисуем маленькую сферу в месте источника света
        glColor3f(1.0, 1.0, 0.0)  # Желтый цвет для индикатора
        glutSolidSphere(0.1, 20, 20)  # Радиус 0.1, деление 20x20

        # Включаем освещение обратно
        glEnable(GL_LIGHTING)
        glPopMatrix()
