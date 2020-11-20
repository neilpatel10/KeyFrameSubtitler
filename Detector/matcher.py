import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


img = cv.imread('aslA.jpg', 0)
img2 = img.copy()
templateA = cv.imread('tempA.jpg', 0)
templateB = cv.imread('tempB.jpg', 0)
templateC = cv.imread('tempC.jpg', 0)
templateD = cv.imread('tempD.jpg', 0)

newImg = cv.matchTemplate(img, templateA, 'cv.TM_CCOEFF')
minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(newImg)


