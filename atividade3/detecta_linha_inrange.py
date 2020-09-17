import auxiliar as aux
import cv2
import numpy as np
import sys
import math

cap = cv2.VideoCapture('testevideo1.mp4')
# hsv1, hsv2 = aux.ranges('#fffbf6')
# print(hsv1, hsv2)
# print(hsv1[0])
# hsv1[0] = 0
# hsv1[1] = 0
# hsv1[2] = 0
# hsv2[0] = 0
# hsv2[1] = 0
# hsv2[2] = 255

sensitivity = 15
lower_white = np.array([0,0,255-sensitivity])
upper_white = np.array([255,sensitivity,255])

min_line_length = 30
max_line_gap = 15


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #create a filter for white color
    mask = cv2.inRange(frame_hsv, lower_white,upper_white)

    src = mask#frame
    dst = cv2.Canny(src, 200, 350) # aplica o detector de bordas de Canny à imagem src
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR) # Converte a imagem para BGR para permitir desenho colorido

    #houghlinesp
    linesp = cv2.HoughLinesP(dst, 10, math.pi/180.0, 100, np.array([]), min_line_length, max_line_gap)
    a,b,c = linesp.shape
    print(linesp)
    for i in range(a):
        l = linesp[i][0]
        print(l)
        cv2.waitKey(0)
        cv2.line(cdst, (l[0], l[1]), (l[2], l[3]), (255,0,0), 3, cv2.LINE_AA)

    #display
    cv2.imshow("frame", cdst)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()