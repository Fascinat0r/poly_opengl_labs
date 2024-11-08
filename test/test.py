# test.py
from OpenGL.GL import *
from OpenGL.GLUT import *
from scene import Scene

def display():
    global scene
    scene.render_shadow_pass()  # Рендерим в теневую карту
    scene.render_main_pass()    # Основной рендеринг сцены с тенями

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Shadow Mapping Example")
    glEnable(GL_DEPTH_TEST)

    # Теперь создаем сцену после создания контекста OpenGL
    global scene
    scene = Scene()

    glutDisplayFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()
