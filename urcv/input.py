import cv2
import numpy as np
import random

special_keys = {
    65362: 'up',
    65364: 'down',
    65361: 'left',
    65363: 'right',
    7: 'esc',
    32: 'space',
    13: 'enter',
}

def wait_key(max_time=60000, default=None, delay = 500):
    time = 0
    while time < max_time:
        pressed = cv2.waitKeyEx(delay)
        if pressed in special_keys:
            return special_keys[pressed]
        if pressed != -1:
            return chr(pressed)
        time += delay
    return default


def _scale(image, s):
    h, w = image.shape[:2]
    return cv2.resize(image, (w*s, h*s), interpolation=cv2.INTER_NEAREST)


def get_scaled_roi(image, scale, name):
    w0 = int(image.shape[1] * scale)
    h0 = int(image.shape[0] * scale)
    if name is None:
        name = f'ROI_{random.random()}'
    x, y, w, h = cv2.selectROI(name, cv2.resize(image, (w0, h0), interpolation=cv2.INTER_NEAREST))
    cv2.destroyWindow(name)

    # get the rounded coords of the box
    x2 = round((x + w) / scale)
    y2 = round((y + h) / scale)
    x1 = round(x / scale)
    y1 = round(y / scale)

    # return x, y, w, h based off scaled and rounded values
    return [x1, y1, x2-x1, y2-y1]

def get_exact_roi(get_image, name=None, size=100):
    if not callable(get_image):
        # user passed in an actual image (np array)
        get_image = get_image.copy
    while True:
        image = get_image()
        initial_scale = 1
        if image.shape[0] > 1000 or image.shape[1] > 1000:
            initial_scale = 0.75
        coords = np.array(get_scaled_roi(image, initial_scale, name=name))
        if coords is None:
            continue

        confirm_topleft(image, coords, size)
        confirm_botright(image, coords, size)
        return coords.tolist()

def keypress():
    pressed = wait_key()
    if pressed in ['up', 'w']:
        return [0, -1]
    elif pressed in ['down', 's']:
        return [0, 1]
    elif pressed in ['left', 'a']:
        return [-1, 0]
    elif pressed in ['right', 'd']:
        return [1, -0]
    elif pressed in ['q', 'r']:
        return 'delete'


def enforce_bounds(image, coords):
    coords[0] = max(coords[0], 0)
    coords[1] = max(coords[1], 0)
    coords[2] = min(image.shape[1] - coords[0], coords[2])
    coords[3] = min(image.shape[0] - coords[1], coords[3])

def confirm_botright(image, coords, size):
    size = size // 2
    while True:
        enforce_bounds(image, coords)
        x, y, w, h = coords
        x2 = x + w
        y2 = y + h

        botright = image.copy()
        botright = _rect(botright, coords)
        _minx2 = max(x2-size, 0)
        _miny2 = max(y2-size, 0)
        botright = botright[_miny2:_miny2+2*size,_minx2:_minx2+2*size]

        botright = _scale(botright, 4)
        cv2.imshow('Confirm botright', botright)
        delta = keypress()
        if delta is not None:
            coords[2:] += delta
        elif delta is 'delete':
            # set w/h to zero to start over
            coords[2] = coords[3] = 0
        else:
            break
    cv2.destroyWindow('Confirm botright')

def confirm_topleft(image, coords, size):
    size = size // 2
    while True:
        enforce_bounds(image, coords)
        x, y, _, _ = coords
        topleft = image.copy()
        topleft = _rect(topleft, coords)
        _miny1 = max(y - size, 0)
        _minx1 = max(x - size, 0)
        topleft = topleft[_miny1:_miny1+2*size,_minx1:_minx1+2*size]

        topleft = _scale(topleft, 4)
        cv2.imshow('Confirm topleft', topleft)
        delta = keypress()
        if delta is not None:
            coords[:2] += delta
        elif delta is 'delete':
            # set w/h to zero to start over
            coords[2] = coords[3] = 0
        else:
            break
    cv2.destroyWindow('Confirm topleft')

def _rect(image, coords):
    overlay = image.copy()
    x, y, w, h = coords

    cv2.rectangle(overlay, (x, y), (x+w, y+h), (0, 200, 0), -1)  # A filled rectangle

    alpha = 0.4  # Transparency factor.

    # Following line overlays transparent rectangle over the image
    return cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)