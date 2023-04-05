import numpy as np
import pymunk
import brain

class Protozoan:
    def __init__(self, space, actors, pos, size):
        self.color = (255,255,255)

        self.health = 1

        self.pos = pos
        
        self.energy = 1
        self.energy_consumption = 0
        
        self.size = size


        # inputs: health, energy, mass, bias of 1, (eyespots r, g, b)
        # outputs: rotation amount, movement amount, reproduction desire, attack desire
        self.net = brain.NeuralNet(4, 4)
        self.actions = []

        self.body = pymunk.Body(np.pi * self.size ** 2, 100)
        self.body.position = pos

        self.speed = max((-0.04 * (self.size - 10) ** 2 + 7), 1)

        self.circle = pymunk.Circle(self.body, self.size)
        self.circle.elasticity = 0.6
        self.circle.friction = 0.3
        
        space.add(self.body, self.circle)

        actors.append(self)

    def step(self, actors, space, dt, inputs):
        self.energy_consumption = 0
        self.actions = self.net.feed_forward(inputs)
        self.energy_consumption += max(0.0, (1/8 * (self.actions[0] ** 2) + 0.003) * dt/1000 * 1/3)
        self.energy_consumption += max(0.0, (1/8 * (self.actions[1] ** 2) + 0.003) * dt/1000)
        # self.body.angular_velocity += self.actions[0] * self.body.mass * self.speed * 0.000001 * dt
        # self.body.apply_force_at_local_point((0, (self.actions[1]) * self.body.mass * self.speed *  dt), (0, 0))

        self.energy -= self.energy_consumption

        drag_constant = 0.97
        self.body.velocity = pymunk.Vec2d(self.body.velocity.x * drag_constant, self.body.velocity.y * drag_constant)
        self.body.angular_velocity *= 0.8

        self.prev_mass = self.body.mass

        print(self.actions)

        if self.energy < 0:
            self.body.mass += self.energy * 100
            self.energy = 0

        if self.energy > 1:
            self.body.mass += self.energy * 10
            self.energy = 1

        if self.body.mass < 10:
            actors.remove(self)
            space.remove(self.body, self.circle)
            return
        
        if abs(self.prev_mass - self.body.mass) > 10:
            self.size = np.sqrt(self.body.mass / np.pi)
            self.speed = max((-0.04 * (self.size - 10) ** 2 + 7), 1)

            space.remove(self.circle)

            new_circle = pymunk.Circle(self.body, self.size)

            space.add(new_circle)

            self.circle = new_circle

        # if self.actions[2] > 0.5 and self.energy > 0.5:
        #     actors.remove(self)
        #     space.remove(self.body, self.circle)
        #     self.energy -= 0.5
            
        #     p1 = Protozoan(space, actors, self.body.position, self.size * 0.4)
        #     p2 = Protozoan(space, actors, self.body.position, self.size * 0.4)
        #     actors.append(p1)
        #     actors.append(p2)

        #     print("divide")

        self.prev_mass = self.body.mass

class Plant:
    def __init__(self, space, actors, pos, size):
        self.color = (10,255,10)
        self.size = size

        self.body = pymunk.Body(np.pi * self.size ** 2, 10)
        self.body.position = pos

        self.circle = pymunk.Circle(self.body, self.size)
        self.circle.elasticity = 0.6
        self.circle.friction = 0.3

        self.prev_mass = self.body.mass
        
        space.add(self.body, self.circle)

        actors.append(self)
    
    def step(self, actors, space):
        drag_constant = 0.97
        self.body.velocity = pymunk.Vec2d(self.body.velocity.x * drag_constant, self.body.velocity.y * drag_constant)
        self.body.angular_velocity *= 0.8

        self.size = np.sqrt(self.body.mass / np.pi)

        if self.body.mass < 10:
            actors.remove(self)
            space.remove(self.body, self.circle)
            return

        if self.prev_mass != self.body.mass:
            self.size = np.sqrt(self.body.mass / np.pi)
            self.speed = max((-0.04 * (self.size - 10) ** 2 + 7), 1)

            space.remove(self.circle)

            new_circle = pymunk.Circle(self.body, self.size)

            space.add(new_circle)

            self.circle = new_circle

        self.prev_mass = self.body.mass