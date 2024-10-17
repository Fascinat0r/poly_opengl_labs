from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from camera import Camera
from handlers import key_pressed, key_released, handle_camera_movement, mouse_movement
from scene import Scene  # Класс сцены

# Создаем камеру
camera = Camera([0.0, 0.0, 5.0], [0.0, 1.0, 0.0], -90.0, 0.0)

# Создаем сцену
scene = Scene()

def init():
    glEnable(GL_DEPTH_TEST)  # Включаем тест глубины для 3D
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Черный фон

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800 / 600, 0.1, 100.0)  # Настройка перспективы
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Получаем матрицу вида камеры
    position, target, up = camera.get_view_matrix()
    gluLookAt(position[0], position[1], position[2], target[0], target[1], target[2], up[0], up[1], up[2])

    # Отрисовка сцены
    scene.render()

    glutSwapBuffers()

def update(value):
    """Обновление состояния сцены."""
    handle_camera_movement(camera)
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def key_press_wrapper(key, x, y):
    key_pressed(key, x, y)

def key_release_wrapper(key, x, y):
    key_released(key, x, y)

def mouse_motion_wrapper(x, y):
    mouse_movement(x, y, camera)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"3D Scene with Cube")

    init()

    # Скрываем курсор
    glutSetCursor(GLUT_CURSOR_NONE)

    # Фиксируем мышь в центре окна
    glutWarpPointer(400, 300)

    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutKeyboardFunc(key_press_wrapper)
    glutKeyboardUpFunc(key_release_wrapper)
    glutPassiveMotionFunc(mouse_motion_wrapper)
    glutTimerFunc(16, update, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()
