# particles/emitter.py (продолжение)
import math
import random

import glm

from lab_kr.particles.emitter import Emitter
from lab_kr.particles.particle import Particle


class ConeEmitter(Emitter):
    def __init__(self, position, emission_rate, max_particles, speed_range, size_range, color, lifetime):
        super().__init__(position, emission_rate, max_particles)
        self.speed_range = speed_range
        self.size_range = size_range
        self.color = color
        self.lifetime = lifetime

    def emit_particle(self):
        # Начальная скорость: по нормали к конусу с вариацией направления
        angle = random.uniform(-math.pi / 8, math.pi / 8)
        direction = glm.vec3(
            math.cos(angle),
            math.sin(angle),
            random.uniform(-0.1, 0.1)
        )
        velocity = glm.normalize(direction) * random.uniform(self.speed_range[0], self.speed_range[1])
        size = random.uniform(self.size_range[0], self.size_range[1])
        return Particle(
            position=self.position,
            velocity=velocity,
            size=size,
            color=self.color,
            lifetime=self.lifetime,
            has_trail=False  # След необязателен
        )
