import turtle
import math
import cmath

# --- Налаштування графіка ---
LINE_COLOR = "#8B2E2E"   # колір ліній (hex)
BG_COLOR   = "white"     # колір фону
ANGLE_DEG  = 45.0        # кут розгалуження
SIZE       = 200.0       # довжина стовбура
PEN_WIDTH  = 2           # товщина ліній

def _branch(t, order: int, start: complex, length: float, theta_rad: float, angle_rad: float):
    """
    Малює одну гілку довжини length від точки start під кутом theta_rad,
    а потім рекурсивно дві гілки від її вершини: +angle та -angle.
    """

    vec = cmath.rect(length, theta_rad)  
    end = start + vec

    # сегмент
    t.penup(); t.goto(start.real, start.imag); t.pendown()
    t.goto(end.real, end.imag)

    if order == 0:
        return

    # довжини дочірніх гілок
    l_left  = length * math.cos(angle_rad)
    l_right = length * math.sin(angle_rad)

    # рекурсія: вліво і вправо
    _branch(t, order - 1, end, l_left,  theta_rad + angle_rad, angle_rad)
    _branch(t, order - 1, end, l_right, theta_rad - angle_rad, angle_rad)

def draw_pythagoras_tree(order: int):
    if order < 0:
        raise ValueError("Рівень рекурсії має бути цілим числом ≥ 0.")

    screen = turtle.Screen()
    screen.bgcolor(BG_COLOR)

    t = turtle.Turtle(visible=False)
    t.speed(0)
    t.pensize(PEN_WIDTH)
    t.pencolor(LINE_COLOR)

    # прискорений рендер (без анімації)
    turtle.tracer(0, 0)

    y0 = -screen.window_height() / 2 + 20
    start = complex(0.0, y0)
    theta0 = math.pi / 2                # 90 градусів вгору
    angle_rad = math.radians(ANGLE_DEG)

    _branch(t, order, start, SIZE, theta0, angle_rad)

    turtle.update()
    turtle.done()

def main():
    try:
        order = int(input("Вкажіть рівень рекурсії (ціле число ≥ 0): ").strip())
        if order < 0:
            raise ValueError
    except ValueError:
        print("Помилка: рівень рекурсії має бути цілим числом ≥ 0.")
        return

    draw_pythagoras_tree(order)

if __name__ == "__main__":
    main()
