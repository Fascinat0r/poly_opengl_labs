# material.py
from OpenGL.GL import *


class Material:
    def __init__(self, color=[1.0, 1.0, 1.0, 0.0], shininess=0.0, specular=[1.0, 1.0, 1.0, 1.0],
                 diffuse=[1.0, 1.0, 1.0, 1.0], texture=None, transparent=False):
        """
        Конструктор материала.

        :param color: Основной цвет объекта [R, G, B, A] с прозрачностью.
        :param shininess: Блеск (коэффициент зеркальности).
        :param specular: Зеркальный цвет.
        :param diffuse: Диффузный цвет.
        :param texture: Текстура, связанная с материалом (если есть).
        :param transparent: Флаг, указывающий на прозрачность объекта.
        """
        self.color = color
        self.shininess = shininess
        self.specular = specular
        self.diffuse = diffuse
        self.texture = texture
        self.transparent = transparent

    def apply(self):
        """Применение материала к объекту перед его рендерингом."""

        # Установка цвета (с альфа-каналом для прозрачности)
        glColor4f(*self.color)

        # Настройка прозрачности, если включена
        if self.transparent:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glDepthMask(GL_FALSE)  # Отключаем запись в буфер глубины для прозрачных объектов
        else:
            glDisable(GL_BLEND)
            glDepthMask(GL_TRUE)

        # Установка свойств материала (блеск, зеркальный и диффузный цвет)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.specular)
        glMaterialf(GL_FRONT, GL_SHININESS, min(self.shininess, 128.0))

        # Применение текстуры, если она задана
        if self.texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)
        else:
            glDisable(GL_TEXTURE_2D)

    def cleanup(self):
        """Очистка после применения прозрачности и текстуры."""
        if self.transparent:
            glDepthMask(GL_TRUE)  # Восстанавливаем буфер глубины для других объектов
            glDisable(GL_BLEND)
        if self.texture:
            glDisable(GL_TEXTURE_2D)
