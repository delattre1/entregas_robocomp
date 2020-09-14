#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import sys
import auxiliar as aux

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        try:
            input_source=int(arg) # se for um device
        except:
            input_source=str(arg) # se for nome de arquivo
    else:   
        input_source = 0

    cap = cv2.VideoCapture(input_source)

    hsv1, hsv2 = aux.ranges('#00477f')
    hsv3, hsv4 = aux.ranges("#5affff")
    hsv1[0] = 79
    hsv2[0] = 113
    hsv3[0] = 139
    hsv4[0] = 172
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret == False:
            print("Codigo de retorno FALSO - problema para capturar o frame")

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Our operations on the frame come here

        mask1 = cv2.inRange(frame_hsv, hsv1, hsv2)  
        mask2 = cv2.inRange(frame_hsv, hsv3,hsv4)
        mask = mask1 + mask2


        # Display the resulting frame
        # cv2.imshow('frame',frame)
        cv2.imshow('frame', frame)

        cv2.imshow('mask', mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    print(hsv3,hsv4)
