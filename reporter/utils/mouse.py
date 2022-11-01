import mouse
import time

# In seconds
MOUSE_MOVE_SLEEP = 0.01


def on_click(args):
    """Helper method for debugging the mouse position"""

    def print_relative_position():
        """Print relative position (x, y) of the mouse click"""
        mouse_pos = mouse.get_position()
        x = mouse_pos[0] / 2560
        y = mouse_pos[1] / 1440
        print((x, y))

    return print_relative_position


def do_right_click(x, y, args, absolute=True):
    """Perform a right click with appropriate wait times"""
    mouse.move(x, y, absolute=absolute, duration=args.mouse_duration)
    time.sleep(MOUSE_MOVE_SLEEP)
    mouse.right_click()
    time.sleep(args.mouse_wait)


def do_left_click(x, y, args, absolute=True):
    """Perform a left click with appropriate wait times"""
    mouse.move(x, y, absolute=absolute, duration=args.mouse_duration)
    time.sleep(MOUSE_MOVE_SLEEP)
    mouse.click()
    time.sleep(args.mouse_wait)
