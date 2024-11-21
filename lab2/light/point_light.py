from OpenGL.GL import *
from OpenGL.GLUT import *

ids = [GL_LIGHT0, GL_LIGHT1, GL_LIGHT2, GL_LIGHT3, GL_LIGHT4, GL_LIGHT5, GL_LIGHT6, GL_LIGHT7]
next_id = 0


class PointLight:
    def __init__(self, position=[0.0, 0.0, 1.0, 1.0],
                 ambient=[0.05, 0.05, 0.05, 1.0],
                 diffuse=[1.0, 1.0, 1.0, 1.0],
                 specular=[1.0, 1.0, 1.0, 1.0],
                 attenuation=[1.0, 0.1, 0.01],
                 target_color=[1.0, 0.0, 0.0, 1.0], ):
        """
        light_id: ID источника света (например, GL_LIGHT0).
        position: Позиция источника света [x, y, z, w]. w = 1 для точечного источника.
        ambient: Фоновое освещение.
        diffuse: Рассеянный свет.
        specular: Зеркальный свет.
        attenuation: Аттенюация (затухание света) [constant, linear, quadratic].
        """
        global next_id  # TODO: костыль
        self.light_id = ids[next_id]
        next_id += 1
        self.position = position
        self.ambient = ambient.copy()
        self.diffuse = diffuse.copy()
        self.specular = specular.copy()
        self.attenuation = attenuation

        # Для плавного изменения цвета
        self.original_ambient = ambient.copy()
        self.original_diffuse = diffuse.copy()
        self.original_specular = specular.copy()
        self.target_color = [1.0, 0.0, 0.0, 1.0]  # Пример: красный цвет
        self.color_step = 0.01  # Шаг изменения цвета
        self.color_direction = 1  # 1: к целевому, -1: к исходному

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

    def change_color(self, target_color=None):
        """
        Изменение цвета источника света плавно от исходного до заданного и обратно.
        :param target_color: Целевой цвет [R, G, B, A]. Если None, используется self.target_color.
        """
        if target_color:
            self.target_color = target_color

        # Определяем текущую цель (целевой или исходный цвет)
        current_target = self.target_color if self.color_direction == 1 else self.original_ambient

        # Обновляем значения цветов с плавным изменением
        for i in range(4):
            # Линейное приближение текущего цвета к целевому
            self.ambient[i] += (current_target[i] - self.ambient[i]) * self.color_step
            self.diffuse[i] += (current_target[i] - self.diffuse[i]) * self.color_step
            self.specular[i] += (current_target[i] - self.specular[i]) * self.color_step

        # Проверяем, достигнут ли целевой цвет
        if all(abs(self.ambient[i] - current_target[i]) < 0.01 for i in range(4)):
            # Меняем направление, если достигли текущей цели
            self.color_direction *= -1

        # Применяем обновленные значения
        self.apply()

