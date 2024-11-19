from OpenGL.GL import *


def draw_quad(v1, v2, v3, v4, n, uv1, uv2, uv3, uv4):
    """
    Отрисовка одной грани (четырёхугольника) с текстурными координатами и нормалью.

    :param v1, v2, v3, v4: Координаты четырёх углов грани.
    :param n: Нормаль для всей грани.
    :param uv1, uv2, uv3, uv4: Текстурные координаты для вершин.
    """
    glNormal3fv(n)  # Устанавливаем нормаль

    # Вершина 1
    glTexCoord2f(*uv1)
    glVertex3fv(v1)

    # Вершина 2
    glTexCoord2f(*uv2)
    glVertex3fv(v2)

    # Вершина 3
    glTexCoord2f(*uv3)
    glVertex3fv(v3)

    # Вершина 4
    glTexCoord2f(*uv4)
    glVertex3fv(v4)


def draw_triangle(v1, v2, v3, n, uv1, uv2, uv3):
    """
    Отрисовка одного треугольника с текстурными координатами и нормалью.
    :param v1, v2, v3: Координаты трёх вершин треугольника.
    :param n: Нормаль для треугольника.
    :param uv1, uv2, uv3: Текстурные координаты для вершин.
    """
    glNormal3fv(n)  # Устанавливаем нормаль

    # Вершина 1
    glTexCoord2f(*uv1)
    glVertex3fv(v1)

    # Вершина 2
    glTexCoord2f(*uv2)
    glVertex3fv(v2)

    # Вершина 3
    glTexCoord2f(*uv3)
    glVertex3fv(v3)


def draw_edge(v1, v2):
    """
    Отрисовка одного ребра.

    :param v1, v2: Координаты двух вершин ребра.
    """
    glVertex3fv(v1)
    glVertex3fv(v2)


def batch_draw_triangles(triangles):
    """
    Пакетная отрисовка треугольников.
    :param triangles: Массив, содержащий данные о всех треугольниках.
    """
    glBegin(GL_TRIANGLES)
    for triangle in triangles:
        v1, v2, v3, n, uv1, uv2, uv3 = triangle
        glNormal3fv(n)
        glTexCoord2f(*uv1)
        glVertex3fv(v1)
        glTexCoord2f(*uv2)
        glVertex3fv(v2)
        glTexCoord2f(*uv3)
        glVertex3fv(v3)
    glEnd()
