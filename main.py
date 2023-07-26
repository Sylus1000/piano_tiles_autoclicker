from numpy import array
from webbrowser import open
from PIL import ImageGrab
from time import time_ns, sleep
from pyautogui import click, moveTo
from keyboard import is_pressed
from screeninfo import get_monitors
from cv2 import cvtColor, threshold, findContours, arcLength, approxPolyDP, contourArea, boundingRect, COLOR_BGR2GRAY, THRESH_BINARY_INV, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE

MOUSE_CENTER_COORDS = None
GAME_BBOX = None
MONITOR = None

def initializeGame():
    global MONITOR, MOUSE_CENTER_COORDS, GAME_BBOX
    MONITOR = get_monitors()[0]
    MOUSE_CENTER_COORDS = (int(MONITOR.width * 0.411328125), int(MONITOR.height * 0.302777777))
    GAME_BBOX = (int(MONITOR.width * 0.344921875), 
                 int(MONITOR.height * 0.138888888),
                 int(MONITOR.width * 0.4765625),
                 int(MONITOR.height * 0.521527777))
    open("https://www.agame.com/game/magic-piano-tiles")
    sleep(5)
    click(x=MOUSE_CENTER_COORDS[0], y=MOUSE_CENTER_COORDS[1])
    sleep(1)
    click(x=MOUSE_CENTER_COORDS[0], y=MOUSE_CENTER_COORDS[1])
    sleep(3)

def gameLoop(fps: int = 30):
    while True:
        start_time = time_ns()
        if is_pressed("q") or is_pressed("esc"):
            break
        #logic
        ################################################################
        current_frame = ImageGrab.grab(bbox=GAME_BBOX)
        rectangles = findBlackRectangles(current_frame)
        if len(rectangles) > 0:
            for rect in rectangles:
                x,y = rect["x"], rect["y"]
                click(x + GAME_BBOX[0], y + GAME_BBOX[1])
        ################################################################
        elapsed_time_s = (time_ns() - start_time) / 1e+9
        frame_time_s = 1.0 / fps
        remaining_time_s = frame_time_s - elapsed_time_s + 1e-16
        print(f"Frametime: {frame_time_s}, Elapsed: {elapsed_time_s}, Remaining: {remaining_time_s}, FPS: {(1 // elapsed_time_s)}")
        sleep(max(0, remaining_time_s))

def findBlackRectangles(screenshot):
    # Convert the screenshot to a NumPy array
    screenshot_np = array(screenshot)
    
    # Convert the image to grayscale
    gray_image = cvtColor(screenshot_np, COLOR_BGR2GRAY)

    # Apply binary thresholding to convert all non-black pixels to white (255) and black pixels to black (0)
    _, binary_image = threshold(gray_image, 1, 255, THRESH_BINARY_INV)

    # Find contours in the binary image
    contours, _ = findContours(binary_image, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)

    # Filter out rectangles
    min_rectangle_area = 11600 # 80x145px
    black_rectangles = []

    for contour in contours:
        perimeter = arcLength(contour, True)
        approx = approxPolyDP(contour, 0.04 * perimeter, True)

        if len(approx) == 4 and contourArea(contour) > min_rectangle_area: # does the shape have 4 corners (rectangle) and min_area ?
            x, y, w, h = boundingRect(approx)
            center_x = x + w // 2
            center_y = y + h // 2
            black_rectangles.append({"x": center_x, "y": center_y})

    return black_rectangles

if __name__ == "__main__":
    initializeGame()
    gameLoop()