from lab3.animations.directional_light_rotation_animation import DirectionalLightRotationAnimation
from lab3.animations.looped_movement_animation import LoopedMovementAnimation
from lab3.camera import Camera
from lab3.light.directional_light import DirectionalLight
from lab3.materials.material import Material
from lab3.materials.textures import ImageTexture, FlatTexture
from lab3.render_window import RenderWindow
from lab3.scene import Scene
from lab3.shapes.cone import Cone
from lab3.shapes.cube import Cube
from lab3.shapes.cylinder import Cylinder
from lab3.shapes.octahedron import Octahedron
from lab3.shapes.plane import Plane
from lab3.shapes.sphere import Sphere
from lab3.shapes.teapot import Teapot
from lab3.shapes.torus import Torus


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
    texture = ImageTexture("../data/textures/wool.jpg")
    texture.load()

    texture_cobblestone = ImageTexture("../data/textures/grass.jpg")
    texture_cobblestone.load()

    blue_texture = FlatTexture(color=[80.0, 80.0, 255.0])
    blue_texture.load()

    red_texture = FlatTexture(color=[255.0, 80.0, 80.0])
    red_texture.load()

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
        texture=texture_cobblestone.texture_id,
        transparent=False
    )

    # Создаем объект плоскости
    floor = Plane(position=[0.0, 0.0, 0.0], scale=40.0, rotation=[0.0, 0.0, 0.0], material=floor_material)
    scene.add_object(floor)

    # Создаем материалы для объектов
    textured_material = Material(
        ambient=[0.1, 0.1, 0.1],
        diffuse=[0.8, 0.8, 0.8],
        specular=[0.5, 0.5, 0.5],
        shininess=32.0,
        texture=texture.texture_id,
        transparent=True
    )

    glossy_material = Material(
        ambient=[0.0, 0.0, 0.0],
        diffuse=[0.55, 0.55, 0.55],
        specular=[0.7, 0.7, 0.7],
        shininess=32.0,
        texture=blue_texture.texture_id,
        transparent=False
    )

    diffuse_material = Material(
        ambient=[0.1, 0.1, 0.1],
        diffuse=[0.8, 0.8, 0.8],
        specular=[0.5, 0.5, 0.5],
        shininess=32.0,
        texture=red_texture.texture_id,
        transparent=False
    )

    # Создаем объекты и применяем материалы

    cone = Cone(base_radius=1.0, height=2.0, slices=20, position=[-3.0, 0.0, -5.0], scale=1.0,
                rotation=[0.0, 0.0, 0.0], material=diffuse_material)
    scene.add_object(cone)

    cube = Cube(position=[-1.0, 1.0, 4.0], scale=1.0, rotation=[0.0, 0.0, 0.0], material=glossy_material)
    scene.add_object(cube)

    sphere = Sphere(radius=1,
                    stacks=20,
                    slices=20,
                    position=[2.0, 2.0, 2.0],
                    scale=[1.0, 1.0, 1.0],
                    rotation=[0.0, 0.0, 0.0],
                    material=textured_material)

    scene.add_object(sphere)

    cylinder = Cylinder(base_radius=1.0,
                        top_radius=1.0,
                        height=2.0,
                        slices=20,
                        position=[-2.0, 0.0, 2.0],
                        scale=[1.0, 1.0, 1.0],
                        rotation=[0.0, 0.0, 0.0],
                        material=glossy_material)
    scene.add_object(cylinder)

    # Устанавливаем сцену в окно рендеринга
    window.set_scene(scene)

    # Запускаем рендеринг
    window.run()


if __name__ == "__main__":
    main()
