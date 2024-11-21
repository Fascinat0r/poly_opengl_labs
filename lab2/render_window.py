from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from lab2.handlers import key_pressed, key_released, create_mouse_movement_handler, handle_camera_movement, \
    handle_light_color_change
from lab2.scene import Scene


class RenderWindow:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.scene = None
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow(self.title)

        # Включаем режим прозрачности
        glEnable(GL_DEPTH_TEST)
        # Включаем запись в буфер глубины снова
        glEnable(GL_LIGHTING)
        # Включаем цветовые материалы
        glEnable(GL_COLOR_MATERIAL)

        # Скрываем курсор и фиксируем мышь в центре окна
        glutSetCursor(GLUT_CURSOR_NONE)
        glutWarpPointer(self.width // 2, self.height // 2)

    def set_scene(self, scene: Scene):
        self.scene = scene

    def run(self):
        # Устанавливаем обработчики
        glutReshapeFunc(self.reshape)
        glutDisplayFunc(self.scene.render)
        glutIdleFunc(self.scene.render)
        glutKeyboardFunc(key_pressed)  # Обычные клавиши
        glutKeyboardUpFunc(key_released)  # Отпускание обычных клавиш
        glutPassiveMotionFunc(create_mouse_movement_handler(self.scene.camera))

        glutTimerFunc(16, self.update, 0)
        glutMainLoop()

    def update(self, value):
        handle_camera_movement(self.scene.camera)  # Обновляем позицию камеры
        handle_light_color_change(self.scene.lights[0])  # Изменяем цвет света
        glutPostRedisplay()
        glutTimerFunc(16, self.update, 0)

    def reshape(self, width, height):
        self.width = width if width != 0 else self.width
        self.height = height if height != 0 else self.height

        aspect_ratio = self.width / self.height

        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, aspect_ratio, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glutWarpPointer(self.width // 2, self.height // 2)
