import pygetwindow as gw
from pywinauto.win32functions import MoveWindow
from win32api import GetMonitorInfo, MonitorFromPoint
from win32con import MONITOR_DEFAULTTONEAREST
from win32gui import GetWindowRect


def list_windows():
    windows = gw.getWindowsWithTitle("")
    for i, win in enumerate(windows):
        if win.title != "":
            print(f"{i}: {win.title}")
    return windows


def list_monitors():
    """Displays a list of available monitors"""
    monitors = []
    prev_monitor_area = None

    for x in range(-10000, 10000, 1000):
        try:
            monitor_info = GetMonitorInfo(
                MonitorFromPoint((x, 0), MONITOR_DEFAULTTONEAREST))
            monitor_area = monitor_info["Monitor"]
            if monitor_area != prev_monitor_area:
                monitors.append(monitor_info)
                prev_monitor_area = monitor_area
        except Exception:
            break

    print("Available monitors:")
    for i, monitor in enumerate(monitors):
        monitor_area = monitor['Monitor']
        print(
            f"{i + 1}: Top-left({monitor_area[0]}, {monitor_area[1]}), Bottom-right({monitor_area[2]}, {monitor_area[3]})")

    return monitors


def move_window_to_monitor(window, monitor):
    """Moves the specified window to another monitor"""
    if monitor is None:
        print("No target monitor selected.")
        return

    # Get the current position of the window
    rect = GetWindowRect(window._hWnd)
    window_width = rect[2] - rect[0]
    window_height = rect[3] - rect[1]

    # Calculate the new position
    monitor_area = monitor['Monitor']
    new_left = monitor_area[0]
    new_top = monitor_area[1]
    new_right = new_left + window_width
    new_bottom = new_top + window_height

    # Move the window
    MoveWindow(window._hWnd, new_left, new_top, new_right -
               new_left, new_bottom - new_top, True)
    print("Window has been moved.")


def main():
    print("Currently open windows:")
    windows = list_windows()

    try:
        win_index = int(
            input("Select the number of the window you want to move: "))
        selected_window = windows[win_index]
    except (ValueError, IndexError):
        print("Invalid number entered.")
        return

    print("\nAvailable monitors:")
    monitors = list_monitors()

    try:
        monitor_index = int(
            input("Select the number of the target monitor (1 or higher): "))
        selected_monitor = monitors[monitor_index - 1]
    except (ValueError, IndexError):
        print("Invalid monitor number entered.")
        return

    move_window_to_monitor(selected_window, selected_monitor)


if __name__ == "__main__":
    main()
