# Гайд по первой лабораторной работе по графике

## Введение

Проект представляет собой реализацию сцены с 3D-объектами и анимациями на языке Python с использованием библиотеки OpenGL. Основная цель проекта — демонстрация основ работы с OpenGL, включая создание геометрических фигур, управление камерой и анимацию.

Этот гайд содержит подробное объяснение структуры проекта, ключевых компонентов и их взаимодействий.

---

## Структура проекта

Проект организован в следующей структуре:

```
lab1/
├── animations/           # Анимации для объектов сцены
│   ├── animation.py
│   ├── looped_movement_animation.py
│   ├── looped_rotation_animation.py
│   ├── looped_scale_animation.py
├── shapes/               # 3D-объекты (фигуры)
│   ├── cone.py
│   ├── cube.py
│   ├── cylinder.py
│   ├── octahedron.py
│   ├── shape.py          # Базовый класс для фигур
│   ├── sphere.py
│   ├── teapot.py
│   ├── torus.py
├── camera.py             # Камера для работы со сценой
├── handlers.py           # Обработчики ввода (клавиатура, мышь)
├── scene.py              # Сцена с объектами и анимациями
└── lab1_main.py          # Главный файл проекта
```

---

## План объяснения

1. **Основные концепции OpenGL в проекте**
2. **Работа с базовыми фигурами**
3. **Камера: перемещение и вращение**
4. **Анимации: перемещение, вращение, масштабирование**
5. **Обработчики ввода: клавиатура и мышь**
6. **Сцена и рендеринг**
7. **Итог: как всё работает вместе**

---

## 1. Основные концепции OpenGL в проекте

OpenGL — это библиотека для рендеринга графики. В этом проекте используются её базовые функции:

- **glBegin/glEnd**: Описывают, какие примитивы будут рендериться (например, `GL_TRIANGLES`, `GL_QUADS`, и т.д.).
- **glVertex3f**: Определяет координаты вершины.
- **glColor3f**: Устанавливает цвет вершины.
- **glTranslatef, glRotatef, glScalef**: Операции трансформации (перемещение, вращение, масштабирование).
- **glPushMatrix/glPopMatrix**: Сохраняют/восстанавливают текущую матрицу трансформации.
- **gluLookAt**: Используется для установки камеры.

Эти функции образуют основу для создания и управления 3D-объектами.

---

## 2. Работа с базовыми фигурами

Каждая 3D-фигура реализована как отдельный класс. Все фигуры наследуются от базового класса `Shape`.

### Базовый класс `Shape`

Класс `Shape` описывает свойства, общие для всех фигур:

- **Атрибуты:**
  - `position`: Позиция фигуры.
  - `scale`: Масштаб.
  - `color`: Цвет.
  - `rotation`: Углы вращения.

- **Методы:**
  - `draw`: Отрисовка фигуры.
  - `draw_edges`: Отрисовка рёбер фигуры.
  - `render`: Применение трансформаций (позиция, вращение, масштаб) перед отрисовкой.

Пример базового метода `render`:

```python
def render(self):
    glPushMatrix()
    glTranslatef(*self.position)
    glRotatef(self.rotation[0], 1.0, 0.0, 0.0)
    glRotatef(self.rotation[1], 0.0, 1.0, 0.0)
    glRotatef(self.rotation[2], 0.0, 0.0, 1.0)
    glScalef(self.scale, self.scale, self.scale)
    self.draw()
    self.draw_edges()
    glPopMatrix()
```

### Примеры фигур

- **Конус** (`Cone`): Реализован через боковые треугольники и нижнее основание с помощью `GL_TRIANGLES` и `GL_TRIANGLE_FAN`.
- **Цилиндр** (`Cylinder`): Состоит из боковой поверхности и двух оснований.
- **Сфера** (`Sphere`): Использует полярные координаты для генерации точек.

---

## 3. Камера: перемещение и вращение

Класс `Camera` управляет положением и ориентацией камеры в сцене.

- **Атрибуты:**
  - `position`: Позиция камеры.
  - `front`: Направление взгляда.
  - `right`, `up`: Ориентация камеры.
  - `yaw`, `pitch`: Углы вращения.

- **Методы:**
  - `move_forward`, `move_backward`, `move_left`, `move_right`: Движение камеры.
  - `rotate`: Вращение камеры при движении мыши.
  - `get_view_matrix`: Возвращает параметры для `gluLookAt`.

### Код вращения камеры:

```python
def rotate(self, x_offset, y_offset):
    self.yaw += x_offset * self.sensitivity
    self.pitch += y_offset * self.sensitivity
    self.pitch = max(min(self.pitch, 89.0), -89.0)  # Ограничиваем наклон
    self.update_camera_vectors()
```

---

## 4. Анимации: перемещение, вращение, масштабирование

Все анимации наследуются от абстрактного класса `Animation`. Анимация обновляет параметры фигуры (позицию, угол, масштаб) в зависимости от времени (`delta_time`).

### Пример анимации перемещения (`LoopedMovementAnimation`):

- **Логика:**
  - Объект движется между `start_position` и `end_position`.
  - После достижения одной из позиций движение меняет направление.

### Пример обновления:

```python
def update(self, shape, delta_time):
    for i in range(3):
        direction = self.directions[i] if self.moving_forward else -self.directions[i]
        self.current_position[i] += direction * self.speeds[i] * delta_time
        shape.position = self.current_position
```

---

## 5. Обработчики ввода: клавиатура и мышь

Класс `handlers.py` отвечает за ввод пользователя.

- **Клавиатура**:
  - Словарь `keys` отслеживает состояния клавиш (`True`, если нажата).
  - Методы `key_pressed` и `key_released` обновляют состояния.

- **Мышь**:
  - Замыкание `create_mouse_movement_handler` обрабатывает движение мыши и обновляет ориентацию камеры.

---

## 6. Сцена и рендеринг

Класс `Scene` управляет объектами и анимациями.

- **Атрибуты:**
  - `objects`: Список объектов в сцене.
  - `animations`: Список анимаций.

- **Методы:**
  - `add_object`: Добавляет объект в сцену.
  - `add_animation`: Добавляет анимацию.
  - `update_animations`: Обновляет анимации.
  - `render`: Отрисовывает оси, сетку и объекты.

---

## 7. Итог: как всё работает вместе

1. **Инициализация:**
   - Устанавливаются параметры OpenGL (`glEnable(GL_DEPTH_TEST)` и др.).
   - Создаются объекты (`Cube`, `Cone`, `Sphere`).
   - Добавляются анимации (`LoopedRotationAnimation` и др.).

2. **Рендеринг:**
   - Камера устанавливается с помощью `gluLookAt`.
   - Вызывается метод `scene.render()` для отрисовки объектов.

3. **Обновление:**
   - Анимации обновляются в методе `scene.update_animations()`.

---

## Заключение

Этот проект демонстрирует основы работы с 3D-графикой в OpenGL, включая создание фигур, управление камерой, реализацию анимаций и взаимодействие с пользователем. 

Для дальнейшего изучения рекомендуется:
- Исследовать методы улучшения производительности (VAO/VBO, шейдеры).
- Добавить освещение и текстурирование.