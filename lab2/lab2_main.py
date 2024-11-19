from lab2.animations.ligth_rotation_animation import LightRotationAnimation
from lab2.camera import Camera
from lab2.materials.textures import Texture
from lab2.render_window import RenderWindow
from lab2.scene import Scene
from lab2.shapes.cone import Cone
from lab2.shapes.cube import Cube
from lab2.shapes.octahedron import Octahedron
from lab2.shapes.torus import Torus
from light.point_light import PointLight
from materials.material import Material
from shapes.teapot import Teapot


def main():
    window = RenderWindow(800, 600, b"Lab 2")

    # Создаем сцену
    scene = Scene()

    # Создаем камеру
    camera = Camera([0.0, 0.0, 5.0], [0.0, 1.0, 0.0], -90.0, 0.0)
    scene.set_camera(camera)

    # Загрузка текстуры
    texture = Texture("../data/textures/leafs.png")
    texture.load()

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
        shininess=50,
        specular=[1.0, 1.0, 1.0, 1.0],
        diffuse=[0.2, 0.2, 0.2, 0.5],  # Диффузный красный цвет с альфа 0.5
        transparent=True  # Включение прозрачности
    )

    # Полированный материал для тороидального объекта
    polished_material = Material(
        color=[0.2, 0.2, 0.6, 1.0],  # Голубой цвет
        shininess=128,
        specular=[2.0, 2.0, 2.0, 1.0],
        diffuse=[0.4, 0.4, 0.4, 1.0],
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

    # Создаем текстурированный октаэдр с матовым материалом
    textured_cube_material = Material(
        color=[1.0, 1.0, 1.0, 0.0],
        shininess=10,
        specular=[0.1, 0.1, 0.1, 1.0],
        diffuse=[0.8, 0.8, 0.8, 1.0],
        texture=texture.texture_id,
        transparent=True)

    textured_oct = Octahedron(position=[1.0, 1.0, -5.0], scale=2.0, material=textured_cube_material)
    scene.add_object(textured_oct)

    # Полированный голубой чайник
    polished_teapot = Teapot(position=[-3.0, 1.0, 0.0], scale=1.0, material=polished_material)
    scene.add_object(polished_teapot)

    # Прозрачный розовый тор
    transparent_torus = Torus(inner_radius=0.5, outer_radius=1.0, rings=30, sides=30,
                              position=[0.5, 1.0, 0.0], scale=1.0, material=transparent_material)
    scene.add_object(transparent_torus)

    # Матовый желтый конус
    matte_cone = Cone(position=[3.0, 0.0, 0.0], scale=1.0, material=diffuse_material)
    scene.add_object(matte_cone)

    # Создаем анимацию вращения источника света
    light_rotation_animation = LightRotationAnimation(point_light, radius=5.0, speed=30.0)
    light_rotation_animation.start()

    # Добавляем анимацию в сцену
    scene.add_animation(light_rotation_animation)

    window.set_scene(scene)
    window.run()


if __name__ == "__main__":
    main()
