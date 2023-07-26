from webbrowser import open
from PIL import ImageGrab, Image
from time import time_ns, sleep
from pyautogui import click
from keyboard import is_pressed
from screeninfo import get_monitors

MOUSE_CENTER_COORDS = []
GAME_BBOX = []
MONITOR = None

def initializeGame():
    MONITOR = get_monitors()[0]
    MOUSE_CENTER_COORDS = [int(MONITOR.width * 0.411328125), int(MONITOR.height * 0.302777777)]
    GAME_AREA = [int(MONITOR.width * 0.344921875), 
                 int(MONITOR.height * 0.105555555),
                 int(MONITOR.width * 0.4765625),
                 int(MONITOR.height * 0.521527777)]
    open("https://www.jetztspielen.de/spiel/magische-klaviertasten")
    sleep(3)
    click(x=MOUSE_CENTER_COORDS[0], y=MOUSE_CENTER_COORDS[1])
    sleep(1)
    click(x=MOUSE_CENTER_COORDS[0], y=MOUSE_CENTER_COORDS[1])
    sleep(3)

def analyzeFrame(frame: Image):
    return None

def gameLoop(fps: int = 30):
    while True:
        start_time = time_ns()
        if is_pressed("q") or is_pressed("esc"):
            break
        #logic
        ################################################################
        current_frame = ImageGrab.grab(bbox=())
        ################################################################
        elapsed_time_s = (time_ns() - start_time) / 1e+9
        frame_time_s = 1.0 / fps
        remaining_time_s = frame_time_s - elapsed_time_s + 1e-16
        print(f"Frametime: {frame_time_s}, Elapsed: {elapsed_time_s}, Remaining: {remaining_time_s}, FPS: {(1 // remaining_time_s)}")
        sleep(max(0, remaining_time_s))

if __name__ == "__main__":
    initializeGame()
    #gameLoop()