from graphics import Canvas
from constants import CANVAS_WIDTH, CANVAS_HEIGHT, BALLOON_RADIUS, BASE_SPEED
from shapes import *
from game_logic import *
from ui import draw_background, draw_balloon, wait_for_start, show_game_over
import time
import random

canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)



def main():
    print("Canvas created:", canvas)

    center_x = CANVAS_WIDTH / 2
    high_score = 0

    while True:
        wait_for_start(canvas)
        draw_background(canvas)
        balloon = draw_balloon(canvas, center_x, random.choice(["red", "blue", "green"]))
        dot = canvas.create_rectangle(0, 0, 60, 15, 'black')  # Our deflecting slab

        shapes = []

        # Create 20 non-overlapping falling shapes
        while len(shapes) < 20:
            new_shape = create_random_shape(canvas)
            if all(not is_overlapping(new_shape, s) for s in shapes):
                shapes.append(new_shape)

        start_time = time.time()
        game_over = False
        prev_mouse_x = canvas.get_mouse_x()
        prev_mouse_y = canvas.get_mouse_y()

        while not game_over:
            elapsed = int(time.time() - start_time)
            speed_multiplier = 1 + (elapsed // 5) * 0.2

            for shape in shapes:
                # Adjust direction towards balloon each frame
                update_velocity_towards_balloon(shape, center_x, CANVAS_HEIGHT - BALLOON_RADIUS)

                move_shape(canvas, shape, speed_multiplier)

            # Check for collisions between shapes and bounce
            for i in range(len(shapes)):
                for j in range(i + 1, len(shapes)):
                    if check_collision(shapes[i], shapes[j]):
                        bounce_on_collision(canvas, shapes[i], shapes[j])

            # Move the player-controlled slab
            mouse_x = canvas.get_mouse_x()
            mouse_y = canvas.get_mouse_y()

            if mouse_x is not None and mouse_y is not None:
                dx = mouse_x - (prev_mouse_x if prev_mouse_x is not None else mouse_x)
                dy = mouse_y - (prev_mouse_y if prev_mouse_y is not None else mouse_y)

                canvas.moveto(dot, mouse_x - 30, mouse_y - 7)
                prev_mouse_x, prev_mouse_y = mouse_x, mouse_y

                # Check slab-shape collisions and apply push
                slab_x, slab_y = canvas.coords(dot)
                slab_x2, slab_y2 = slab_x + 60, slab_y + 15

                for shape in shapes:
                    sx1, sy1 = shape['x'], shape['y']
                    sx2, sy2 = sx1 + shape['size'], sy1 + shape['size']

                    if sx2 >= slab_x and sx1 <= slab_x2 and sy2 >= slab_y and sy1 <= slab_y2:
                        shape['vx'] += dx * 0.2
                        shape['vy'] += dy * 0.2

            # Replace offscreen or stagnant shapes
            new_shapes = []
            for shape in shapes:
                # Check if shape is offscreen
                if (shape['x'] + shape['size'] < 0 or shape['x'] > CANVAS_WIDTH or
                    shape['y'] + shape['size'] < 0 or shape['y'] > CANVAS_HEIGHT):
                    canvas.delete(shape['id'])
                    continue

                # Check if shape is stuck (not moved for 100+ frames)
                last_x, last_y = shape.get('last_pos', (shape['x'], shape['y']))
                if abs(shape['x'] - last_x) < 1 and abs(shape['y'] - last_y) < 1:
                    shape['sleep_count'] = shape.get('sleep_count', 0) + 1
                else:
                    shape['sleep_count'] = 0

                shape['last_pos'] = (shape['x'], shape['y'])

                if shape['sleep_count'] >= 100:
                    canvas.delete(shape['id'])
                    continue

                new_shapes.append(shape)

            # Refill if shapes removed
            while len(new_shapes) < 20:
                new_shape = create_random_shape(canvas)
                if all(not is_overlapping(new_shape, s) for s in new_shapes):
                    new_shapes.append(new_shape)
                else:
                    canvas.delete(new_shape['id'])

            shapes = new_shapes

            # Check balloon collision
            for shape in shapes:
                if check_balloon_collision(shape, center_x, CANVAS_HEIGHT, BALLOON_RADIUS):
                    canvas.create_text(center_x, CANVAS_HEIGHT / 2, text="POP!", font="Arial", font_size=40, color="red")
                    game_over = True

            canvas.sleep(20)

        elapsed = int(time.time() - start_time)
        high_score = max(high_score, elapsed)
        show_game_over(canvas, elapsed, high_score)

if __name__ == '__main__':
    main()
