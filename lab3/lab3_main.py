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

    # Создаем материалы с использованием нового класса Material
    transparent_material = Material(
        color=[0.8, 0.0, 0.0, 0.5],  # Красный с прозрачностью 0.5
        shininess=30,
        specular=[1.0, 1.0, 1.0, 1.0],
        diffuse=[0.8, 0.0, 0.0, 0.5],  # Диффузный красный цвет с альфа 0.5
        transparent=True  # Включение прозрачности
    )

    # Полированный материал для тороидального объекта
    polished_material = Material(
        color=[0.2, 0.2, 0.6, 1.0],  # Голубой цвет
        shininess=128,
        specular=[2.0, 2.0, 2.0, 1.0],
        diffuse=[0.4, 0.4, 0.4, 1.0]
    )

    # Матовый материал для объектов с текстурой
    diffuse_material = Material(
        # Жёлтый
        color=[0.8, 0.8, 0.0, 1.0],
        shininess=10,
        specular=[0.1, 0.1, 0.1, 1.0],
        diffuse=[0.6, 0.6, 0.6, 1.0]
    )

    # Матовый материал для фона
    background_material = Material(
        color=[0.1, 0.1, 0.1, 1.0],
        shininess=10,
        specular=[0.1, 0.1, 0.1, 1.0],
        diffuse=[0.1, 0.1, 0.1, 1.0]
    )

    # Создаем объекты и применяем материалы

    # Объект комнаты с матовым материалом
    room = Cube(position=[0.0, 9.0, 0.0], scale=20.0, material=background_material)
    scene.add_object(room)

    # Загрузка текстуры для текстурированного куба
    texture = Texture("../data/textures/wool.jpg")
    texture.load()

    # Создаем текстурированный куб с матовым материалом
    textured_cube_material = Material(color=[1.0, 1.0, 1.0, 1.0], diffuse=[0.8, 0.8, 0.8, 1.0],
                                      texture=texture.texture_id)
    textured_cube = TexturedCube(position=[0.0, 0.0, -5.0], scale=2.0, material=textured_cube_material)
    scene.add_object(textured_cube)

    # Полированный голубой чайник
    polished_teapot = Teapot(position=[-3.0, 0.0, 0.0], scale=1.0, material=polished_material)
    scene.add_object(polished_teapot)

    # Прозрачный розовый чайник
    transparent_teapot = Teapot(position=[0.0, 0.0, 0.0], scale=1.0, material=transparent_material)
    scene.add_object(transparent_teapot)

    # Матовый желтый чайник
    matte_teapot = Teapot(position=[3.0, 0.0, 0.0], scale=1.0, material=diffuse_material)
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
