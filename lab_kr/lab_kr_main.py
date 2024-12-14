from lab_kr.camera import Camera
from lab_kr.light.directional_light import DirectionalLight
from lab_kr.materials.material import Material
from lab_kr.materials.textures import ImageTexture
from lab_kr.particles.emitters.point_emitter import PointEmitter
from lab_kr.render_window import RenderWindow
from lab_kr.scene import Scene
from lab_kr.shapes.plane import Plane
from lab_kr.shapes.cylinder import Cylinder


def main():
    # Создаем окно рендеринга
    width, height = 1024, 768
    window = RenderWindow(width, height, b'Course work')

    # Создаем сцену
    scene = Scene()

    # Создаем камеру
    camera = Camera(position=[12.0, 3.5, 0.0], up=[0.0, 1.0, 0.0],
                    yaw=-180.0, pitch=5.0, zoom=60.0, aspect_ratio=width/height)
    scene.set_camera(camera)

    # Создаем направленный свет
    directional_light = DirectionalLight(direction=[-0.2, -1.0, -0.3],
                                         ambient=[0.05, 0.05, 0.05],
                                         diffuse=[0.9, 0.9, 0.9],
                                         specular=[0.8, 0.8, 0.8])
    scene.add_light(directional_light)

    # Загрузка текстур
    texture_cylinder = ImageTexture('../data/textures/grey-metal.jpg')
    texture_cylinder.load()

    texture_plane = ImageTexture('../data/textures/grey-bricks.jpg')
    texture_plane.load()

    # Создаем материал для пола
    floor_material = Material(
        ambient=[0.2, 0.2, 0.2],
        diffuse=[0.6, 0.6, 0.6],
        specular=[0.3, 0.3, 0.3],
        shininess=10.0,
        texture=texture_plane.texture_id,
        transparent=False
    )

    # Создаем объект плоскости
    floor = Plane(position=[0.0, 0.0, 0.0], scale=20.0, rotation=[0.0, 0.0, 0.0], material=floor_material)
    scene.add_object(floor)

    # Создаем материалы для объектов
    textured_material = Material(
        ambient=[0.3, 0.3, 0.3],
        diffuse=[0.8, 0.8, 0.8],
        specular=[0.6, 0.6, 0.6],
        shininess=32.0,
        texture=texture_cylinder.texture_id,
        transparent=False
    )

    # Создаем объекты и применяем материалы
    cylinder = Cylinder(position=[0.0, 2.0, -2.0], base_radius=2.0, top_radius=2.0, height=4.0, rotation=[90, 0, 0],
                        material=textured_material)
    scene.add_object(cylinder)

    scene.initialize_particle_system(range_of_effect=1.0)
    # Эмиттер – точка со случайным направлением испускания частиц
    point_emitter = PointEmitter(
        position=[3.5, 4.0, 0.0],
        emission_rate=100,
        max_particles=1000,
        speed_range=(6.0, 8.0),
        size_range=(4.0, 7.0),
        color=[255, 127, 0, 255],
        lifetime=5.0,
        color_fading=True,
        transparency_radius=9.0,
        has_trail=True
    )
    scene.add_emitter_to_particle_system(point_emitter)

    # Устанавливаем сцену в окно рендеринга
    window.set_scene(scene)

    # Запускаем рендеринг
    window.run()


if __name__ == "__main__":
    main()
