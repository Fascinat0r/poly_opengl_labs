from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from lab3.handlers import key_pressed, key_released, create_mouse_movement_handler, handle_camera_movement
from lab3.scene import Scene


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
        glutDisplayFunc(self.render)
        glutIdleFunc(self.render)
        glutKeyboardFunc(key_pressed)  # Обычные клавиши
        glutKeyboardUpFunc(key_released)  # Отпускание обычных клавиш
        glutPassiveMotionFunc(create_mouse_movement_handler(self.scene.camera))

        glutTimerFunc(16, self.update, 0)
        glutMainLoop()

    def update(self, value):
        handle_camera_movement(self.scene.camera)  # Обновляем позицию камеры
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

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Устанавливаем матрицу вида для камеры
        position, target, up = self.scene.camera.get_view_matrix()
        gluLookAt(position[0], position[1], position[2], target[0], target[1], target[2], up[0], up[1], up[2])

        # Обновляем анимации в сцене
        self.scene.update_animations()

        # Отрисовываем сетку и оси
        self.scene.draw_grid()
        self.scene.draw_axes()

        # Рисуем индикатор источника света
        for light in self.scene.lights:
            light.draw_indicator()

        # Разделяем и сортируем объекты
        opaque_objects, transparent_objects = self.scene.sort_objects()

        # Рендер непрозрачных объектов
        for obj in opaque_objects:
            obj.render()

        # Рендер прозрачных объектов в правильном порядке
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(GL_FALSE)  # Отключаем запись в буфер глубины для прозрачных объектов

        for obj in transparent_objects:
            obj.render()

        glDepthMask(GL_TRUE)  # Восстанавливаем запись в буфер глубины
        glDisable(GL_BLEND)

        glutSwapBuffers()
