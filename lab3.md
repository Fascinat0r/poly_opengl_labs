# Гайд по третьей лабораторной работе по графике: Тени, Теневые Карты и Шейдеры

## Введение

Третья лабораторная работа (`lab3`) расширяет функциональность второй (`lab2`), внедряя реалистичные тени с использованием теневых карт и шейдеров. Основные улучшения включают:

- **Тени**: Добавление реалистичных теней объектов в сцене.
- **Теневые Карты (Shadow Maps)**: Использование буфера глубины для хранения информации о глубине от источника света.
- **Шейдеры**: Создание и использование вершинных и фрагментных шейдеров для рендеринга сцены с тенями.

Этот гайд фокусируется на нововведениях и обновлениях, основываясь на предыдущих лабораторных работах.

---

## Теория: Тени и Теневые Карты

### Тени в 3D-графике

Тени играют ключевую роль в повышении реализма сцены, показывая взаимное расположение объектов и источников света. Основные типы теней:

- **Реалистичные (Hard) Тени**: Четкие границы теней.
- **Мягкие (Soft) Тени**: Размытые границы, имитирующие реальные источники света.

### Теневые Карты (Shadow Mapping)

**Теневые карты** — это популярный метод создания теней в реальном времени. Процесс включает два прохода рендеринга:

1. **Depth Pass (Проход глубины)**:
   - Рендеринг сцены с точки зрения источника света.
   - Запись глубины каждого фрагмента в текстуру глубины (теневую карту).

2. **Render Pass (Основной проход)**:
   - Рендеринг сцены с точки зрения камеры.
   - Для каждого фрагмента проверяется, находится ли он в тени, сравнивая его глубину с глубиной, записанной в теневую карту.

**Преимущества теневых карт**:
- Относительная простота реализации.
- Поддержка динамических сцен и анимаций.

**Недостатки**:
- Возможны артефакты, такие как зебра-эффект (aliasing).
- Ограниченная точность из-за разрешения текстуры глубины.

### Шейдеры

**Шейдеры** — это программы, выполняемые на GPU, которые управляют процессом рендеринга графических объектов. Основные типы шейдеров:

- **Вершинный шейдер (Vertex Shader)**: Обрабатывает вершины объектов.
- **Фрагментный шейдер (Fragment Shader)**: Определяет цвет пикселей.

В `lab3` используются **шейдеры с поддержкой теней**, которые учитывают информацию из теневых карт при расчете освещения.

---

## Концептуальные Отличия от Второй Лабораторной Работы

Вторая лабораторная работа (`lab2`) фокусировалась на:

- **Материалах**: Определение свойств поверхностей объектов (цвет, блеск, текстуры).
- **Освещении**: Добавление источников света и управление их параметрами.
- **Текстурировании**: Применение текстур к объектам.
- **Нормалях**: Добавление нормальных векторов для корректного освещения.

Третья лабораторная работа (`lab3`) добавляет следующие концептуальные элементы:

- **Тени**: Реализация теней для объектов.
- **Теневые Карты**: Использование буфера глубины для создания теней.
- **Шейдеры для Теней**: Создание специализированных шейдеров для обработки теней.
- **Множественные Проходы Рендеринга**: Введение Depth Pass и Render Pass для создания теней.

---

## Реализация в Третьей Лабораторной Работе

### 1. Шейдеры для Теней

**Вершинный Шейдер (depth.vert)**:
- Преобразует вершины сцены в пространство источника света.
- Передает глубину фрагментов в текстуру глубины.

**Фрагментный Шейдер (depth.frag)**:
- Вычисляет глубину каждого фрагмента и записывает его в теневую карту.

**Вершинный Шейдер для Основного Прохода (shading.vert)**:
- Преобразует вершины сцены в пространство камеры и источника света.
- Передает необходимые данные в фрагментный шейдер.

**Фрагментный Шейдер для Основного Прохода (shading.frag)**:
- Использует теневую карту для определения, находится ли фрагмент в тени.
- Вычисляет финальный цвет фрагмента с учетом освещения и теней.

**Пример Фрагментного Шейдера для Теней (`shading.frag`)**:

```glsl
#version 330 core
out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;
in vec2 TexCoords;
in vec4 FragPosLightSpace;

uniform sampler2D diffuseTexture;
uniform sampler2D shadowMap;

uniform vec3 viewPos;

// Структура для направленного света
struct DirLight {
    vec3 direction;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

uniform DirLight dirLight;

// Функция для расчета теней
float ShadowCalculation(vec4 fragPosLightSpace)
{
    // Преобразование из пространств NDC
    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    // Преобразование в [0,1] диапазон
    projCoords = projCoords * 0.5 + 0.5;
    // Получение глубины из карты теней
    float closestDepth = texture(shadowMap, projCoords.xy).r; 
    float currentDepth = projCoords.z;
    // Порог для смещения (Bias) для предотвращения артефактов
    float bias = max(0.05 * (1.0 - dot(Normal, -dirLight.direction)), 0.005);
    // Проверка, находится ли текущий фрагмент в тени
    float shadow = currentDepth - bias > closestDepth ? 1.0 : 0.0;
    // Если фрагмент за пределами карты теней, он не в тени
    if(projCoords.z > 1.0)
        shadow = 0.0;
    return shadow;
}

void main()
{
    // Получение текстуры
    vec3 color = texture(diffuseTexture, TexCoords).rgb;
    // Нормализация нормали
    vec3 norm = normalize(Normal);
    // Направление света
    vec3 lightDir = normalize(-dirLight.direction);
    // Расчет диффузного компонента
    float diff = max(dot(norm, lightDir), 0.0);
    // Расчет зеркального компонента
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    // Расчет тени
    float shadow = ShadowCalculation(FragPosLightSpace);                      
    // Итоговое освещение
    vec3 ambient = dirLight.ambient * color;
    vec3 diffuse = dirLight.diffuse * diff * color;
    vec3 specular = dirLight.specular * spec;
    // Применение тени
    vec3 lighting = ambient + (1.0 - shadow) * (diffuse + specular);
    FragColor = vec4(lighting, 1.0);
}
```

### 2. Теневые Карты

**Класс `DepthMap` (`materials/depth_map.py`)**:
- Создает и управляет буфером глубины (теневой картой).
- Инициализирует Framebuffer Object (FBO) для рендеринга глубины.
- Предоставляет методы для привязки карты глубины для записи и чтения.

**Пример Инициализации Теневой Карты**:

```python
class DepthMap:
    def __init__(self, width=1024, height=1024):
        self.width = width
        self.height = height
        self.FBO = glGenFramebuffers(1)

        # Создание текстуры для карты глубины
        self.depth_map = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.depth_map)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, self.width, self.height, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        border_color = [1.0, 1.0, 1.0, 1.0]
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, border_color)

        # Привязка текстуры к FBO
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.depth_map, 0)
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
```

### 3. Изменения в Классе `Scene` (`scene.py`)

**Добавление Метода `render_depth_map`**:
- Выполняет Depth Pass: рендеринг сцены с точки зрения источника света для создания теневой карты.
- Настраивает матрицу пространства света (`lightSpaceMatrix`).

**Добавление Метода `render_scene`**:
- Выполняет Render Pass: основной рендеринг сцены с использованием теневой карты для определения теней.
- Передает параметры света и камеры в шейдеры.

**Пример Реализации Метода `render_depth_map`**:

```python
def render_depth_map(self, depth_shader: Shader):
    """Рендеринг сцены для создания карты глубины."""
    self.depth_map.bind_for_writing()
    glClear(GL_DEPTH_BUFFER_BIT)

    depth_shader.use()

    if not self.lights:
        print("No lights in the scene for depth map.")
        return

    # Предполагаем, что у нас один направленный свет
    light = self.lights[0]

    # Настраиваем lightSpaceMatrix на основе направления света.
    light_projection = glm.ortho(-10.0, 10.0, -10.0, 10.0, 1.0, 20.0)
    light_dir = glm.normalize(glm.vec3(*light.direction))
    light_position = glm.vec3(-light_dir.x * 10.0, -light_dir.y * 10.0, -light_dir.z * 10.0)
    light_view = glm.lookAt(light_position, glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))
    light_space_matrix = light_projection * light_view
    depth_shader.set_mat4("lightSpaceMatrix", light_space_matrix)

    # Рендерим все объекты
    for obj in self.objects:
        obj.render(depth_shader)

    glBindFramebuffer(GL_FRAMEBUFFER, 0)
```

### 4. Обновления в Классе `RenderWindow` (`render_window.py`)

**Добавление Проходов Рендеринга**:
- **Depth Pass**: Вызов `render_depth_map` для создания теневой карты.
- **Render Pass**: Вызов `render_scene` для основного рендеринга с тенями.

**Изменение Метода `render`**:

```python
def render(self):
    if not self.scene or not self.shader or not self.depth_shader:
        return

    # Обновляем анимации
    self.scene.update_animations()

    # Рисуем оси координат и сетку
    self.scene.draw_grid()
    self.scene.draw_axes()

    # Depth Pass
    self.scene.render_depth_map(self.depth_shader)

    # Render Pass
    self.shader.use()
    self.scene.render_scene(self.shader)

    glutSwapBuffers()
```

### 5. Класс `Shader` (`materials/shader.py`)

**Управление Шейдерами**:
- Загрузка, компиляция и связывание вершинных и фрагментных шейдеров.
- Методы для установки uniform-переменных (матрицы, цвета, текстур и т.д.).

**Пример Инициализации Шейдера**:

```python
class Shader:
    def __init__(self, vertex_source_path: str, fragment_source_path: str):
        # Чтение исходников шейдеров
        with open(vertex_source_path, 'r') as file:
            vertex_source = file.read()
        with open(fragment_source_path, 'r') as file:
            fragment_source = file.read()

        # Создание и компиляция вершинного шейдера
        vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(vertex_shader, vertex_source)
        gl.glCompileShader(vertex_shader)
        self._check_compile_errors(vertex_shader, "VERTEX")

        # Создание и компиляция фрагментного шейдера
        fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(fragment_shader, fragment_source)
        gl.glCompileShader(fragment_shader)
        self._check_compile_errors(fragment_shader, "FRAGMENT")

        # Создание шейдерной программы и связывание шейдеров
        self._program = gl.glCreateProgram()
        gl.glAttachShader(self._program, vertex_shader)
        gl.glAttachShader(self._program, fragment_shader)
        gl.glLinkProgram(self._program)
        self._check_compile_errors(self._program, "PROGRAM")

        # Удаление шейдеров после связывания
        gl.glDeleteShader(vertex_shader)
        gl.glDeleteShader(fragment_shader)

    def use(self):
        gl.glUseProgram(self._program)

    # Методы для установки uniform-переменных...
```

### 6. Обновления в Классах `Shape` и Его Подклассах

**Рендеринг с Шейдерами**:
- Каждый объект вызывает метод `render`, который устанавливает матрицу модели, применяет материал и вызывает метод `draw_mesh` с текущим шейдером.

**Пример Реализации Метода `render` в `Shape`**:

```python
def render(self, shader: Shader):
    """Отрисовка фигуры с применением трансформаций и материала."""
    # Создаем матрицу модели
    model = glm.mat4(1.0)
    model = glm.translate(model, glm.vec3(*self.position))
    model = glm.rotate(model, glm.radians(self.rotation[0]), glm.vec3(1.0, 0.0, 0.0))
    model = glm.rotate(model, glm.radians(self.rotation[1]), glm.vec3(0.0, 1.0, 0.0))
    model = glm.rotate(model, glm.radians(self.rotation[2]), glm.vec3(0.0, 0.0, 1.0))
    model = glm.scale(model, glm.vec3(self.scale))

    shader.set_mat4("model", model)

    # Применяем материал
    self.material.apply(shader)

    # Отрисовка геометрии
    self.draw_mesh(shader)

    # Очистка материала
    self.material.cleanup(shader)
```

**Обновления в Подклассах**:
- Подклассы, такие как `Cube`, `Sphere`, `Teapot`, и другие, реализуют метод `draw_mesh`, который выполняет рендеринг геометрии с использованием текущего шейдера.

---

## Ключевые Изменения и Добавления

1. **Теневые Карты**:
   - Введение класса `DepthMap` для управления буфером глубины.
   - Реализация Depth Pass и Render Pass в классе `Scene` и `RenderWindow`.

2. **Шейдеры с Поддержкой Теней**:
   - Создание и использование специализированных шейдеров (`depth.vert`, `depth.frag`, `shading.vert`, `shading.frag`).

3. **Изменение Класса `Light`**:
   - Введение класса `DirectionalLight` с поддержкой направления и параметров освещения.
   - Добавление методов для передачи параметров света в шейдеры.

4. **Обновление Класса `Scene`**:
   - Добавление методов `render_depth_map` и `render_scene` для управления проходами рендеринга.
   - Обновление матриц для пространства света (`lightSpaceMatrix`).

5. **Рендеринг Объектов**:
   - Обновление методов рендеринга объектов для использования шейдеров и теневых карт.

6. **Анимации**:
   - Добавление новых типов анимаций, таких как `DirectionalLightRotationAnimation`, для динамического изменения направления света и создания движущихся теней.

---

## Заключение

Третья лабораторная работа (`lab3`) значительно расширяет функциональность предыдущих, внедряя реалистичные тени с использованием теневых карт и шейдеров. Это позволяет создавать более глубоко проработанные и визуально привлекательные 3D-сцены. 

**Ключевые моменты**:

- **Теневые Карты**: Позволяют создавать реалистичные тени путем записи глубины сцены с точки зрения источника света.
- **Шейдеры**: Обеспечивают гибкость и контроль над процессом рендеринга, позволяя учитывать тени и освещение.
- **Множественные Проходы Рендеринга**: Позволяют разделить процесс рендеринга на Depth Pass и Render Pass для эффективного создания теней.
- **Динамические Тени**: Анимации света позволяют создавать изменяющиеся тени, добавляя реализма сцене.

**Рекомендации для дальнейшего изучения**:

- **Улучшение Качества Теней**: Реализация техник PCF (Percentage Closer Filtering) для смягчения теней.
- **Множественные Источники Света**: Поддержка нескольких источников света и их теней.
- **Каскадные Теневые Карты**: Для улучшения качества теней в различных частях сцены.
- **Использование Шейдеров GLSL**: Переход на более сложные шейдеры для расширения возможностей рендеринга.

Этот гайд предоставляет основы для понимания и дальнейшего развития проекта по теням и теневым картам в OpenGL на Python.