import cv2

def erode(img):
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
  return cv2.erode(img, kernel, iterations=2)

def dilate(img):
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
  return cv2.dilate(img, kernel, iterations=2)

def opening(img):
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
  return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

def closing(img):
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
  return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)