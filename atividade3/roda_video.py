#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import sys
import math


print("Baixe o arquivo a seguir para funcionar: ")
print("https://github.com/Insper/robot20/raw/master/aula02/hall_box_battery_1024.mp4")

cap = cv2.VideoCapture('testevideo1.mp4')

min_line_length = 20
max_line_gap = 15

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if ret == False:
        print("Codigo de retorno FALSO - problema para capturar o frame")

    # Our operations on the frame come here
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    # cv2.imshow('frame',frame)
    # cv2.imshow('gray', frame)

    src = frame
    dst = cv2.Canny(src, 200, 350) # aplica o detector de bordas de Canny à imagem src
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR) # Converte a imagem para BGR para permitir desenho colorido

    if True: # HoughLinesP
        lines = cv2.HoughLinesP(dst, 10, math.pi/180.0, 100, np.array([]), min_line_length, max_line_gap)
        # print("Used Probabilistic Rough Transform")
        # print("The probabilistic hough transform returns the end points of the detected lines")
        a,b,c = lines.shape
        # print("Valor de A",a, "valor de lines.shape", lines.shape)
        for i in range(a):
            # Faz uma linha ligando o ponto inicial ao ponto final, com a cor vermelha (BGR)
            l = lines[i][0]
            cv2.line(cdst, (l[0], l[1]), (l[2], l[3]), (3*i,2*i,i), 3, cv2.LINE_AA)
            # cv2.line(cdst, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (50, 50, 100), 3, cv2.LINE_AA)
            # cv2.line(cdst,(0,0),(100,100),(255,25,25), 3,cv2.LINE_AA)

    else:    # HoughLines
        # Esperemos nao cair neste caso
        lines = cv2.HoughLines(dst, 1, math.pi/180.0, 50, np.array([]), 0, 0)
        a,b,c = lines.shape
        for i in range(b):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0, y0 = a*rho, b*rho
            pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
            pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )
            cv2.line(cdst, pt1, pt2, (50, 100, 0), 3, cv2.LINE_AA)
        # print("Used old vanilla Hough transform\n")
        # print("Returned points will be radius and angles\n")

    cv2.imshow("source", src)
    cv2.imshow("detected lines", cdst)
    cv2.waitKey(0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()



# #!/usr/bin/python
# # -*- coding: utf-8 -*-

# import cv2
# import sys
# import auxiliar as aux

# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         arg = sys.argv[1]
#         try:
#             input_source=int(arg) # se for um device
#         except:
#             input_source=str(arg) # se for nome de arquivo
#     else:   
#         input_source = 0

#     cap = cv2.VideoCapture(input_source)

#     hsv1, hsv2 = aux.ranges('#00477f')
#     hsv3, hsv4 = aux.ranges("#5affff")
#     hsv1[0] = 79
#     hsv2[0] = 113
#     hsv3[0] = 139
#     hsv4[0] = 172
#     while(True):
#         # Capture frame-by-frame
#         ret, frame = cap.read()
        
#         if ret == False:
#             print("Codigo de retorno FALSO - problema para capturar o frame")

#         frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#         # Our operations on the frame come here

#         mask1 = cv2.inRange(frame_hsv, hsv1, hsv2)  
#         mask2 = cv2.inRange(frame_hsv, hsv3,hsv4)
#         mask = mask1 + mask2


#         # Display the resulting frame
#         # cv2.imshow('frame',frame)
#         cv2.imshow('frame', frame)

#         cv2.imshow('mask', mask)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # When everything done, release the capture
#     cap.release()
#     cv2.destroyAllWindows()

#     print(hsv3,hsv4)
