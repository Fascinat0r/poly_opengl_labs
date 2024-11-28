# particles/emitter.py (продолжение)
# Добавим в emitter.py или отдельный файл, но для простоты оставим здесь
from lab_kr.particles.emitter import Emitter


class ParticleSystem:
    def __init__(self, scene, collision_handler, acceleration=[0.0, -9.81, 0.0]):
        self.emitters = []
        self.collision_handler = collision_handler
        self.acceleration = acceleration  # Общие ускорения, например, гравитация

    def add_emitter(self, emitter: Emitter):
        self.emitters.append(emitter)

    def update(self, delta_time):
        for emitter in self.emitters:
            emitter.update(delta_time, self.acceleration)
            for particle in emitter.particles:
                self.collision_handler.handle_collisions(particle)

    def render(self, shader):
        for emitter in self.emitters:
            emitter.render(shader)
