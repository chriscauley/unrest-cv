import cv2
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


def get_scaled_roi(image, scale):
    w0 = image.shape[1] * scale
    h0 = image.shape[0] * scale
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

def get_exact_roi(image):
    _image = image.copy()
    x0, y0, w0, h0 = get_scaled_roi(image, 1)
    _miny1 = max(y0-50, 0)
    _minx1 = max(x0-50, 0)
    topleft = _image[_miny1:y0+50,_minx1:x0+50]
    x1, y1, _, _ = get_scaled_roi(topleft, 10)

    x1 += _minx1
    y1 += _miny1

    x2 = x0 + w0
    y2 = y0 + h0
    _minx2 = x2-50
    _miny2 = y2-50
    bottomright = _image[_miny2:y2+50,_minx2:x2+50]
    x2, y2, w2, h2 = get_scaled_roi(bottomright, 20)

    x2 += _minx2 + w2
    y2 += _miny2 + h2

    return [x1, y1, x2 - x1, y2 - y1]
