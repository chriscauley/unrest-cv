import cv2
import random

def wait_key(max_time=60000, default=None):
    delay = 500
    time = 0
    while time < max_time:
        pressed = cv2.waitKey(delay)
        if pressed != -1:
            return chr(pressed)
        time += delay
    return default


def get_scaled_roi(image, scale):
    w = image.shape[1] * scale
    h = image.shape[0] * scale
    name = f'ROI_{random.random()}'
    bounds = cv2.selectROI(name, cv2.resize(image, (w, h)))
    cv2.destroyWindow(name)
    return [int(i/scale) for i in bounds]
