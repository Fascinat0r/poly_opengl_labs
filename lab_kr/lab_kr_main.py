from lab_kr.animations.directional_light_rotation_animation import DirectionalLightRotationAnimation
from lab_kr.camera import Camera
from lab_kr.light.directional_light import DirectionalLight
from lab_kr.materials.material import Material
from lab_kr.materials.textures import ImageTexture, FlatTexture
from lab_kr.particles.emitters.cone_emitter import ConeEmitter
from lab_kr.particles.emitters.plane_emitter import PlaneEmitter
from lab_kr.particles.emitters.point_emitter import PointEmitter
from lab_kr.render_window import RenderWindow
from lab_kr.scene import Scene
from lab_kr.shapes.cube import Cube
from lab_kr.shapes.plane import Plane


def main():
    # Создаем окно рендеринга
    window = RenderWindow(800, 600, b"Course Work")

    # Создаем сцену
    scene = Scene()

    # Создаем камеру
    camera = Camera(position=[0.0, 2.0, 5.0], up=[0.0, 1.0, 0.0], yaw=-90.0, pitch=-20.0)
    scene.set_camera(camera)

    # Загрузка текстур
    texture = ImageTexture("../data/textures/emerald.jpg")
    texture.load()

    texture_cobblestone = ImageTexture("../data/textures/grassy_cobblestone.jpg")
    texture_cobblestone.load()

    pink_texture = FlatTexture(color=[255.0, 192.0, 203.0])
    pink_texture.load()

    peach_texture = FlatTexture(color=[255.0, 210.0, 180.0])
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

    # Создаем объект плоскости
    floor = Plane(position=[0.0, 0.0, 0.0], scale=40.0, rotation=[0.0, 0.0, 0.0], material=floor_material)
    scene.add_object(floor)

    # Создаем материалы для объектов
    textured_cube_material = Material(
        ambient=[0.1, 0.1, 0.1],
        diffuse=[0.8, 0.8, 0.8],
        specular=[0.5, 0.5, 0.5],
        shininess=32.0,
        texture=texture.texture_id,
        transparent=True
    )

    # Создаем объекты и применяем материалы
    textured_cube = Cube(position=[0.0, 0.5, 0.0], scale=1.0, rotation=[0.0, 0.0, 0.0],
                         material=textured_cube_material)
    scene.add_object(textured_cube)

    # КУРСОВАЯ РАБОТА
    scene.initialize_particle_system()

    # Пример 1: Эмиттер – точка
    point_emitter = PointEmitter(
        position=[0.0, 2.0, 0.0],
        emission_rate=100,
        max_particles=1000,
        speed_range=(1.0, 3.0),
        size_range=(2.0, 5.0),
        color=[255, 128, 255, 128],  # Белый цвет
        lifetime=5.0
    )
    scene.add_emitter_to_particle_system(point_emitter)

    # Пример 2: Эмиттер – конус
    cone_emitter = ConeEmitter(
        position=[-3.0, 2.0, -5.0],
        emission_rate=50,
        max_particles=500,
        speed_range=(2.0, 4.0),
        size_range=(1.0, 3.0),
        color=[255, 0, 0, 128],  # Красный цвет
        lifetime=3.0
    )
    scene.add_emitter_to_particle_system(cone_emitter)

    # Пример 3: Эмиттер – плоскость
    plane_emitter = PlaneEmitter(
        position=[3.0, 10.0, -4.0],
        emission_rate=75,
        max_particles=750,
        speed_range=(1.5, 3.5),
        size_range=(1.5, 4.0),
        color=[0, 255, 0, 128],  # Зеленый цвет
        lifetime=4.0,
        width=10,
        height=10
    )
    scene.add_emitter_to_particle_system(plane_emitter)

    # Устанавливаем сцену в окно рендеринга
    window.set_scene(scene)

    # Запускаем рендеринг
    window.run()


if __name__ == "__main__":
    main()
