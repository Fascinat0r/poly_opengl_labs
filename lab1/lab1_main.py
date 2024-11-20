from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from camera import Camera
from handlers import create_mouse_movement_handler, key_pressed, key_released, handle_camera_movement
from lab1.animations.looped_movement_animation import LoopedMovementAnimation
from lab1.animations.looped_scale_animation import LoopedScaleAnimation
from lab1.shapes.cone import Cone
from lab1.shapes.cube import Cube
from lab1.shapes.cylinder import Cylinder
from lab1.shapes.sphere import Sphere
from scene import Scene

# Создаём камеру и сцену
camera = Camera([0.0, 100.0, 350.0], [0.0, 1.0, 0.0], -90.0, 0.0)
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

    # Создаем объекты
    cube = Cube(position=[40.0, 125.0, 30.0], scale=250.0, color=[0.0, 1.0, 1.0], rotation=[0.0, 0.0, 0.0])
    scene.add_object(cube)

    sphere = Sphere(radius=1.732*250/2, slices=32, stacks=16, position=[40.0, 125.0, 30.0], color=[1.0, 0.0, 1.0])
    scene.add_object(sphere)

    cone = Cone(base_radius=100.0, height=100.0, slices=20, position=[-300.0, 0.0, 0.0], scale=1.0,
                color=[1.0, 0.0, 0.0], rotation=[0.0, 0.0, 0.0])
    scene.add_object(cone)

    cylinder = Cylinder(base_radius=100.0, top_radius=100.0, height=100.0, slices=20, position=[-300.0, 100.0, 0.0], scale=1.0,
                        color=[0.0, 1.0, 1.0], rotation=[0.0, 0.0, 0.0])
    scene.add_object(cylinder)

    # Создаем анимации и добавляем их в сцену
    cube_movement_animation = LoopedMovementAnimation(
        target_object=cube,
        start_position=[40.0, 125.0, 30.0],
        end_position=[40.0+250, 125.0, 30.0],
        speeds=[250.0, 0.0, 0.0]
    )
    cube_movement_animation.start()
    scene.add_animation(cube_movement_animation)

    sphere_movement_animation = LoopedMovementAnimation(
        target_object=sphere,
        start_position=[40.0, 125.0, 30.0],
        end_position=[40.0, 125.0-150, 30.0],
        speeds=[0.0, 150.0, 0.0]
    )
    sphere_movement_animation.start()
    scene.add_animation(sphere_movement_animation)

    cylinder_scale_animation = LoopedScaleAnimation(
        target_object=cylinder,
        start_scale=1.0,
        end_scale=1.7,
        speed=1.0
    )
    cylinder_scale_animation.start()
    scene.add_animation(cylinder_scale_animation)

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
