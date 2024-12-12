from lab_kr.animations.directional_light_rotation_animation import DirectionalLightRotationAnimation
from lab_kr.camera import Camera
from lab_kr.light.directional_light import DirectionalLight
from lab_kr.materials.material import Material
from lab_kr.materials.textures import ImageTexture, FlatTexture

from lab_kr.particles.emitters.cone_emitter import ConeEmitter
from lab_kr.render_window import RenderWindow
from lab_kr.scene import Scene
from lab_kr.shapes.cone import Cone
from lab_kr.shapes.plane import Plane
from lab_kr.shapes.sphere import Sphere


def main():
    # Создаем окно рендеринга
    width, height = 1024, 768
    window = RenderWindow(width, height, b"Course Work")

    # Создаем сцену
    scene = Scene()

    # Создаем камеру
    camera = Camera(position=[0.0, 2.0, 5.0], up=[0.0, 1.0, 0.0],
                    yaw=-75.0, pitch=-5.0, zoom=60.0, aspect_ratio=width/height)
    scene.set_camera(camera)

    # Загрузка текстур
    texture = ImageTexture("../data/textures/emerald.jpg")
    texture.load()

    texture_cobblestone = ImageTexture("../data/textures/grassy_cobblestone.jpg")
    texture_cobblestone.load()

    pink_texture = FlatTexture(color=[255.0, 192.0, 203.0])
    pink_texture.load()

    peach_texture = FlatTexture(color=[255.0, 210.0, 180.0, 255.0])
    peach_texture.load()

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

    sphere_material = Material(
        ambient=[0.2, 0.2, 0.2],
        diffuse=[0.3, 0.3, 0.3],
        specular=[0.8, 0.8, 0.8],
        shininess=2.0,
        texture=peach_texture.texture_id,
        transparent=False
    )

    # Создаем объект плоскости
    floor = Plane(position=[0.0, 0.0, 0.0], scale=40.0, rotation=[0.0, 0.0, 0.0], material=floor_material)
    scene.add_object(floor)

    sphere = Sphere(position=[2.0, 2.0, 1.0], material=sphere_material)
    scene.add_object(sphere)

    # Создаем визуальный конус
    cone_material = Material(
        ambient=[0.1, 0.1, 0.1],
        diffuse=[0.8, 0.5, 0.3],
        specular=[0.5, 0.5, 0.5],
        shininess=32.0,
        texture=texture.texture_id,
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

    # Создаем эмиттер для конуса
    cone_emitter = ConeEmitter(
        position=cone.position,  # Позиция совпадает с вершиной конуса
        rotation=cone.rotation,  # Передаем поворот конуса
        emission_rate=100,
        max_particles=1000,
        speed_range=(1.0, 3.0),
        size_range=(6.5, 7.5),
        color=[50, 123, 240, 255],
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
