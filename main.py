import pymunk
import pygame
import protozoan
import numpy as np

pygame.init()
SIZE = 600, 400
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = 0, 0

objects = []

proto = protozoan.Protozoan(space, objects, (300, 0), 30)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
            proto.body.apply_force_at_local_point((np.cos(proto.angle) * 50 * 1000 * dt, np.sin(proto.angle) * 50 * 1000 * dt), (0, 0))
    if keys[pygame.K_LEFT]:
            proto.angle -= 0.001 * dt
    if keys[pygame.K_RIGHT]:
          proto.angle += 0.001 * dt
    proto.pos = proto.body.position
    print(proto.angle * 180/np.pi)

    screen.fill((100, 100, 100))

    for object in objects:
          pygame.draw.circle(surface=screen, color=object.color, center=object.pos, radius=object.size)

    pygame.display.update()
    dt = clock.tick(60)
    space.step(dt / 1000)

pygame.quit()
