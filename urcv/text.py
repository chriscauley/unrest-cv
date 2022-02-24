import cv2

FONT = cv2.FONT_HERSHEY_SIMPLEX
def write(image, text, xy=None, font=FONT, size=0.5, color=(255,255,255)):
  if not xy:
      xy = (5, image.shape[0]-5)
  cv2.putText(image, text, xy, font, size, color)