import turtle
import math
import cmath

# дерево Пифагора

def _branch(t, order: int, start: complex, length: float, theta_rad: float, angle_rad: float):
    """
    Малює одну гілку довжини length від точки start під кутом theta_rad,
    а потім рекурсивно дві гілки від її вершини: +angle та -angle.
    """
    # куди тягнемо поточну гілку
    vec = cmath.rect(length, theta_rad)  # length * e^{i*theta}
    end = start + vec

    # власне сегмент
    t.penup(); t.goto(start.real, start.imag); t.pendown()
    t.goto(end.real, end.imag)

    if order == 0:
        return

    # масштаби дочірніх гілок: L·cos(angle), L·sin(angle)
    l_left  = length * math.cos(angle_rad)
    l_right = length * math.sin(angle_rad)

    # напрями дочірніх гілок
    _branch(t, order - 1, end, l_left,  theta_rad + angle_rad, angle_rad)
    _branch(t, order - 1, end, l_right, theta_rad - angle_rad, angle_rad)


def draw_pythagoras_tree_naked(
    order: int,
    size: float = 10,                # довжина стовбура
    angle_deg: float = 45,            # кут розгалуження
    pen_width: int = 2,
    line_color: str = "#8B2E2E",
    bg_color: str = "white",
):
    screen = turtle.Screen()
    screen.bgcolor(bg_color)

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.pensize(pen_width)
    t.color(line_color)

    turtle.tracer(0, 0)  # швидкий рендер

    # ставимо стовбур по центру знизу і малюємо вгору
    y0 = -screen.window_height() / 2 + 20 
    start = complex(0.0, y0)
    theta0 = math.pi / 2               # вертикально вгору
    angle_rad = math.radians(angle_deg)

    _branch(t, order, start, size, theta0, angle_rad)

    turtle.update()
    turtle.done()


# демонстрація
try:
    order = int(input("Вкажіть рівень рекурсії (ціле число ≥ 0): ").strip())
    if order < 0:
        raise ValueError
except ValueError:
    print("Помилка: рівень рекурсії має бути цілим числом ≥ 0.")
else:
    draw_pythagoras_tree_naked(order=order, size=300, angle_deg=45, pen_width=2)
