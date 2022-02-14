import cv2


def scale(image, scale):
    w = int(image.shape[1] * scale)
    h = int(image.shape[0] * scale)
    return cv2.resize(image, (w, h))


def crop(image, bounds):
    x, y, w, h = bounds
    return image[y:y+h,x:x+w]


def crop_ratio(image, bounds):
    ih, iw = image.shape[:2]
    x, y, w, h = bounds
    x = int(x * iw)
    w = int(w * iw)
    y = int(y * ih)
    h = int(h * ih)
    return crop(image, (x, y, w, h))


def threshold(image, value, max_value=255, type=cv2.THRESH_BINARY_INV):
    gray = image
    if len(image.shape) == 3:
        gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, value, max_value, type)
    return cv2.bitwise_and(image, image, mask=mask)