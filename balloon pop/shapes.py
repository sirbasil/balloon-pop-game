import random
from constants import CANVAS_WIDTH, CANVAS_HEIGHT

def create_random_shape(canvas):
	size = random.randint(20, 40)
	x = random.randint(0, CANVAS_WIDTH - size)
	y = random.randint(0, int(CANVAS_HEIGHT * 0.4))  # limit spawn height to upper 40%

	shape = {
		'x': x,
		'y': y,
		'size': size,
		'vx': random.uniform(-2, 2),       # random horizontal speed
		'vy': random.uniform(1.5, 3.0),     # falling speed to keep blocks moving
		'id': canvas.create_oval(x, y, x + size, y + size, random.choice(['red', 'blue', 'green']))
	}
	return shape




def check_collision(shape1, shape2):
    x1, y1, s1 = shape1['x'], shape1['y'], shape1['size']
    x2, y2, s2 = shape2['x'], shape2['y'], shape2['size']
    return (
        x1 < x2 + s2 and x1 + s1 > x2 and
        y1 < y2 + s2 and y1 + s1 > y2
    )

def bounce_on_collision(canvas, shape1, shape2):
    shape1['vx'], shape2['vx'] = -shape1['vx'], -shape2['vx']
    shape1['vy'], shape2['vy'] = -shape1['vy'], -shape2['vy']

    shape1['x'] += shape1['vx'] * 2
    shape1['y'] += shape1['vy'] * 2
    shape2['x'] += shape2['vx'] * 2
    shape2['y'] += shape2['vy'] * 2

    canvas.moveto(shape1['id'], shape1['x'], shape1['y'])
    canvas.moveto(shape2['id'], shape2['x'], shape2['y'])

def is_overlapping(shape1, shape2):
	return not (
		shape1['x'] + shape1['size'] < shape2['x'] or
		shape1['x'] > shape2['x'] + shape2['size'] or
		shape1['y'] + shape1['size'] < shape2['y'] or
		shape1['y'] > shape2['y'] + shape2['size']
	)



def update_velocity_towards_balloon(shape, balloon_x, balloon_y, intensity=0.02):
    # Calculate direction vector towards balloon center
    dx = balloon_x - (shape['x'] + shape['size'] / 2)
    dy = balloon_y - (shape['y'] + shape['size'] / 2)

    distance = max((dx**2 + dy**2) ** 0.5, 1)  # Avoid division by 0
    shape['vx'] += (dx / distance) * intensity
    shape['vy'] += (dy / distance) * intensity



