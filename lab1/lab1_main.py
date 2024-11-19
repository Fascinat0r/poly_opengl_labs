from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from animations.looped_rotation_animation import LoopedRotationAnimation
from camera import Camera
from handlers import create_mouse_movement_handler, key_pressed, key_released, handle_camera_movement
from lab1.animations.looped_movement_animation import LoopedMovementAnimation
from lab1.shapes.octahedron import Octahedron
from lab1.shapes.teapot import Teapot
from lab1.shapes.torus import Torus
from scene import Scene
from shapes.cone import Cone

# Создаём камеру и сцену
camera = Camera([0.0, 0.0, 5.0], [0.0, 1.0, 0.0], -90.0, 0.0)
scene = Scene()


def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

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

    scene.render()

    glutSwapBuffers()


def update(value):
    handle_camera_movement(camera)  # Обновляем позицию камеры
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"3D Scene with Animation")

    init()

    # Создаем объекты
    octahedron = Octahedron(position=[0.0, 0.0, 0.0], scale=1.0, color=[1.0, 0.0, 0.0])
    scene.add_object(octahedron)

    cone = Cone(base_radius=1.0, height=2.0, slices=30, position=[2.0, 0.0, 0.0], scale=1.0, color=[1.0, 1.0, 0.0])
    scene.add_object(cone)

    teapot = Teapot(position=[-2.0, 0.0, 0.0], scale=1.0, color=[0.0, 1.0, 1.0])
    scene.add_object(teapot)

    tor = Torus(position=[-2.0, 0.0, -4.0], scale=1.0, color=[1.0, 0.0, 1.0])
    scene.add_object(tor)

    # Создаем анимации и добавляем их в сцену
    cone_rotation_animation = LoopedRotationAnimation(
        target_object=cone,
        start_angles=[0.0, 0.0, 0.0],
        end_angles=[0.0, 0.0, -60.0],
        speeds=[0.0, 0.0, 20]
    )
    cone_rotation_animation.start()
    scene.add_animation(cone_rotation_animation)

    oct_rotation_animation = LoopedRotationAnimation(
        target_object=octahedron,
        start_angles=[0.0, 0.0, 0.0],
        end_angles=[90.0, 0.0, 0.0],
        speeds=[20, 0.0, 0.0]
    )
    oct_rotation_animation.start()
    scene.add_animation(oct_rotation_animation)

    # Анимации перемещения
    teapot_movement_animation = LoopedMovementAnimation(
        target_object=teapot,
        start_position=[-2.0, 0.0, 0.0],
        end_position=[-2.0, 0.0, -2.0],
        speeds=[0.0, 0.0, 1],
        tolerance=0.01
    )
    teapot_movement_animation.start()
    scene.add_animation(teapot_movement_animation)

    # Анимации перемещения тора, центр тора должен совпасть с центром чайника
    tor_movement_animation = LoopedMovementAnimation(
        target_object=tor,
        start_position=[-2.0, 0.0, -4.0],
        end_position=[-2.0, 0.0, -2.0],
        speeds=[0.0, 0.0, 1.0],
        tolerance=0.01
    )
    tor_movement_animation.start()
    scene.add_animation(tor_movement_animation)

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
