from lab3.animations.ligth_rotation_animation import LightRotationAnimation
from lab3.camera import Camera
from lab3.materials.textures import Texture
from lab3.render_window import RenderWindow
from lab3.scene import Scene
from lab3.shapes.TexturedCube import TexturedCube
from lab3.shapes.cube import Cube
from light.point_light import PointLight
from materials.material import Material
from shapes.teapot import Teapot


def main():
    window = RenderWindow(800, 600, b"Lab 3")

    # Создаем сцену
    scene = Scene()

    # Создаем камеру
    camera = Camera([0.0, 0.0, 5.0], [0.0, 1.0, 0.0], -90.0, 0.0)
    scene.set_camera(camera)

    # Источник света - точечный свет
    point_light = PointLight(position=[0.0, 5.0, 5.0, 1.0],
                             ambient=[0.05, 0.05, 0.05, 1.0],  # Слабое фоновое освещение
                             diffuse=[2.0, 2.0, 2.0, 2.0],  # Яркий рассеянный свет
                             specular=[1.0, 1.0, 1.0, 1.0],  # Яркий зеркальный свет
                             attenuation=[1.0, 0.1, 0.01])  # Затухание света
    scene.add_light(point_light)

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
    texture = Texture("../data/textures/wool.jpg")
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

    window.set_scene(scene)
    window.run()


if __name__ == "__main__":
    main()
