import cv2
import numpy as np
from PIL import ImageGrab
import time
from pynput.mouse import Button, Controller




mouse = Controller()

template1 = cv2.imread('kanto.jpg',0)
template2 = cv2.imread('logs.jpg',0)

w, h = template1.shape[::-1]
w2, h2 = template2.shape[::-1]

edellinen_countti = 1
pankitus = False
kanto = False
klikattu_puuta = False

while True:
    img_rgb = ImageGrab.grab(bbox=(0,0,800,800))
    img_np = np.array(img_rgb)
    frame_gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

    res1 = cv2.matchTemplate(frame_gray,template1,cv2.TM_CCOEFF_NORMED)
    res2 = cv2.matchTemplate(frame_gray, template2, cv2.TM_CCOEFF_NORMED)

    threshold = 0.8

    loc = np.where( res1 >= threshold)
    for pt in zip(*loc[::-1]):
        kanto = True
        klikattu_puuta = False
        cv2.rectangle(img_np, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

    if kanto==False and klikattu_puuta==False:
        print("klikkaa puuta")
        mouse.position = (500, 400)
        time.sleep(0.1)
        mouse.click(Button.left, 1)
        klikattu_puuta = True
    kanto = False


    log_counter = 0
    loc2 = np.where(res2 >= threshold)
    for pt in zip(*loc2[::-1]):
        log_counter+=1
        cv2.rectangle(img_np, pt, (pt[0] + w2, pt[1] + h2), (0, 0, 255), 2)
    if log_counter > edellinen_countti:
        edellinen_countti = log_counter
        print(log_counter)
        if log_counter > 27:
            print("pankkiin")
            mouse.position = (695, 112)
            time.sleep(0.1)
            mouse.click(Button.left,1)
            time.sleep(10)
            mouse.position = (345, 430)
            time.sleep(0.1)
            mouse.click(Button.left, 1)
            time.sleep(2)
            mouse.position = (470, 580)
            time.sleep(0.1)
            mouse.click(Button.left, 1)
            time.sleep(5)
            mouse.position = (770, 114)
            time.sleep(0.1)
            mouse.click(Button.left, 1)
            time.sleep(10)
            mouse.position = (500, 400)
            time.sleep(0.1)
            mouse.click(Button.left, 1)
            time.sleep(5)
            log_counter = 0
    if log_counter == 0:
        edellinen_countti = 0


    cv2.imshow("frame", img_np)
    cv2.waitKey(1)