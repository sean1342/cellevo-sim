import pymunk
import pygame
import numpy as np
import cells

pygame.init()
SIZE = 600, 400
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = 0, 0

actors = []

for i in range(50):
	actors.append(cells.Plant(space, actors, (np.random.random() * SIZE[0], np.random.random() * SIZE[1]), np.random.uniform(5, 10)))

# for i in range(1):
# 	actors.append(cells.Protozoan(space, actors, (np.random.random() * SIZE[0], np.random.random() * SIZE[1]), np.random.uniform(10, 20)))

proto = cells.Protozoan(space, actors, (np.random.random() * SIZE[0], np.random.random() * SIZE[1]), np.random.uniform(10, 20))

def handle_collision(arbiter, space, data):
	for actor1 in actors:
		for actor2 in actors:
			if abs(actor1.body.position - actor2.body.position) <= actor1.circle.radius + actor2.circle.radius:
				if isinstance(actor1, cells.Protozoan) and isinstance(actor2, cells.Plant):
					actor1.energy += 0.001
					actor2.body.mass -= 0.1

				if isinstance(actor1, cells.Plant) and isinstance(actor2, cells.Protozoan):
					actor1.body.mass -= 0.1
					actor2.energy += 0.001
	return True

collision_handler = space.add_collision_handler(0, 0)
collision_handler.begin = handle_collision

tick = 0
running = True
while running:
	tick += 1
	dt = clock.tick_busy_loop(60)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	keys = pygame.key.get_pressed()
	if keys[pygame.K_UP]:
		proto.body.apply_force_at_local_point((0, proto.body.mass * proto.speed *  dt), (0, 0))
		proto.energy_consumption += 0.0863 * dt/1000
	if keys[pygame.K_LEFT]:
		proto.body.angular_velocity -= proto.body.mass * proto.speed * 0.000005 * dt
		proto.energy_consumption += 0.0288 * dt/1000
	if keys[pygame.K_RIGHT]:
		proto.body.angular_velocity += proto.body.mass * proto.speed * 0.000005 * dt
		proto.energy_consumption += 0.0288 * dt/1000
	# if keys[pygame.K_w]:
	# 	if proto.energy > 0.5:
	# 		if proto in actors:
	# 			actors.remove(proto)
	# 			space.remove(proto.body, proto.circle)
	# 			proto.energy -= 0.5

	# 			p1 = cells.Protozoan(space, actors, proto.body.position, proto.size * 0.4)
	# 			p2 = cells.Protozoan(space, actors, proto.body.position, proto.size * 0.4)

	# 			# space.add(p1.body)
	# 			actors.append(p1)
	# 			actors.append(p2)

	# 			print("divide")
	
	screen.fill((100, 100, 100))

	for actor in actors:
		if actor.body in space.bodies:
			if isinstance(actor, cells.Protozoan):
				actor.step(actors, space, dt, [actor.health, actor.energy, actor.body.mass/1000, 1])
				# print(actor.body.mass)
				print(actor.energy)
			else: actor.step(actors, space)

			pygame.draw.circle(screen, actor.color, actor.body.position, actor.size)
			pygame.draw.line(screen, (0, 0, 0), actor.body.position, (actor.body.position[0]+np.cos(actor.body.angle + 1.5708) * actor.size, actor.body.position[1]+np.sin(actor.body.angle + 1.5708) * actor.size), 4)

	# print(proto.energy)
	# print(proto.body.mass)

	pygame.display.update()

	space.step(dt/1000)

	# print(dt)

pygame.quit()