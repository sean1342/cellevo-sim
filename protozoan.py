import numpy as np
import pymunk
import brain

class Protozoan:
    def __init__(self, space, objects, pos, size):
        self.color = (255,255,255)
        
        self.pos = pos
        self.size = size
        self.mass = np.pi * (size ** 2)

        self.speed = 50

        # radians
        self.angle = 0

        # inputs: pheromone amount, pheromone gradient x, pheromone gradient y, health, energy, mass, (eyespots r, g, b)
        # outputs: rotation amount, movement amount, reproduction desire
        self.net = brain.NeuralNet(6, 3)

        self.body = pymunk.Body(mass=self.mass, moment=10)
        self.body.position = self.pos

        self.circle = pymunk.Circle(self.body, radius=self.size)
        self.circle.elasticity = 0.6
        self.circle.friction = 0.3
        
        space.add(self.body, self.circle)

        objects.append(self)

    def step(self, inputs):
        actions = self.net.feed_forward(inputs)

        self.body.apply_force_at_local_point((np.cos(self.angle) * self.speed, np.sin(self.angle) * self.speed), (0, 0))