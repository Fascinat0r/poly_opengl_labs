from lab2.animations.ligth_rotation_animation import LightRotationAnimation
from lab2.camera import Camera
from lab2.materials.textures import Texture
from lab2.render_window import RenderWindow
from lab2.scene import Scene
from lab2.shapes.cube import Cube
from lab2.shapes.sphere import Sphere
from light.point_light import PointLight
from materials.material import Material


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

    # Полированный материал
    polished_material = Material(
        color=[0.2, 0.2, 0.6, 1.0],
        shininess=128,
        specular=[2.0, 2.0, 2.0, 1.0],
        diffuse=[0.4, 0.4, 0.4, 1.0],
        transparent=False
    )

    # Матовый материал для объектов с текстурой
    diffuse_material = Material(
        # Жёлтый
        color=[0.8, 0.8, 0.0, 1.0],
        shininess=10,
        specular=[0.1, 0.1, 0.1, 1.0],
        diffuse=[0.6, 0.6, 0.6, 1.0],
        transparent=False
    )

    # Матовый материал для фона
    background_material = Material(
        color=[0.1, 0.1, 0.1, 1.0],
        shininess=10,
        specular=[0.1, 0.1, 0.1, 1.0],
        diffuse=[0.1, 0.1, 0.1, 1.0],
        transparent=False
    )

    # Создаем объекты и применяем материалы

    # Объект комнаты с матовым материалом
    room = Cube(position=[0.0, 9.0, 0.0], scale=20.0, material=background_material)
    scene.add_object(room)

    textured_material = Material(
        color=[1.0, 1.0, 1.0, 0.0],
        shininess=10,
        specular=[0.1, 0.1, 0.1, 1.0],
        diffuse=[0.8, 0.8, 0.8, 1.0],
        texture=texture.texture_id,
        transparent=True)

    materials = [transparent_material, polished_material, diffuse_material, textured_material]

    cube = Cube(position=[-2.0, 0.5, 0.0], scale=1.0, material=materials[0])

    sphere = Sphere(radius=0.5, position=[2.0, 0.5, 0.0], scale=1.0, material=materials[1], slices=16, stacks=16)

    big_cube = Cube(position=[0.0, 0.5, 0.0], scale=1.0, material=materials[2])

    small_cube = Cube(position=[-2.0, 2.5, -2.0], scale=1.0, material=materials[3])

    scene.add_object(cube)
    scene.add_object(sphere)
    scene.add_object(big_cube)
    scene.add_object(small_cube)

    # Создаем анимацию вращения источника света
    light_rotation_animation = LightRotationAnimation(point_light, radius=5.0, speed=30.0)
    light_rotation_animation.start()

    # Добавляем анимацию в сцену
    scene.add_animation(light_rotation_animation)

    window.set_scene(scene)
    window.run()


if __name__ == "__main__":
    main()
