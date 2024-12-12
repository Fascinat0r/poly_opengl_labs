from lab3.animations.directional_light_rotation_animation import DirectionalLightRotationAnimation
from lab3.animations.looped_movement_animation import LoopedMovementAnimation
from lab3.camera import Camera
from lab3.light.directional_light import DirectionalLight
from lab3.materials.material import Material
from lab3.materials.textures import ImageTexture, FlatTexture
from lab3.render_window import RenderWindow
from lab3.scene import Scene
from lab3.shapes.cube import Cube
from lab3.shapes.plane import Plane
from lab3.shapes.sphere import Sphere


def main():
    # Создаем окно рендеринга
    width, height = 1024, 768
    window = RenderWindow(width, height, b"Lab 3 with Shadows and Shapes")

    # Создаем сцену
    scene = Scene()

    # Создаем камеру
    camera = Camera(position=[0.0, 2.0, 5.0], up=[0.0, 1.0, 0.0],
                    yaw=-75.0, pitch=-5.0, zoom=60.0, aspect_ratio=width / height)
    scene.set_camera(camera)

    # Загрузка текстур
    texture1 = ImageTexture("../data/textures/carpet.jpg")
    texture1.load()

    texture2 = ImageTexture("../data/textures/mandala.jpg")
    texture2.load()

    mirt_texture = FlatTexture(color=[33.0, 66.0, 30.0])
    mirt_texture.load()

    terracota_texture = FlatTexture(color=[204.0, 78.0, 92.0])
    terracota_texture.load()

    # Создаем направленный свет
    directional_light = DirectionalLight(direction=[-0.2, -1.0, -0.3],
                                         ambient=[0.05, 0.05, 0.05],
                                         diffuse=[0.9, 0.9, 0.9],
                                         specular=[0.8, 0.8, 0.8])
    scene.add_light(directional_light)

    # Создаем анимацию вращения направленного света
    light_animation = DirectionalLightRotationAnimation(light=directional_light,
                                                        axis=[0.0, 1.0, 0.5],  # Вращение вокруг Y-оси
                                                        speed=60.0)  # 60 градусов в секунду
    scene.add_animation(light_animation)
    light_animation.start()  # Запускаем анимацию

    # Создаем материал для пола
    floor_material = Material(
        ambient=[0.1, 0.1, 0.1],
        diffuse=[0.5, 0.5, 0.5],
        specular=[0.2, 0.2, 0.2],
        shininess=10.0,
        texture=texture1.texture_id,
        transparent=False
    )

    # Создаем объект плоскости
    floor = Plane(position=[0.0, 0.0, 0.0], scale=40.0, rotation=[0.0, 0.0, 0.0], material=floor_material)
    scene.add_object(floor)

    # Создаем материалы для объектов
    textured_cube_material = Material(
        ambient=[0.1, 0.1, 0.1],
        diffuse=[0.8, 0.8, 0.8],
        specular=[0.5, 0.5, 0.5],
        shininess=32.0,
        texture=texture2.texture_id,
        transparent=True
    )

    glossy_material = Material(
        ambient=[0.0, 0.0, 0.0],
        diffuse=[0.55, 0.55, 0.55],
        specular=[0.7, 0.7, 0.7],
        shininess=32.0,
        texture=mirt_texture.texture_id,
        transparent=False
    )

    diffuse_material = Material(
        ambient=[0.1, 0.1, 0.1],
        diffuse=[0.8, 0.8, 0.8],
        specular=[0.5, 0.5, 0.5],
        shininess=32.0,
        texture=terracota_texture.texture_id,
        transparent=False
    )

    materials = [textured_cube_material, glossy_material, diffuse_material]

    # Создаем объекты
    for idx, material in enumerate(materials):
        cube = Cube(position=[-2.0 + idx * 2.0, 1.0, 0.0], scale=1.0, material=material)
        scene.add_object(cube)

        sphere = Sphere(position=[-2.0 + idx * 2.0, 1.0, 2.0], scale=1.0, material=material)
        scene.add_object(sphere)

        move_animation = LoopedMovementAnimation(target_object=sphere,
                                                 start_position=[-2.0 + idx * 2.0, 3.0, 2.0],
                                                 end_position=[-2.0 + idx * 2.0, 3.0, -2.0],
                                                 speeds=[0.0, 0.0, 1.0],
                                                 tolerance=0.01)
        move_animation.start()
        scene.add_animation(move_animation)

    # Устанавливаем сцену в окно рендеринга
    window.set_scene(scene)

    # Запускаем рендеринг
    window.run()


if __name__ == "__main__":
    main()
