# render_window.py
from functools import partial

import glm

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from lab_kr.handlers import key_pressed, key_released, create_mouse_movement_handler, handle_camera_movement, \
    reset_mouse_position
from lab_kr.materials.shader import Shader
from lab_kr.scene import Scene


class RenderWindow:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.scene = None
        self.shader = None
        self.depth_shader = None

        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow(self.title)

        # Инициализация шейдеров
        self.shader = Shader("../data/shaders/shading.vert", "../data/shaders/shading.frag")
        self.depth_shader = Shader("../data/shaders/depth.vert", "../data/shaders/depth.frag")
        self.particle_shader = Shader("../data/shaders/particles.vert", "../data/shaders/particles.frag")

        # Включаем режим теста глубины
        glEnable(GL_DEPTH_TEST)

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
        # Обработчик движения мыши с учётом размеров окна
        glutPassiveMotionFunc(create_mouse_movement_handler(self.scene.camera, partial(self.get_window_size)))

        # Запускаем таймер для обновления сцены
        glutTimerFunc(16, self.update, 0)
        glutMainLoop()

    def update(self, value):
        handle_camera_movement(self.scene.camera)  # Обновляем позицию камеры
        reset_mouse_position(self.width, self.height)  # Возвращаем мышь в центр экрана
        handle_camera_movement(self.scene.camera)  # Обновляем позицию камеры
        glutPostRedisplay()
        glutTimerFunc(16, self.update, 0)

    def get_window_size(self):
        """Возвращает текущие размеры окна."""
        return self.width, self.height

    def reshape(self, width, height):
        self.width = width if width != 0 else self.width
        self.height = height if height != 0 else self.height

        aspect_ratio = self.width / self.height if height > 0 else 1.0

        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.scene.camera.zoom, aspect_ratio, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

        # При взаимодействии с окном в режиме нажатой клавиши Alt, при попытке изменить размер окна,
        # курсор будет сдвинут в середину этого окна. Чтобы можно было нормально изменять размер окна,
        # данная строка должна быть закомментирована.
        # glutWarpPointer(self.width // 2, self.height // 2)

    def render(self):
        if not self.scene or not self.shader or not self.depth_shader:
            return

        # Обновляем анимации
        self.scene.update_animations()

        # Включаем смешивание для прозрачности
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Рисуем оси координат и сетку
        self.scene.draw_grid()
        self.scene.draw_axes()

        # Depth Pass (Создание карты теней)
        self.scene.render_depth_map(self.depth_shader)

        # Render Pass (Рендер объектов сцены)
        self.shader.use()
        self.scene.render_scene(self.shader)

        # Рендеринг частиц
        glDepthMask(GL_FALSE)  # Отключаем запись в буфер глубины для частиц
        self.particle_shader.use()
        self.particle_shader.set_mat4("projection", self.scene.camera.get_projection_matrix())
        self.particle_shader.set_mat4("view", self.scene.camera.get_view_matrix())
        self.particle_shader.set_mat4("model", glm.mat4(1.0))  # Единичная матрица для мировых координат

        if self.scene.particle_system:
            self.scene.particle_system.render(self.particle_shader)

        glDepthMask(GL_TRUE)  # Включаем запись в буфер глубины обратно
        glDisable(GL_BLEND)

        glutSwapBuffers()
