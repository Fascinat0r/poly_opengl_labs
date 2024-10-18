from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from app.animations.ligth_rotation_animation import LightRotationAnimation
from app.camera import Camera
from app.handlers import key_pressed, key_released, create_mouse_movement_handler, handle_camera_movement
from app.materials.textures import Texture
from app.scene import Scene
from app.shapes.TexturedCube import TexturedCube
from app.shapes.cube import Cube
from light.point_light import PointLight
from materials.material import Material
from shapes.teapot import Teapot

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

    # Включаем глубинный тест
    glEnable(GL_DEPTH_TEST)

    # Включаем запись в буфер глубины снова
    glDepthMask(GL_TRUE)

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

    # Создаем материалы
    transparent_material = Material(
        ambient=[0.2, 0.2, 0.2, 0.5],
        diffuse=[0.8, 0.0, 0.0, 0.5],
        specular=[1.0, 1.0, 1.0, 1.0],
        shininess=30,
        transparency=0.8
    )

    # Очень полированная поверхность для тора
    polished_material = Material(
        ambient=[0.3, 0.3, 0.3, 1.0],
        diffuse=[0.4, 0.4, 0.4, 1.0],
        specular=[2.0, 2.0, 2.0, 1.0],
        shininess=128
    )

    # Матовый объект с текстурой (например, октаэдр)
    diffuse_material = Material(
        ambient=[0.2, 0.2, 0.2, 1.0],
        diffuse=[0.6, 0.6, 0.6, 1.0],
        specular=[0.1, 0.1, 0.1, 1.0],
        shininess=10
    )

    # Создаем объекты
    # Добавим комнату темно-серого цвета
    room = Cube(position=[0.0, 9.0, 0.0], scale=20.0, color=[0.5, 0.5, 0.5], material=diffuse_material)
    scene.add_object(room)

    # Загружаем текстуру
    texture = Texture("data/textures/wool.jpg")
    texture.load()

    # Создаем текстурированный объект (например, куб)
    textured_cube = TexturedCube(position=[0.0, 0.0, -5.0], scale=2.0, texture=texture)
    scene.add_object(textured_cube)

    # Полированный тор
    polished_teapot = Teapot(position=[-3.0, 0.0, 0.0], scale=1.0, color=[0.0, 1.0, 1.0],  # Голубой полированный
                             material=polished_material)

    # Прозрачный чайник
    transparent_teapot = Teapot(position=[0.0, 0.0, 0.0], scale=1.0, color=[1.0, 0.0, 1.0],  # Розовый прозрачный
                                material=transparent_material)

    # Матовый конус
    matte_teapot = Teapot(position=[3.0, 0.0, 0.0], scale=1.0, color=[1.0, 1.0, 0.0],  # Жёлтый матовый
                          material=diffuse_material)

    scene.add_object(polished_teapot)
    scene.add_object(transparent_teapot)
    scene.add_object(matte_teapot)

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
