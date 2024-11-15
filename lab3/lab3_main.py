from lab3.animations.ligth_rotation_animation import LightRotationAnimation
from lab3.camera import Camera
from lab3.materials.textures import Texture
from lab3.render_window import RenderWindow
from lab3.scene import Scene
from lab3.shapes.cube import Cube
from lab3.shapes.plane import Plane
from light.point_light import PointLight
from materials.material import Material


def main():
    # Создаем окно рендеринга
    window = RenderWindow(800, 600, b"Lab 3 with Shadows")

    # Создаем сцену
    scene = Scene()

    # Создаем камеру
    camera = Camera(position=[0.0, 2.0, 5.0], up=[0.0, 1.0, 0.0], yaw=-90.0, pitch=-20.0)
    scene.set_camera(camera)

    # Загрузка текстуры для текстурированного куба
    texture = Texture("../data/textures/leafs.png")
    texture.load()

    texture_cobblestone = Texture("../data/textures/grassy_cobblestone.jpg")
    texture_cobblestone.load()

    # Источник света - точечный свет
    point_light = PointLight(position=[0.0, 5.0, 5.0],
                             ambient=[0.05, 0.05, 0.05],
                             diffuse=[1.0, 1.0, 1.0],
                             specular=[1.0, 1.0, 1.0],
                             attenuation=[1.0, 0.09, 0.032])
    scene.add_light(point_light)

    # Создаем материал для пола
    floor_material = Material(
        ambient=[0.1, 0.1, 0.1],
        diffuse=[0.5, 0.5, 0.5],
        specular=[0.2, 0.2, 0.2],
        shininess=10.0,
        texture=texture_cobblestone.texture_id,
        transparent=False
    )

    # Создаем объект плоскости
    floor = Plane(position=[0.0, 0.0, 0.0], scale=40.0, rotation=[0.0, 0.0, 0.0], material=floor_material)
    scene.add_object(floor)

    # Создаем текстурированный куб
    textured_cube_material = Material(
        ambient=[0.1, 0.1, 0.1],
        diffuse=[0.8, 0.8, 0.8],
        specular=[0.5, 0.5, 0.5],
        shininess=32.0,
        texture=texture.texture_id,
        transparent=True
    )
    textured_cube = Cube(position=[1.0, 1.0, -5.0], scale=2.0, rotation=[0.0, 0.0, 0.0],
                         material=textured_cube_material)
    scene.add_object(textured_cube)

    # Создаем анимацию вращения источника света
    light_rotation_animation = LightRotationAnimation(point_light, radius=5.0, speed=30.0)
    light_rotation_animation.start()

    # Добавляем анимацию в сцену
    scene.add_animation(light_rotation_animation)

    # Устанавливаем сцену в окно рендеринга
    window.set_scene(scene)

    # Запускаем рендеринг
    window.run()


if __name__ == "__main__":
    main()
