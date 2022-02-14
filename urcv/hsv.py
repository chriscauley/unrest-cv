import cv2
from collections import OrderedDict
import numpy as np


def filter(hsv, hue=[0,180], saturation=[0, 255], value=[0, 255]):
    lower = np.array([hue[0], saturation[0], value[0]])
    upper = np.array([hue[1], saturation[1], value[1]])
    mask = cv2.inRange(hsv, lower, upper)
    return cv2.bitwise_and(hsv, hsv, mask=mask)


def scan_hue(hsv, n_steps=12, **kwargs):
    s = 180 / n_steps
    ranges = [(int(i*s), int((i+1) * s)) for i in range(n_steps)]
    results = [filter(hsv, hue=r, **kwargs) for r in ranges]
    return results, ranges