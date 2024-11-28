# particles/emitter.py (продолжение)
import random

import glm

from lab_kr.particles.emitter import Emitter
from lab_kr.particles.particle import Particle


class PointEmitter(Emitter):
    def __init__(self, position, emission_rate, max_particles, speed_range, size_range, color, lifetime):
        super().__init__(position, emission_rate, max_particles)
        self.speed_range = speed_range  # (min_speed, max_speed)
        self.size_range = size_range  # (min_size, max_size)
        self.color = color
        self.lifetime = lifetime

    def emit_particle(self):
        # Начальная скорость с уменьшением по мере удаления (обязательный параметр)
        speed = random.uniform(self.speed_range[0], self.speed_range[1])
        direction = glm.vec3(
            random.uniform(-0.1, 0.1),
            random.uniform(0.5, 1.0),
            random.uniform(-0.1, 0.1)
        )
        velocity = glm.normalize(direction) * speed
        size = random.uniform(self.size_range[0], self.size_range[1])
        return Particle(
            position=self.position,
            velocity=velocity,
            size=size,
            color=self.color,
            lifetime=self.lifetime,
            has_trail=True
        )
