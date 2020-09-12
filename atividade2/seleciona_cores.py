#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__      = "Matheus Dib, Fabio de Miranda"
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
import sys
import auxiliar as aux
from scipy.spatial import distance as dist


if len(sys.argv) > 1:
    arg = sys.argv[1]
    try:
        input_source=int(arg) # se for um device
    except:
        input_source=str(arg) # se for nome de arquivo
else:   
    input_source = 0

cap = cv2.VideoCapture(input_source)
# Parameters to use when opening the webcam.
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

lower = 0
upper = 1
# print("Press q to QUIT")
# Returns an image containing the borders of the image
# sigma is how far from the median we are setting the thresholds
def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.GaussianBlur(frame,(5,5),0) #remover ruidos
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #after colorpicker is used
    color_picker_ciano=  '#003762'
    hsv1_ciano, hsv2_ciano = aux.ranges(color_picker_ciano)
    mask_ciano = cv2.inRange(hsv_frame.copy(), hsv1_ciano, hsv2_ciano)    

    color_picker_magenta=  '#5f0428'
    hsv1_magenta, hsv2_magenta= aux.ranges(color_picker_magenta)
    mask_magenta = cv2.inRange(hsv_frame.copy(), hsv1_magenta, hsv2_magenta)    

    masks_magenta_and_ciano = cv2.add(mask_ciano,mask_magenta)  
    bordas = auto_canny(masks_magenta_and_ciano) #deopois de filtrar só ter as cores selecionadas na imagem, detecta as bordas
    bordas_color = cv2.cvtColor(bordas, cv2.COLOR_GRAY2BGR)

    circles = None
    circles=cv2.HoughCircles(bordas,cv2.HOUGH_GRADIENT,2,40,param1=50,param2=100,minRadius=5,maxRadius=60)
    # segmentado_img_magenta = cv2.morphologyEx(mask_magenta,cv2.MORPH_CLOSE,np.ones((4, 4)))
    #changing the output frame 
    if circles is not None:  
        maior_raio = 0
        segundo_maior_raio = 0    
        posicao_centro1 = (0,0)  
        posicao_centro2 = (0,0)
        circles = np.uint16(np.around(circles))
        contador = 0

        for i in circles[0,:]:
            if i[2] >= maior_raio:
                segundo_maior_raio = maior_raio
                posicao_centro2 = posicao_centro1
                maior_raio = i[2]
                posicao_centro1 = (i[0],i[1])

        # draw the outer circle
        # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
        cv2.circle(bordas_color,posicao_centro1,maior_raio,(0,255,0),2)
        # draw the center of the circle
        cv2.circle(bordas_color,(posicao_centro2),segundo_maior_raio,(0,0,255),3)
        #linha de centro a centro 
        print(posicao_centro1)
        print(posicao_centro2)
        cv2.line(bordas_color,posicao_centro1,posicao_centro2 ,(255,0,0),5)
        deltax = (posicao_centro2[0] - posicao_centro1[0])
        deltay = (posicao_centro2[1] - posicao_centro1[1])
        distancia_entre_centros = (deltax**2+deltay**2)**(1/2)
        print(distancia_entre_centros, deltax, deltay)
        D = dist.euclidean((posicao_centro1[0], posicao_centro2[0]), (posicao_centro1[1], posicao_centro1[1]))
        print("D: ",D)
    #ta atirando raios, arrumar as posicoes

    cv2.imshow('Nome da Janela', bordas_color)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#  When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
