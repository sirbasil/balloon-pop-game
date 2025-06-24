from constants import CANVAS_WIDTH, CANVAS_HEIGHT, BALLOON_RADIUS
print("[ui.py loaded]")

print("UI module loaded.")
def render_text_on_canvas(canvas, x, y, text, color):
    return canvas.create_text(x, y, text=text, font='Arial', font_size=20, color=color)




def draw_background(canvas):
    canvas.create_rectangle(0, 0, canvas.get_width(), canvas.get_height(), 'skyblue')

def draw_balloon(canvas, x, color):
    y = canvas.get_height()
    balloon = canvas.create_oval(
        x - BALLOON_RADIUS,
        y - 2 * BALLOON_RADIUS,
        x + BALLOON_RADIUS,
        y,
        color
    )
    return balloon

def draw_mouse_dot(canvas, x, y):
    return canvas.create_oval(x - 10, y - 10, x + 10, y + 10, 'black')

def wait_for_start(canvas):
    canvas.create_text(canvas.get_width() / 2, canvas.get_height() / 2, 
                       text="Right-click to Start", 
                       font="Arial", font_size=30, color="white")
    
    canvas.wait_for_click()  # This will pause until user clicks



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
    
    canvas.wait_for_click()  # Waits until user clicks again

