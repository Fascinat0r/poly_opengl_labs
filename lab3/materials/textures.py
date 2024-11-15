# textures.py
import numpy as np
from PIL import Image

from OpenGL.GL import *


class Texture:
    def __init__(self, texture_path):
        self.texture_path = texture_path
        self.texture_id = glGenTextures(1)

    def load(self):
        """Загружаем текстуру и привязываем её к объекту OpenGL."""
        image = Image.open(self.texture_path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Переворот изображения для корректного отображения

        img_data = np.array(image, dtype=np.uint8)

        if image.mode == "RGBA":
            format = GL_RGBA
        elif image.mode == "RGB":
            format = GL_RGB
        else:
            raise ValueError("Unsupported image format")

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, format, image.width, image.height, 0, format, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        # Установка параметров текстуры
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def bind(self, unit=0):
        """Привязка текстуры к текстурному блоку."""
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
