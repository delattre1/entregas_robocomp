#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import sys
import auxiliar as aux
import math
import numpy as np


cap = cv2.VideoCapture('line_following.mp4')

while(True):
    ret, frame = cap.read()
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    src = frame
    dst = cv2.Canny(src, 50, 200) # aplica o detector de bordas de Canny à imagem src
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR) # Converte a imagem para BGR para permitir desenho colorido

    if True: # HoughLinesP
        lines = cv2.HoughLinesP(dst, 10, math.pi/180.0, 100, np.array([]), 5, 5)
        print("Used Probabilistic Rough Transform")
        print("The probabilistic hough transform returns the end points of the detected lines")
        a,b,c = lines.shape
        print("Valor de A",a, "valor de lines.shape", lines.shape)
        for i in range(a):
            # Faz uma linha ligando o ponto inicial ao ponto final, com a cor vermelha (BGR)
            cv2.line(cdst, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)

    else:    # HoughLines
        # Esperemos nao cair neste caso
        lines = cv2.HoughLines(dst, 1, math.pi/180.0, 50, np.array([]), 0, 0)
        a,b,c = lines.shape
        for i in range(a):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0, y0 = a*rho, b*rho
            pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
            pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )
            cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)
        print("Used old vanilla Hough transform")
        print("Returned points will be radius and angles")

    cv2.imshow("source", src)
    cv2.imshow("detected lines", cdst)
    cv2.waitKey(0)

    # Display the resulting frame
    # cv2.imshow('frame',frame)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

print(hsv3,hsv4)
