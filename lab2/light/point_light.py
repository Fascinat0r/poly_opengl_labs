import colorsys

from OpenGL.GL import *
from OpenGL.GLUT import *

ids = [GL_LIGHT0, GL_LIGHT1, GL_LIGHT2, GL_LIGHT3, GL_LIGHT4, GL_LIGHT5, GL_LIGHT6, GL_LIGHT7]
next_id = 0


class PointLight:
    def __init__(self, position=[0.0, 0.0, 1.0, 1.0],
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
        global next_id
        self.light_id = ids[next_id]
        next_id += 1
        self.position = position
        self.ambient = ambient.copy()
        self.diffuse = diffuse.copy()
        self.specular = specular.copy()
        self.attenuation = attenuation

        # HSV параметры
        self.hue = 0.0  # Начальный оттенок
        self.saturation = 0.0  # Начальная насыщенность
        self.value = 1.0  # Полная яркость
        self.step = 0.01  # Шаг изменения
        self.direction = 1  # Направление изменения

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
        r, g, b = colorsys.hsv_to_rgb(self.hue, self.saturation, self.value)
        glColor3f(r, g, b)
        glutSolidSphere(0.1, 20, 20)  # Радиус 0.1, деление 20x20

        # Включаем освещение обратно
        glEnable(GL_LIGHTING)
        glPopMatrix()

    def change_color(self):
        """
        Изменение цвета источника света по кольцу HSV.
        """
        # Обновляем оттенок
        self.saturation += self.step
        if self.saturation > 1.0 and self.direction == 1:
            self.saturation = 1.0
            self.direction = -1
        elif self.saturation < 0.0 and self.direction == -1:
            self.saturation = 0.0
            self.direction = 1
        # Преобразуем HSV -> RGB
        r, g, b = colorsys.hsv_to_rgb(self.hue, self.saturation, self.value)

        # Обновляем цвета источника света
        self.ambient = [r * 0.1, g * 0.1, b * 0.1, 1.0]  # Менее яркий фоновый свет
        self.diffuse = [r, g, b, 1.0]  # Основной цвет
        self.specular = [r, g, b, 1.0]  # Цвет бликов

        # Применяем обновленные значения
        self.apply()
