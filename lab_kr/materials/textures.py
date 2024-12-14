from abc import ABC, abstractmethod

import numpy as np
from PIL import Image
from OpenGL.GL import *


class Texture(ABC):
    """
    Абстрактный класс для текстур.
    """
    def __init__(self):
        self.texture_id = glGenTextures(1)

    @abstractmethod
    def load(self):
        """Загружает текстуру в OpenGL."""
        pass

    def bind(self, unit=0):
        """Привязывает текстуру к указанному текстурному блоку."""
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)


class ImageTexture(Texture):
    """
    Класс для загрузки текстуры из изображения.
    """
    def __init__(self, texture_path):
        super().__init__()
        self.texture_path = texture_path

    def load(self):
        """Загружает текстуру из файла изображения и привязывает её к объекту OpenGL."""
        image = Image.open(self.texture_path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Переворот изображения для OpenGL
        if image.mode != 'RGBA' and image.mode != 'RGB':
            image = image.convert('RGBA')

        img_data = np.array(image, dtype=np.uint8)

        if image.mode == 'RGBA':
            clr_format = GL_RGBA
        elif image.mode == 'RGB':
            clr_format = GL_RGB
        else:
            raise ValueError('Unsupported image format')

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, clr_format,
                     image.width, image.height, 0, clr_format, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        # Установка параметров текстуры
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)


class FlatTexture(Texture):
    """
    Класс для создания плоской текстуры с заданным цветом.
    """
    def __init__(self, color):
        """
        :param color: Цвет текстуры в формате [R, G, B, A].
        """
        super().__init__()
        self.color = color

    def load(self):
        """Создает плоскую текстуру с указанным цветом."""
        # Формируем текстурные данные для 1x1 текстуры
        img_data = np.array(self.color * 3, dtype=np.uint8)  # RGBA-цвет

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1, 1, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        # Установка параметров текстуры
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
