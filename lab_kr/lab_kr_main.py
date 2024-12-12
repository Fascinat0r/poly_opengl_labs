from lab_kr.animations.directional_light_rotation_animation import DirectionalLightRotationAnimation
from lab_kr.camera import Camera
from lab_kr.light.directional_light import DirectionalLight
from lab_kr.materials.material import Material
from lab_kr.materials.textures import ImageTexture, FlatTexture
from lab_kr.particles.emitters.directed_emitter import DirectedEmitter
from lab_kr.render_window import RenderWindow
from lab_kr.scene import Scene
from lab_kr.shapes.plane import Plane


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
    texture = ImageTexture("../data/textures/kanye.png")
    texture.load()

    texture_cobblestone = ImageTexture("../data/textures/bandera.jpg")
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
    floor = Plane(position=[0.0, 0.0, 0.0], scale=40.0, rotation=[0.0, 180.0, 0.0], material=floor_material)
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

    # Создаем объекты и применяем материалы

    plane = Plane(position=[0.0, 5.0, 0.0], scale=10.0, rotation=[90.0, 180.0, .0], material=textured_material)
    scene.add_object(plane)

    scene.initialize_particle_system()
    # Эмиттер – направленный источник
    cone_emitter = DirectedEmitter(
        position=[0.0, 8, 3],
        emission_rate=100,
        max_particles=1000,
        speed_range=(6.0, 8.0),
        size_range=(1.0, 5.0),
        color=[255, 255, 255, 255],
        lifetime=1.0,
        main_direction=[0.5, 0, -1],  # Направление испускания частиц
        max_angle=15.0  # максимальный угол отклонения от направления
    )
    scene.add_emitter_to_particle_system(cone_emitter)

    # Устанавливаем сцену в окно рендеринга
    window.set_scene(scene)

    # Запускаем рендеринг
    window.run()


if __name__ == "__main__":
    main()
