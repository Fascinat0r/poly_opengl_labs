from lab_kr.animations.directional_light_rotation_animation import DirectionalLightRotationAnimation
from lab_kr.camera import Camera
from lab_kr.light.directional_light import DirectionalLight
from lab_kr.materials.material import Material
from lab_kr.materials.textures import ImageTexture, FlatTexture
from lab_kr.particles.emitters.cone_emitter import ConeEmitter
from lab_kr.render_window import RenderWindow
from lab_kr.scene import Scene
from lab_kr.shapes.plane import Plane
from lab_kr.shapes.cone import Cone
from lab_kr.shapes.sphere import Sphere
from lab_kr.shapes.point import Point


def main():
    # Создаем окно рендеринга
    window = RenderWindow(800, 600, b"Course Work with Cone Emitter")

    # Создаем сцену
    scene = Scene()

    # Создаем камеру
    camera = Camera(position=[0.0, 2.0, 5.0], up=[0.0, 1.0, 0.0], yaw=-90.0, pitch=-20.0)
    scene.set_camera(camera)

    # Загрузка текстур
    texture_cobblestone = ImageTexture("../data/textures/grassy_cobblestone.jpg")
    texture_cobblestone.load()

    texture_leafs = ImageTexture("../data/textures/leafs.png")
    texture_leafs.load()


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

    # Создаем визуальный конус
    cone_material = Material(
        ambient=[0.1, 0.1, 0.1],
        diffuse=[0.8, 0.5, 0.3],
        specular=[0.5, 0.5, 0.5],
        shininess=32.0,
        texture=texture_leafs.texture_id,
        transparent=False
    )
    cone = Cone(
        base_radius=1.0,
        height=2.0,
        slices=30,
        position=[0.0, 0.0, 0.0],
        rotation=[0.0, 0.0, 0.0],
        material=cone_material
    )
    scene.add_object(cone)

    # КУРСОВАЯ РАБОТА
    scene.initialize_particle_system()

    point = Point(position=[0.0, 3.0, 0.0], size=15.0, color=[1.0, 0.0, 0.0, 1.0])  # Красная точка
    scene.add_object(point)

    # Создаем эмиттер для конуса
    cone_emitter = ConeEmitter(
        position=cone.position,  # Позиция совпадает с вершиной конуса
        rotation=cone.rotation,  # Передаем поворот конуса
        emission_rate=50,
        max_particles=500,
        speed_range=(1.0, 3.0),  # Скорость частиц
        size_range=(6.5, 7.5),  # Размер частиц
        color=[0, 0, 0, 255],  # Красный цвет
        lifetime=3.0,
        base_radius=1.0,
        height=2.0
    )
    scene.add_emitter_to_particle_system(cone_emitter)

    # Устанавливаем сцену в окно рендеринга
    window.set_scene(scene)

    # Запускаем рендеринг
    window.run()


if __name__ == "__main__":
    main()
