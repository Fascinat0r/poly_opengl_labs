from typing import List

from lab_kr.materials.shader import Shader
from lab_kr.particles.anti_attractor import AntiAttractorHandler
from lab_kr.particles.emitter import Emitter


class ParticleSystem:
    def __init__(self, anti_attractor_handler: AntiAttractorHandler, acceleration=None):
        if acceleration is None:
            acceleration = [0.0, -9.81, 0.0]
        self.emitters: List[Emitter] = []
        self.anti_attractor_handler = anti_attractor_handler
        self.acceleration = acceleration  # Общие ускорения, например, гравитация

    def add_emitter(self, emitter: Emitter):
        self.emitters.append(emitter)

    def update(self, delta_time):
        for emitter in self.emitters:
            emitter.update(delta_time)
            for particle in emitter.particles:
                self.anti_attractor_handler.apply_anti_attraction(particle)

    def render(self, shader: Shader):
        shader.set_bool('useParticleColor', True)
        for emitter in self.emitters:
            emitter.render(shader)
        shader.set_bool('useParticleColor', False)
