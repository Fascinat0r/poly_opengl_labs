# Гайд по второй лабораторной работе по графике: Материалы и Освещение

## Введение

Вторая лабораторная работа (`lab2`) расширяет функциональность первой (`lab1`), добавляя поддержку материалов и освещения в 3D-сцену. Основные улучшения включают:

- **Материалы**: Возможность задавать свойства материалов, такие как цвет, блеск, зеркальность, диффузность, текстуры и прозрачность.
- **Освещение**: Добавление источников света (например, точечного света) и управление их параметрами.
- **Текстурирование**: Применение текстур к объектам для более реалистичного внешнего вида.
- **Нормали**: Добавление нормалей к вершинам объектов для корректного расчета освещения.

Этот гайд фокусируется на нововведениях и обновлениях, основываясь на предыдущем руководстве по первой лабораторной работе.

---

## Структура проекта `lab2`

Проект организован следующим образом:

```
lab2/
├── animations/           # Анимации для объектов и источников света
│   ├── animation.py
│   ├── ligth_rotation_animation.py
│   ├── looped_movement_animation.py
│   ├── looped_rotation_animation.py
├── light/                # Источники света
│   ├── point_light.py
├── materials/            # Материалы и текстуры
│   ├── material.py
│   ├── textures.py
├── shapes/               # 3D-объекты (фигуры) с поддержкой материалов и нормалей
│   ├── cone.py
│   ├── cube.py
│   ├── cylinder.py
│   ├── octahedron.py
│   ├── shape.py          # Базовый класс для фигур
│   ├── sphere.py
│   ├── teapot.py
│   ├── torus.py
│   ├── utils.py          # Вспомогательные функции для отрисовки
├── camera.py             # Камера для работы со сценой
├── handlers.py           # Обработчики ввода (клавиатура, мышь)
├── render_window.py      # Окно рендеринга и основной цикл
├── scene.py              # Сцена с объектами, светом и анимациями
└── lab2_main.py          # Главный файл проекта
```

---

## План объяснения

1. **Расширение функциональности первой лабораторной работы**
2. **Материалы: определение и применение**
3. **Текстурирование: загрузка и применение текстур**
4. **Освещение: добавление и управление источниками света**
5. **Обновленные 3D-объекты с нормалями и материалами**
6. **Анимации освещения**
7. **Интеграция материалов и освещения в сцену**
8. **Заключение**

---

## 1. Расширение функциональности первой лабораторной работы

В первой лабораторной работе мы создали базовую 3D-сцену с объектами, камерой и простыми анимациями. Во второй лабораторной работе мы добавляем:

- **Материалы**: Определение свойств поверхности объектов.
- **Освещение**: Создание и настройка источников света для улучшения визуализации.
- **Текстурирование**: Применение изображений на поверхности объектов для повышения реалистичности.
- **Нормали**: Добавление нормальных векторов для корректного расчета освещения.

---

## 2. Материалы: определение и применение

### Класс `Material` (`materials/material.py`)

Класс `Material` отвечает за свойства поверхности объектов, такие как цвет, блеск, зеркальность, диффузность, текстуры и прозрачность.

**Основные атрибуты:**

- `color`: Основной цвет объекта с альфа-каналом для прозрачности.
- `shininess`: Коэффициент блеска (зеркальности).
- `specular`: Зеркальный цвет.
- `diffuse`: Диффузный цвет.
- `texture`: Идентификатор текстуры (если используется).
- `transparent`: Флаг прозрачности объекта.

**Пример применения материала:**

```python
class Material:
    def __init__(self, color=[1.0, 1.0, 1.0, 0.0], shininess=0.0, specular=[1.0, 1.0, 1.0, 1.0],
                 diffuse=[1.0, 1.0, 1.0, 1.0], texture=None, transparent=False):
        # Инициализация атрибутов
        self.color = color
        self.shininess = shininess
        self.specular = specular
        self.diffuse = diffuse
        self.texture = texture
        self.transparent = transparent

    def apply(self):
        """Применение материала к объекту перед его рендерингом."""
        glColor4f(*self.color)
        if self.transparent:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glDepthMask(GL_FALSE)
        else:
            glDisable(GL_BLEND)
            glDepthMask(GL_TRUE)

        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.specular)
        glMaterialf(GL_FRONT, GL_SHININESS, min(self.shininess, 128.0))

        if self.texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)
        else:
            glDisable(GL_TEXTURE_2D)

    def cleanup(self):
        """Очистка после применения прозрачности и текстуры."""
        if self.transparent:
            glDepthMask(GL_TRUE)
            glDisable(GL_BLEND)
        if self.texture:
            glDisable(GL_TEXTURE_2D)
```

### Применение материала в фигурах

Каждая фигура теперь имеет атрибут `material`, который применяется при рендеринге:

```python
class Shape(ABC):
    def __init__(self, position, scale, rotation, color=[1.0, 1.0, 1.0, 1.0],
                 material=None):
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.material = material if material else Material(color=color)

    def render(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1.0, 0.0, 0.0)
        glRotatef(self.rotation[1], 0.0, 1.0, 0.0)
        glRotatef(self.rotation[2], 0.0, 0.0, 1.0)
        glScalef(self.scale, self.scale, self.scale)

        self.material.apply()
        self.draw()
        self.material.cleanup()

        self.draw_center_axes()
        glPopMatrix()
```

---

## 3. Текстурирование: загрузка и применение текстур

### Класс `Texture` (`materials/textures.py`)

Класс `Texture` отвечает за загрузку изображений и их привязку к объектам в OpenGL.

**Основные методы:**

- `load()`: Загружает изображение из файла и создает текстуру OpenGL.
- `apply()`: Применяет текстуру при рендеринге объекта.

**Пример загрузки текстуры:**

```python
class Texture:
    def __init__(self, texture_path):
        self.texture_path = texture_path
        self.texture_id = glGenTextures(1)

    def load(self):
        """Загружаем текстуру и привязываем её к объекту OpenGL."""
        image = Image.open(self.texture_path)
        if image.mode == "RGBA":
            img_data = image.tobytes("raw", "RGBA", 0, -1)
            format = GL_RGBA
        else:
            img_data = image.tobytes("raw", "RGB", 0, -1)
            format = GL_RGB

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, format, image.width, image.height, 0, format, GL_UNSIGNED_BYTE, img_data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glEnable(GL_TEXTURE_2D)

    def apply(self):
        """Применение текстуры."""
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
```

### Применение текстур к фигурам

Фигуры используют текстурные координаты (`glTexCoord2f`) при отрисовке граней. Пример:

```python
def draw_quad(v1, v2, v3, v4, n, uv1, uv2, uv3, uv4):
    glNormal3fv(n)
    glTexCoord2f(*uv1)
    glVertex3fv(v1)
    glTexCoord2f(*uv2)
    glVertex3fv(v2)
    glTexCoord2f(*uv3)
    glVertex3fv(v3)
    glTexCoord2f(*uv4)
    glVertex3fv(v4)
```

---

## 4. Освещение: добавление и управление источниками света

### Класс `PointLight` (`light/point_light.py`)

Класс `PointLight` представляет точечный источник света с параметрами освещения и затухания.

**Основные атрибуты:**

- `position`: Позиция света `[x, y, z, w]`, где `w=1.0` для точечного источника.
- `ambient`: Фоновое освещение.
- `diffuse`: Рассеянный свет.
- `specular`: Зеркальный свет.
- `attenuation`: Затухание света `[constant, linear, quadratic]`.

**Пример применения света:**

```python
class PointLight:
    def __init__(self, position=[0.0, 0.0, 1.0, 1.0],
                 ambient=[0.05, 0.05, 0.05, 1.0],
                 diffuse=[1.0, 1.0, 1.0, 1.0],
                 specular=[1.0, 1.0, 1.0, 1.0],
                 attenuation=[1.0, 0.1, 0.01]):
        global next_id
        self.light_id = ids[next_id]
        next_id += 1
        self.position = position
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.attenuation = attenuation

    def apply(self):
        """Применение параметров точечного источника света."""
        glEnable(self.light_id)
        glLightfv(self.light_id, GL_POSITION, self.position)
        glLightfv(self.light_id, GL_AMBIENT, self.ambient)
        glLightfv(self.light_id, GL_DIFFUSE, self.diffuse)
        glLightfv(self.light_id, GL_SPECULAR, self.specular)
        glLightf(self.light_id, GL_CONSTANT_ATTENUATION, self.attenuation[0])
        glLightf(self.light_id, GL_LINEAR_ATTENUATION, self.attenuation[1])
        glLightf(self.light_id, GL_QUADRATIC_ATTENUATION, self.attenuation[2])

    def set_position(self, position):
        """Обновление позиции источника света."""
        self.position = position
        glLightfv(self.light_id, GL_POSITION, self.position)

    def draw_indicator(self):
        """Рисование индикатора источника света в виде маленькой сферы."""
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 0.0)
        glutSolidSphere(0.1, 20, 20)
        glEnable(GL_LIGHTING)
        glPopMatrix()
```

### Настройка освещения в сцене

В `scene.py` добавляются источники света, которые применяются к сцене:

```python
class Scene:
    def __init__(self):
        self.camera = None
        self.lights = []
        self.objects = []
        self.animations = []
        self.last_update_time = glutGet(GLUT_ELAPSED_TIME)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

    def add_light(self, light: PointLight):
        """Добавляем источник света в сцену."""
        light.apply()
        self.lights.append(light)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        position, target, up = self.camera.get_view_matrix()
        gluLookAt(position[0], position[1], position[2],
                  target[0], target[1], target[2],
                  up[0], up[1], up[2])

        self.update_animations()
        self.draw_grid()
        self.draw_axes()

        for light in self.lights:
            light.draw_indicator()

        opaque_objects, transparent_objects = self.sort_objects()

        for obj in opaque_objects:
            obj.render()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(GL_FALSE)

        for obj in transparent_objects:
            obj.render()

        glDepthMask(GL_TRUE)
        glDisable(GL_BLEND)

        glutSwapBuffers()
```

---

## 5. Обновленные 3D-объекты с нормалями и материалами

### Добавление нормалей

Нормали необходимы для корректного расчета освещения. Они определяют направление, в котором поверхность объекта "смотрит".

**Пример добавления нормалей в `Cone` (`shapes/cone.py`):**

```python
def draw_surface(self):
    triangles = []
    tip = [0.0, self.height, 0.0]

    for i in range(self.slices):
        theta = 2.0 * math.pi * i / self.slices
        next_theta = 2.0 * math.pi * (i + 1) / self.slices

        x1 = self.base_radius * math.cos(theta)
        z1 = self.base_radius * math.sin(theta)
        x2 = self.base_radius * math.cos(next_theta)
        z2 = self.base_radius * math.sin(next_theta)

        normal = [x1 + x2, self.height, z1 + z2]
        length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
        normal = [n / length for n in normal]

        triangles.append((tip, [x1, 0.0, z1], [x2, 0.0, z2], normal, uv_tip, uv1, uv2))

    batch_draw_triangles(triangles)

    # Основание конуса
    glBegin(GL_TRIANGLE_FAN)
    glNormal3fv([0.0, -1.0, 0.0])
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 0.0)
    for i in range(self.slices + 1):
        theta = 2.0 * math.pi * i / self.slices
        x = self.base_radius * math.cos(theta)
        z = self.base_radius * math.sin(theta)
        uv = [0.5 + 0.5 * math.cos(theta), 0.5 + 0.5 * math.sin(theta)]
        glTexCoord2f(*uv)
        glVertex3f(x, 0.0, z)
    glEnd()
```

### Применение материалов к фигурам

Каждая фигура использует свой материал для определения внешнего вида. Пример создания и применения материала в `lab2_main.py`:

```python
# Создаем материалы
transparent_material = Material(
    color=[0.8, 0.0, 0.0, 0.5],
    shininess=50,
    specular=[1.0, 1.0, 1.0, 1.0],
    diffuse=[0.2, 0.2, 0.2, 0.5],
    transparent=True
)

polished_material = Material(
    color=[0.2, 0.2, 0.6, 1.0],
    shininess=128,
    specular=[2.0, 2.0, 2.0, 1.0],
    diffuse=[0.4, 0.4, 0.4, 1.0],
)

diffuse_material = Material(
    color=[0.8, 0.8, 0.0, 1.0],
    shininess=10,
    specular=[0.1, 0.1, 0.1, 1.0],
    diffuse=[0.6, 0.6, 0.6, 1.0]
)

background_material = Material(
    color=[0.1, 0.1, 0.1, 1.0],
    shininess=10,
    specular=[0.1, 0.1, 0.1, 1.0],
    diffuse=[0.1, 0.1, 0.1, 1.0]
)

# Применение материалов к объектам
room = Cube(position=[0.0, 9.0, 0.0], scale=20.0, material=background_material)
scene.add_object(room)

textured_oct = Octahedron(position=[1.0, 1.0, -5.0], scale=2.0, material=textured_cube_material)
scene.add_object(textured_oct)

polished_teapot = Teapot(position=[-3.0, 1.0, 0.0], scale=1.0, material=polished_material)
scene.add_object(polished_teapot)

transparent_torus = Torus(inner_radius=0.5, outer_radius=1.0, rings=20, sides=20,
                          position=[0.5, 1.0, 0.0], scale=1.0, material=transparent_material)
scene.add_object(transparent_torus)

matte_cone = Cone(position=[3.0, 0.0, 0.0], scale=1.0, material=diffuse_material)
scene.add_object(matte_cone)
```

---

## 6. Анимации освещения

### Класс `LightRotationAnimation` (`animations/ligth_rotation_animation.py`)

Позволяет анимировать движение источника света по круговой траектории.

**Основные атрибуты:**

- `light`: Объект источника света (`PointLight`).
- `radius`: Радиус круга, по которому движется свет.
- `speed`: Скорость вращения в градусах в секунду.
- `angle`: Текущий угол вращения.

**Пример реализации:**

```python
class LightRotationAnimation(Animation):
    def __init__(self, light, radius=5.0, speed=30.0):
        super().__init__(light)
        self.radius = radius
        self.speed = speed
        self.angle = 0.0

    def start(self):
        self.running = True

    def update(self, light, delta_time):
        if not self.running:
            return

        self.angle += self.speed * delta_time
        self.angle %= 360

        new_x = self.radius * math.cos(math.radians(self.angle))
        new_z = self.radius * math.sin(math.radians(self.angle))

        light.set_position([new_x, light.position[1], new_z, 1.0])
```

### Добавление анимации в сцену (`lab2_main.py`)

```python
# Создаем анимацию вращения источника света
light_rotation_animation = LightRotationAnimation(point_light, radius=5.0, speed=30.0)
light_rotation_animation.start()
scene.add_animation(light_rotation_animation)
```

---

## 7. Интеграция материалов и освещения в сцену

### Главный файл `lab2_main.py`

Этот файл инициализирует сцену, добавляет объекты с материалами, источники света и анимации.

**Основные шаги:**

1. **Создание окна рендеринга:**

    ```python
    window = RenderWindow(800, 600, b"Lab 2")
    ```

2. **Создание сцены и камеры:**

    ```python
    scene = Scene()
    camera = Camera([0.0, 0.0, 5.0], [0.0, 1.0, 0.0], -90.0, 0.0)
    scene.set_camera(camera)
    ```

3. **Загрузка текстуры:**

    ```python
    texture = Texture("../data/textures/leafs.png")
    texture.load()
    ```

4. **Создание и добавление источника света:**

    ```python
    point_light = PointLight(position=[0.0, 5.0, 5.0, 1.0],
                             ambient=[0.05, 0.05, 0.05, 1.0],
                             diffuse=[2.0, 2.0, 2.0, 2.0],
                             specular=[1.0, 1.0, 1.0, 1.0],
                             attenuation=[1.0, 0.1, 0.01])
    scene.add_light(point_light)
    ```

5. **Создание материалов:**

    ```python
    transparent_material = Material(
        color=[0.8, 0.0, 0.0, 0.5],
        shininess=50,
        specular=[1.0, 1.0, 1.0, 1.0],
        diffuse=[0.2, 0.2, 0.2, 0.5],
        transparent=True
    )

    polished_material = Material(
        color=[0.2, 0.2, 0.6, 1.0],
        shininess=128,
        specular=[2.0, 2.0, 2.0, 1.0],
        diffuse=[0.4, 0.4, 0.4, 1.0],
    )

    diffuse_material = Material(
        color=[0.8, 0.8, 0.0, 1.0],
        shininess=10,
        specular=[0.1, 0.1, 0.1, 1.0],
        diffuse=[0.6, 0.6, 0.6, 1.0]
    )

    background_material = Material(
        color=[0.1, 0.1, 0.1, 1.0],
        shininess=10,
        specular=[0.1, 0.1, 0.1, 1.0],
        diffuse=[0.1, 0.1, 0.1, 1.0]
    )
    ```

6. **Создание и добавление объектов с материалами:**

    ```python
    # Объект комнаты с матовым материалом
    room = Cube(position=[0.0, 9.0, 0.0], scale=20.0, material=background_material)
    scene.add_object(room)

    # Текстурированный октаэдр с материалом
    textured_oct = Octahedron(position=[1.0, 1.0, -5.0], scale=2.0, material=textured_cube_material)
    scene.add_object(textured_oct)

    # Полированный чайник
    polished_teapot = Teapot(position=[-3.0, 1.0, 0.0], scale=1.0, material=polished_material)
    scene.add_object(polished_teapot)

    # Прозрачный тор
    transparent_torus = Torus(inner_radius=0.5, outer_radius=1.0, rings=20, sides=20,
                              position=[0.5, 1.0, 0.0], scale=1.0, material=transparent_material)
    scene.add_object(transparent_torus)

    # Матовый конус
    matte_cone = Cone(position=[3.0, 0.0, 0.0], scale=1.0, material=diffuse_material)
    scene.add_object(matte_cone)
    ```

7. **Добавление анимации источника света:**

    ```python
    light_rotation_animation = LightRotationAnimation(point_light, radius=5.0, speed=30.0)
    light_rotation_animation.start()
    scene.add_animation(light_rotation_animation)
    ```

8. **Запуск окна рендеринга:**

    ```python
    window.set_scene(scene)
    window.run()
    ```

---

## 8. Заключение

Вторая лабораторная работа значительно расширяет возможности первой, добавляя поддержку материалов, текстур и освещения. Это позволяет создавать более реалистичные и визуально привлекательные 3D-сцены. 

**Ключевые моменты:**

- **Материалы**: Позволяют настраивать свойства поверхностей объектов, такие как цвет, блеск и прозрачность.
- **Текстуры**: Добавляют детализацию поверхностям объектов, делая их более реалистичными.
- **Освещение**: Улучшает восприятие формы и глубины объектов, создавая тени и отражения.
- **Нормали**: Необходимы для корректного расчета взаимодействия света с поверхностью объекта.

**Рекомендации для дальнейшего изучения:**

- **Расширение типов источников света**: Добавление направленных и рассеянных источников света.
- **Использование шейдеров**: Переход на использование шейдеров (GLSL) для более гибкого и мощного управления графикой.
- **Текстурирование более сложных объектов**: Применение различных типов текстур, таких как нормальные карты или карты отражений.
- **Добавление эффектов постобработки**: Такие как размытие, освещение с глобальным освещением и т.д.

Этот гайд предоставляет основы для понимания и дальнейшего развития проекта по материалам и освещению в OpenGL на Python.