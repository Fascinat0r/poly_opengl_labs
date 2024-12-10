from typing import List

from lab_kr.materials.shader import Shader
from lab_kr.particles.collision import CollisionHandler
from lab_kr.particles.emitter import Emitter


class ParticleSystem:
    def __init__(self, collision_handler: CollisionHandler):
        self.emitters: List[Emitter] = []
        self.collision_handler = collision_handler

    def add_emitter(self, emitter: Emitter):
        self.emitters.append(emitter)

    def update(self, delta_time):
        for emitter in self.emitters:
            emitter.update(delta_time)
            for particle in emitter.particles:
                self.collision_handler.handle_collisions(particle)

    def render(self, shader: Shader):
        shader.set_bool("useParticleColor", True)
        for emitter in self.emitters:
            emitter.render(shader)
        shader.set_bool("useParticleColor", False)
