import time
from ui import render_text_on_canvas
from constants import *

def wait_for_start(canvas):
    canvas.create_text(canvas.get_width() / 2, canvas.get_height() / 2, 
                       text="Right-click to Start", 
                       font="Arial", font_size=30, color="white")
    while not canvas.get_new_mouse_clicks():
        canvas.sleep(50)

def show_game_over(canvas, score, high_score):
    canvas.clear()
    canvas.create_text(canvas.get_width() / 2, canvas.get_height() / 2 - 30,
                       text=f"Game Over! Score: {score}",
                       font="Arial", font_size=28, color="red")
    canvas.create_text(canvas.get_width() / 2, canvas.get_height() / 2,
                       text=f"High Score: {high_score}",
                       font="Arial", font_size=24, color="black")
    canvas.create_text(canvas.get_width() / 2, canvas.get_height() / 2 + 30,
                       text="Right-click to Play Again",
                       font="Arial", font_size=20, color="blue")
    while not canvas.get_new_mouse_clicks():
        canvas.sleep(50)

def check_balloon_collision(shape, center_x, canvas_height, balloon_radius):
    shape_center_x = shape['x'] + shape['size'] / 2
    shape_center_y = shape['y'] + shape['size'] / 2
    balloon_center_y = canvas_height - balloon_radius

    dx = shape_center_x - center_x
    dy = shape_center_y - balloon_center_y
    distance_squared = dx * dx + dy * dy

    return distance_squared < (balloon_radius + shape['size'] / 2) ** 2

def move_shape(canvas, shape, speed_multiplier):
    # Apply velocity
    shape['x'] += shape['vx'] * speed_multiplier
    shape['y'] += shape['vy'] * speed_multiplier

    # Optional: apply friction to slow it down gradually
    shape['vx'] *= 0.98
    shape['vy'] *= 0.98

    # Update position on canvas
    canvas.moveto(shape['id'], shape['x'], shape['y'])

