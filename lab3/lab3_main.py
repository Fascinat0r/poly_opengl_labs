# lab3_main.py
from lab3.animations.directional_light_rotation_animation import DirectionalLightRotationAnimation
from lab3.camera import Camera
from lab3.light.directional_light import DirectionalLight  # Импортируйте новый класс
from lab3.materials.material import Material
from lab3.materials.textures import Texture
from lab3.render_window import RenderWindow
from lab3.scene import Scene
from lab3.shapes.cube import Cube
from lab3.shapes.plane import Plane


# lab3_main.py
def main():
    # Создаем окно рендеринга
    window = RenderWindow(800, 600, b"Lab 3 with Shadows")

    # Создаем сцену
    scene = Scene()

    # Создаем камеру
    camera = Camera(position=[0.0, 2.0, 5.0], up=[0.0, 1.0, 0.0], yaw=-90.0, pitch=-20.0)
    scene.set_camera(camera)

    # Загрузка текстур
    texture = Texture("../data/textures/leafs.png")
    texture.load()

    texture_cobblestone = Texture("../data/textures/grassy_cobblestone.jpg")
    texture_cobblestone.load()

    # Создаем направленный свет
    directional_light = DirectionalLight(direction=[-0.2, -1.0, -0.3],
                                         ambient=[0.05, 0.05, 0.05],
                                         diffuse=[1.0, 1.0, 1.0],
                                         specular=[1.0, 1.0, 1.0])
    scene.add_light(directional_light)

    # Создаем анимацию вращения направленного света
    light_animation = DirectionalLightRotationAnimation(light=directional_light,
                                                        axis=[0.0, 1.0, 0.0],  # Вращение вокруг Y-оси
                                                        speed=60.0)  # 30 градусов в секунду
    scene.add_animation(light_animation)
    light_animation.start()  # Запускаем анимацию

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

    # Устанавливаем сцену в окно рендеринга
    window.set_scene(scene)

    # Запускаем рендеринг
    window.run()


if __name__ == "__main__":
    main()
