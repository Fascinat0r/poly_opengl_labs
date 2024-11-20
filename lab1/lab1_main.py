from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from camera import Camera
from handlers import create_mouse_movement_handler, key_pressed, key_released, handle_camera_movement
from lab1.animations.looped_movement_animation import LoopedMovementAnimation
from lab1.animations.looped_scale_animation import LoopedScaleAnimation
from lab1.shapes.cube import Cube
from lab1.shapes.sphere import Sphere
from scene import Scene

# Создаём камеру и сцену
camera = Camera([0.0, 0.0, 100.0], [0.0, 1.0, 0.0], -90.0, 0.0)
scene = Scene()


def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800 / 600, 0.1, 1000.0)
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

    cube = Cube(position=[50.0, 50.0, 0.0], scale=100.0, color=[1.0, 0.0, 0.0])
    scene.add_object(cube)

    sphere = Sphere(position=[50.0, 50.0, 0.0], scale=50.0, color=[0.0, 1.0, 0.0])
    scene.add_object(sphere)

    big_cube = Cube(position=[-75.0, 50.0, 0.0], scale=100.0, color=[0.0, 0.0, 1.0])
    scene.add_object(big_cube)

    small_cube = Cube(position=[-75.0, 110.0, 0.0], scale=20.0, color=[1.0, 1.0, 0.0])
    scene.add_object(small_cube)

    # Создаем анимации и добавляем их в сцену
    sphere_scale_animation = LoopedScaleAnimation(
        target_object=sphere,
        start_scale=50.0,
        end_scale=100.0,
        speed=10.0
    )
    sphere_scale_animation.start()
    scene.add_animation(sphere_scale_animation)

    small_cube_movement_animation = LoopedMovementAnimation(
        target_object=small_cube,
        start_position=[-75.0, 110.0, 0.0],
        end_position=[-35.0, 110.0, 40.0],
        speeds=[10.0, 0.0, 10.0],
        tolerance=0.01
    )
    small_cube_movement_animation.start()
    scene.add_animation(small_cube_movement_animation)

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
