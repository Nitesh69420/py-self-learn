"""
Assignment 1 - Question 1: Interactive Geometric Pattern Studio
Subject: Python Laboratory (DJS23APC203L)
Description: Modular GUI application using easygui and turtle for dynamic geometric art.
"""

import turtle
import sys
import easygui

def draw_square(t: turtle.Turtle, side_length: int, fill_color: str):
    """Draws a filled square centered on canvas."""
    t.penup()
    t.goto(-side_length / 2, -side_length / 2)
    t.setheading(0)
    t.pendown()
    t.fillcolor(fill_color)
    t.begin_fill()
    for _ in range(4):
        t.forward(side_length)
        t.left(90)
    t.end_fill()

def draw_equilateral_triangle(t: turtle.Turtle, side_length: int, fill_color: str):
    """Draws a filled equilateral triangle centered on canvas."""
    t.penup()
    t.goto(-side_length / 2, -side_length / 3)
    t.setheading(0)
    t.pendown()
    t.fillcolor(fill_color)
    t.begin_fill()
    for _ in range(3):
        t.forward(side_length)
        t.left(120)
    t.end_fill()

def draw_concentric_circles(t: turtle.Turtle, max_radius: int, fill_color: str):
    """Draws concentric circles with alternating fill opacity/shades."""
    steps = 3
    radius_step = max_radius / steps
    t.fillcolor(fill_color)
    for i in range(steps, 0, -1):
        r = i * radius_step
        t.penup()
        t.goto(0, -r)
        t.setheading(0)
        t.pendown()
        if i % 2 == 1:
            t.begin_fill()
            t.circle(r)
            t.end_fill()
        else:
            t.circle(r)

def draw_custom_star(t: turtle.Turtle, size: int, fill_color: str):
    """Draws a filled 5-point star centered on canvas."""
    t.penup()
    t.goto(-size / 2, size / 5)
    t.setheading(0)
    t.pendown()
    t.fillcolor(fill_color)
    t.begin_fill()
    for _ in range(5):
        t.forward(size)
        t.right(144)
    t.end_fill()

def main():
    # 1. Shape Selection via easygui.buttonbox
    shape_choices = ["Square", "Equilateral Triangle", "Concentric Circles", "Custom Star"]
    selected_shape = easygui.buttonbox(
        msg="Select a geometric shape to draw:",
        title="Geometric Pattern Studio - Shape Selection",
        choices=shape_choices
    )

    if not selected_shape:
        easygui.msgbox("No shape selected. Exiting application.", title="Cancelled")
        sys.exit()

    # 2. Dimension input via easygui.integerbox (bounded 50 to 250)
    dimension = easygui.integerbox(
        msg=f"Enter size/radius for '{selected_shape}' (between 50 and 250):",
        title="Set Dimensions",
        default=150,
        lowerbound=50,
        upperbound=250
    )

    if dimension is None:
        easygui.msgbox("Operation cancelled by user.", title="Cancelled")
        sys.exit()

    # 3. Fill color input via easygui.enterbox
    fill_color = easygui.enterbox(
        msg="Enter a valid fill color (e.g., 'teal', 'coral', 'deepskyblue', 'crimson'):",
        title="Color Selection",
        default="teal"
    )

    if not fill_color:
        fill_color = "teal"

    # 4. Canvas Initialization via turtle
    screen = turtle.Screen()
    screen.title(f"Pattern Studio: {selected_shape}")
    screen.setup(width=650, height=650)
    screen.bgcolor("#F5F7FA")

    t = turtle.Turtle()
    t.speed(3)
    t.pensize(2)
    t.pencolor("#2D3748")

    # 5. Execute Drawing based on shape selection
    try:
        if selected_shape == "Square":
            draw_square(t, dimension, fill_color)
        elif selected_shape == "Equilateral Triangle":
            draw_equilateral_triangle(t, dimension, fill_color)
        elif selected_shape == "Concentric Circles":
            draw_concentric_circles(t, dimension, fill_color)
        elif selected_shape == "Custom Star":
            draw_custom_star(t, dimension, fill_color)
    except turtle.TurtleGraphicsError:
        easygui.msgbox(f"Invalid color '{fill_color}'. Falling back to default gray.", title="Color Error")
        t.reset()
        draw_square(t, dimension, "gray")

    t.hideturtle()

    # 6. Completion Alert and Safe Window Teardown
    easygui.msgbox(
        msg=f"'{selected_shape}' has been successfully rendered!\nClick OK to close the canvas.",
        title="Rendering Complete"
    )
    turtle.bye()


if __name__ == "__main__":
    main()