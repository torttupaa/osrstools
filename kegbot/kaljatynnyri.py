import cv2
import numpy as np
from PIL import ImageGrab
import time
from pynput.mouse import Button, Controller




mouse = Controller()

fourdose_pot = cv2.imread('fourdose.jpg',0)
full_energy = cv2.imread('100energy.jpg',0)
#barrelmatafaka


w, h = fourdose_pot.shape[::-1]
w2, h2 = full_energy.shape[::-1]

edellinen_countti = 1
pankitus = False
kanto = False
klikattu_puuta = False

four_doselist = []

while True:
    img_rgb = ImageGrab.grab(bbox=(0,0,800,800))
    img_np = np.array(img_rgb)
    frame_gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

    fourdose_matsi = cv2.matchTemplate(frame_gray,fourdose_pot,cv2.TM_CCOEFF_NORMED)
    energy_matsi = cv2.matchTemplate(frame_gray, full_energy, cv2.TM_CCOEFF_NORMED)

    threshold = 0.8

    fourdose_check = np.where( fourdose_matsi >= threshold)
    for pt in zip(*fourdose_check[::-1]):
        cv2.rectangle(img_np, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        four_doselist.append(pt)

    #try:
        #print(four_doselist[0])
        #mouse.position = four_doselist[0]
    #except:
        #pass
    if len(four_doselist) == 0:
        quit()
    four_doselist = []
    #time.sleep(2)

    no_energy = True
    energia_check = np.where(energy_matsi >= 0.9)
    for pt in zip(*energia_check[::-1]):
        no_energy = False
        cv2.rectangle(img_np, pt, (pt[0] + w2, pt[1] + h2), (0, 0, 255), 2)

    if no_energy:
        print("ei energiaa")


    cv2.imshow("frame", img_np)
    cv2.waitKey(1)