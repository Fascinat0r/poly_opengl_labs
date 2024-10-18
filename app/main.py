from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from app.animations.ligth_rotation_animation import LightRotationAnimation
from app.camera import Camera
from app.handlers import key_pressed, key_released, create_mouse_movement_handler, handle_camera_movement
from app.scene import Scene
from light.point_light import PointLight
from materials.material import Material
from shapes.cone import Cone
from shapes.teapot import Teapot
from shapes.torus import Torus

# Создаём камеру и сцену
camera = Camera([0.0, 0.0, 5.0], [0.0, 1.0, 0.0], -90.0, 0.0)
scene = Scene()

# Источник света - точечный свет
point_light = PointLight(GL_LIGHT0, position=[0.0, 5.0, 5.0, 1.0],
                         ambient=[0.05, 0.05, 0.05, 1.0],  # Слабое фоновое освещение
                         diffuse=[2.0, 2.0, 2.0, 2.0],  # Яркий рассеянный свет
                         specular=[1.0, 1.0, 1.0, 1.0],  # Яркий зеркальный свет
                         attenuation=[1.0, 0.1, 0.01])  # Затухание света


def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)

    # Включаем первый источник света
    point_light.apply()

    # Настраиваем темную сцену
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Фоновый черный цвет

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800 / 600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    position, target, up = camera.get_view_matrix()
    gluLookAt(position[0], position[1], position[2], target[0], target[1], target[2], up[0], up[1], up[2])

    # Обновляем анимации в сцене
    scene.update_animations()

    # Включаем режим прозрачности
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Рисуем индикатор источника света
    point_light.draw_indicator()

    scene.render()

    glutSwapBuffers()


def update(value):
    handle_camera_movement(camera)  # Обновляем позицию камеры
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1024, 720)  # Устанавливаем размер окна
    glutCreateWindow(b"Dark Scene with Point Light")

    init()

    # Создаем объекты
    # Полированный тор
    polished_torus = Torus(position=[2.0, 0.0, 0.0], scale=1.0, color=[0.5, 0.5, 0.5],
                           material=Material(specular=[1.0, 1.0, 1.0, 1.0], shininess=128))

    # Прозрачный чайник
    transparent_teapot = Teapot(position=[-2.0, 0.0, 0.0], scale=1.0, color=[0.0, 1.0, 1.0],
                                material=Material(diffuse=[0.0, 1.0, 1.0, 0.6], transparency=0.6))

    # Матовый конус
    matte_cone = Cone(base_radius=1.0, height=2.0, position=[0.0, 0.0, 0.0], scale=1.0,
                      material=Material(diffuse=[0.8, 0.8, 0.0, 1.0], shininess=10))

    scene.add_object(polished_torus)
    scene.add_object(transparent_teapot)
    scene.add_object(matte_cone)

    # Создаем анимацию вращения источника света
    light_rotation_animation = LightRotationAnimation(point_light, radius=5.0, speed=30.0)
    light_rotation_animation.start()

    # Добавляем анимацию в сцену
    scene.add_animation(light_rotation_animation)

    # Скрываем курсор и фиксируем мышь в центре окна
    glutSetCursor(GLUT_CURSOR_NONE)
    glutWarpPointer(400, 300)

    # Устанавливаем обработчики
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutKeyboardFunc(key_pressed)
    glutKeyboardUpFunc(key_released)
    glutPassiveMotionFunc(create_mouse_movement_handler(camera))

    glutTimerFunc(16, update, 0)
    glutMainLoop()


if __name__ == "__main__":
    main()
