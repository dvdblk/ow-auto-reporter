import keyboard
import mouse
import argparse
import time
import random
from win32gui import FindWindow, GetWindowRect, GetForegroundWindow

from reporter.utils import load_reasons
from reporter.utils.img import get_reason_index_from_img, take_screenshot
from reporter.utils.mouse import do_right_click, do_left_click

# In seconds
MENU_OPEN_SLEEP = 0.1


def report_hover(width, height, reasons: dict, args):
    """
    Reports hovered player once.
    """
    player_x, player_y = mouse.get_position()

    # Report hovered player
    for i in range(args.iterations):
        print(f"\tReporting hover #{i}")
        for reason, msgs in reasons.items():
            reason_normalized = reason.replace("_", " ").upper()
            if msgs:
                reason_msg = random.choice(msgs)
            else:
                reason_msg = ""

            single_report(
                player_x, player_y, width, height, reason_normalized, reason_msg, args
            )


def single_report(x, y, width, height, reason, reason_msg, args):
    """Attempt to report a player at x and y"""
    # Right click player menu on a hovered player tag
    do_right_click(x, y, args)

    # Click report button
    # The relative height accounts for players with a title
    do_left_click(width * 0.0774, height * 0.337, args, absolute=False)
    time.sleep(MENU_OPEN_SLEEP)

    # move to center
    do_left_click(width * 0.4847, height * 0.4409, args)
    mouse.move(5, 5, absolute=False, duration=args.mouse_duration)
    time.sleep(MENU_OPEN_SLEEP)

    # Choose report category
    # Find the appropriate reason bounding box
    report_category_img = take_screenshot(
        bbox=(width * 0.3175, height * 0.4618, width * 0.6824, height * 0.6687)
    )
    reason_idx = get_reason_index_from_img(
        reason, report_category_img, tesseract_path=args.tesseract_path
    ) or 0
    # Click on the correct category
    do_left_click(width * 0.4894, height * (0.481 + reason_idx * 0.033), args)

    # Continue
    # must be based on the reason because the continue buttons Y pos differs
    continue_y = {
        "GAMEPLAY SABOTAGE": 0.7215,
        "BAD BATTLETAG": 0.6916,
        "CHEATING": 0.7,
        "SPAM": 0.7097,
        "ABUSIVE CHAT": 0.7118,
        "INACTIVITY": 0.6888,
    }
    do_left_click(width * 0.537, height * continue_y[reason], args)

    # Write reason
    if reason_msg:
        keyboard.write(reason_msg)
        time.sleep(args.mouse_wait)

    # Send report
    do_left_click(width * 0.538, height * 0.7048, args)

    # OK
    do_left_click(width * 0.491, height * 0.602, args)


def wait_for_hotkey(args):
    """Wait for report hotkey indefinitely and report the player"""

    reasons = load_reasons(args)

    while True:
        # Wait for report signal
        print("Waiting for report hotkey...")
        keyboard.wait(args.report_hotkey)
        print("\tReporting")

        ow_window = FindWindow(None, "Overwatch")
        fg_window = GetForegroundWindow()
        if fg_window != ow_window:
            print("Overwatch is not in the foreground. Skipping report...")
            continue

        # Get window size
        window_rect = GetWindowRect(ow_window)
        if (
            window_rect[0] + window_rect[1] != 0
            or window_rect[2] < 0
            or window_rect[3] < 0
        ):
            print(f"Wrong Overwatch window size {window_rect}. Skipping report...")
            continue

        # Report
        report_hover(window_rect[2], window_rect[3], reasons, args)
        print("\tDone reporting.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto report for Overwatch.")
    parser.add_argument(
        "--report-hotkey",
        default="ctrl+shift+R",
        help="The key combination that starts reporting",
    )
    parser.add_argument(
        "--mouse-duration",
        default=0.04,
        help="The duration of mouse movement animations",
    )
    parser.add_argument(
        "--mouse-wait",
        default=0.1,
        help="The wait time between mouseclicks. Should be higher than 0.08",
    )
    parser.add_argument(
        "--iterations",
        default=1,
        help="Number of iterations of reports. Defaults to 1.",
    )
    parser.add_argument(
        "--reasons-fp",
        default="etc/reasons.json",
        help="The filepath to a json containing report reasons",
    )
    parser.add_argument(
        "--tesseract-path",
        default="C:\Program Files\Tesseract-OCR\\tesseract.exe",
        help="The path to tesseeract.exe"
    )

    args = parser.parse_args()

    try:
        wait_for_hotkey(args)
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting...")
