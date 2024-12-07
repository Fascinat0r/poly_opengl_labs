# particles/emitter.py
from abc import ABC, abstractmethod

import glm

from lab_kr.materials.shader import Shader


class Emitter(ABC):
    def __init__(self, position, emission_rate, max_particles):
        self.position = glm.vec3(*position)
        self.emission_rate = emission_rate  # Частота эмиссии (частиц в секунду)
        self.max_particles = max_particles
        self.particles = []
        self.accumulator = 0.0  # Накопитель времени

    @abstractmethod
    def emit_particle(self):
        pass

    def update(self, delta_time, acceleration):
        # Эмиссия новых частиц
        self.accumulator += self.emission_rate * delta_time
        particles_to_emit = int(self.accumulator)

        for _ in range(particles_to_emit):
            if len(self.particles) < self.max_particles:
                self.particles.append(self.emit_particle())

        self.accumulator -= particles_to_emit

        # Обновление существующих частиц
        alive_particles = []
        for particle in self.particles:
            particle.update(delta_time, acceleration)
            if particle.is_alive():
                alive_particles.append(particle)
        self.particles = alive_particles

    def render(self, shader: Shader):
        for particle in self.particles:
            particle.render(shader)
