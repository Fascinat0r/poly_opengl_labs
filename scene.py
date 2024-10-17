from OpenGL.GL import *


def draw_axes():
    glBegin(GL_LINES)

    # Оси
    glColor3f(1, 0, 0)  # Ось X
    glVertex3f(-10.0, 0.0, 0.0)
    glVertex3f(10.0, 0.0, 0.0)

    glColor3f(0, 1, 0)  # Ось Y
    glVertex3f(0.0, -10.0, 0.0)
    glVertex3f(0.0, 10.0, 0.0)

    glColor3f(0, 0, 1)  # Ось Z
    glVertex3f(0.0, 0.0, -10.0)
    glVertex3f(0.0, 0.0, 10.0)

    glEnd()


def draw_grid():
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINES)

    for i in range(-10, 11):
        glVertex3f(i, 0, -10)
        glVertex3f(i, 0, 10)
        glVertex3f(-10, 0, i)
        glVertex3f(10, 0, i)

    glEnd()
