import pymunk

def step(space, bodies):
    for body in bodies:
        drag_constant = 0.0002

        pointing_direction = pymunk.Vec2d(1,0).rotated(body.angle)
        flight_direction = pymunk.Vec2d(body.velocity)
        flight_speed = flight_direction.normalize_return_length()
        dot = flight_direction.dot(pointing_direction)
        # (1-abs(dot)) can be replaced with (1-dot) to make arrows turn 
        # around even when fired straight up. Might not be as accurate, but 
        # maybe look better.
        drag_force_magnitude = (1-abs(dot)) * flight_speed **2 * drag_constant * body.mass
        arrow_tail_position = pymunk.Vec2d(-50, 0).rotated(body.angle)
        body.apply_impulse_at_world_point(drag_force_magnitude * -flight_direction, arrow_tail_position)

        body.angular_velocity *= 0.5
    
    space.step(0.001)