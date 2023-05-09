import numpy as np
import cv2
from tkinter import messagebox

def compute_sk(img):
  hist = cv2.calcHist([img], [0], None, [256], [0, 256])
  h, w = img.shape[:2]
  hist = hist/(h*w)
  
  cdf = np.cumsum(hist)
  s_k = (255 * cdf-0.5).astype("uint8")
  return s_k

def equalize(img):
  s_k = compute_sk(img)
  equalized_img = cv2.LUT(img, s_k)
  return equalized_img

def equalize_cv2_colored(img):
  # equalized_img_cv2 = cv2.equalizeHist(img)
  R, G, B = cv2.split(img)

  output1_R = cv2.equalizeHist(R)
  output1_G = cv2.equalizeHist(G)
  output1_B = cv2.equalizeHist(B)

  equ = cv2.merge((output1_R, output1_G, output1_B))
  return equ

def equalize_cv2_grayscale(img):
  try:
    equ = cv2.equalizeHist(img)
    return equ
  except:
    messagebox.showerror("Error", "Image is not grayscale")
    return img

def adaptive_equalize(img):
  try:
    clahe = cv2.createCLAHE(clipLimit=40, tileGridSize=(8,8))
    clahe_high = clahe.apply(img)
    return clahe_high
  except:
    messagebox.showerror("Error", "Image is not grayscale")
    return img

def is_gray_scale(img):
    w, h = img.size
    for i in range(w):
      for j in range(h):
        r, g, b = img.getpixel((i,j))
        if r != g != b: 
          return False
    return True
