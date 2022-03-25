import cv2
import numpy as np


def polygon(image, points, fill=None, stroke=None, interiors=[], bg=None):
    pts = np.array(points, dtype=np.int32)
    pts = pts.reshape((-1,1,2))
    if fill is not None:
        cv2.fillPoly(image, [pts], color=fill)
    if stroke is not None:
        cv2.polylines(image, [pts], True, color=stroke)
    if bg is None:
        bg = tuple([0 for _ in fill])
    for shape in interiors:
        polygon(image, shape, fill=bg, stroke=stroke)


def paste(back, front, x, y):
    """
    Paste front onto back at x, y
    Optimized for non-alpha images
    """
    bh, bw = back.shape[:2]
    fh, fw = front.shape[:2]
    x1, x2 = max(x, 0), min(x+fw, bw)
    y1, y2 = max(y, 0), min(y+fh, bh)

    back[y1:y2, x1:x2] = front


def paste_alpha(back, front, x, y):
    """
    Paste front onto back at x, y while preserving alpha channel
    Will throw error if target is out of bounds for back image
    """
    assert back.shape[2] == 4
    if front.shape[2] == 3:
        front = cv2.cvtColor(back, cv2.COLOR_BGR2BGRA)

    y_buffer = back.shape[0] - front.shape[0] - y
    if y_buffer < 0:
        print('cropping y')
        front = front[:y_buffer]

    x_buffer = back.shape[1] - front.shape[1] - x
    if x_buffer < 0:
        print('cropping x')
        front = front[:,:-x_buffer]

    # crop the overlay from both images
    bh, bw = back.shape[:2]
    fh, fw = front.shape[:2]
    x1, x2 = max(x, 0), min(x+fw, bw)
    y1, y2 = max(y, 0), min(y+fh, bh)
    back_cropped = back[y1:y2, x1:x2]

    alpha_front = front[:,:,3:4] / 255
    alpha_back = back_cropped[:,:,3:4] / 255

    # replace an area in back with overlay
    back[y1:y2, x1:x2, :3] = alpha_front * front[:,:,:3] + (1-alpha_front) * back_cropped[:,:,:3]
    back[y1:y2, x1:x2, 3:4] = (alpha_front + alpha_back) / (1 + alpha_front*alpha_back) * 255
