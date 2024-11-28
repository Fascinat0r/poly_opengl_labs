# particles/emitter.py
from abc import ABC, abstractmethod

import glm


class Emitter(ABC):
    def __init__(self, position, emission_rate, max_particles):
        self.position = glm.vec3(*position)
        self.emission_rate = emission_rate  # Частота эмиссии (частиц в секунду)
        self.max_particles = max_particles
        self.particles = []

    @abstractmethod
    def emit_particle(self):
        pass

    def update(self, delta_time, acceleration):
        # Эмиссия новых частиц
        particles_to_emit = int(self.emission_rate * delta_time)
        for _ in range(particles_to_emit):
            if len(self.particles) < self.max_particles:
                self.particles.append(self.emit_particle())

        # Обновление существующих частиц
        alive_particles = []
        for particle in self.particles:
            particle.update(delta_time, acceleration)
            if particle.is_alive():
                alive_particles.append(particle)
        self.particles = alive_particles

    def render(self, shader):
        for particle in self.particles:
            particle.render(shader)
