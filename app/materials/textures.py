from OpenGL.GL import *
from PIL import Image


class Texture:
    def __init__(self, texture_path):
        self.texture_path = texture_path
        self.texture_id = glGenTextures(1)

    def load(self):
        """Загружаем текстуру и привязываем её к объекту OpenGL."""
        image = Image.open(self.texture_path)

        # Проверка на наличие альфа-канала
        if image.mode == "RGBA":
            img_data = image.tobytes("raw", "RGBA", 0, -1)
            format = GL_RGBA
        else:
            img_data = image.tobytes("raw", "RGB", 0, -1)
            format = GL_RGB

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, format, image.width, image.height, 0, format, GL_UNSIGNED_BYTE, img_data)

        # Устанавливаем параметры фильтрации текстуры
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glEnable(GL_TEXTURE_2D)

    def apply(self):
        """Применение текстуры."""
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
