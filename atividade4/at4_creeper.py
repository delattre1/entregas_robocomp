#! /usr/bin/env python
# -*- config:utf-8 -*-

import rospy, tf, math,cv2, time, cormodule
from geometry_msgs.msg import Twist, Vector3, Pose
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, CompressedImage, LaserScan
from nav_msgs.msg import Odometry
import numpy as np

from tf import transformations

bridge = CvBridge()

x, y, alfa, contador, distancia_x = None, None, -1, 0, 0
distancia_x = 0
diminuir_velocidade = False
para_tudo = False

def posicao_odometry(msg):
    # print(msg.pose.pose)
    global x
    global y
    global alfa
    global contador

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    quat = msg.pose.pose.orientation
    lista = [quat.x, quat.y, quat.z, quat.w]
    angulos_rad = transformations.euler_from_quaternion(lista)
    alfa = angulos_rad[2]
    angs_degree = np.degrees(angulos_rad)
    # print("Posicao (x,y)  ({:.2f} , {:.2f}) + angulo {:.2f}".format(x, y, angs_degree[2]))


def callback(msg):
    global distancia_x
    global andar_frente
    global diminuir_velocidade
    global para_tudo
    contador_diminuir_velocidade = 0 
    distancia_x = len(msg.ranges)
    lista_distancias = list(msg.ranges)
    contador_parar = 0 

    for i in range(len(lista_distancias)):
        dist = lista_distancias[i]
        if (i < 21 or i > 339) and str(dist) != "inf":
            print(dist)

            if dist <= 0.25:
                contador_parar += 1
                if contador_parar >= 5:
                    print("PARA TUDO")
                    para_tudo = True

            elif dist <= 0.4:
                contador_diminuir_velocidade += 1
                if contador_diminuir_velocidade >= 5:
                    print("DIMINUIR VELOCIDADE")
                    diminuir_velocidade = True


    contador_diminuir_velocidade = 0 
    contador_parar = 0
        
    print(" ")
    andar_frente = True 

def roda_todo_frame(imagem):
    global cv_image
    global media
    global centro

    try:
        cv_image = bridge.compressed_imgmsg_to_cv2(imagem, "bgr8")
        media, centro, maior_area = cormodule.identifica_cor(cv_image)
        # cv2.imshow("camera", cv_image)
    except CvBridgeError as e:
        print("ex", e)

cv_image = None
media, centro = [], []
area = 0.1
andar_frente = False
vel_rot = .3
vel_lin = 0.1

contador_deteccao_creeper = 1
        
if __name__=="__main__":

    rospy.init_node("creeperzao")
    topico_imagem = "/camera/rgb/image_raw/compressed"
    #topico_camera = "/raspicam/image_raw"
    odom_sub = rospy.Subscriber("/odom", Odometry, posicao_odometry)
    recebe_img = rospy.Subscriber(topico_imagem, CompressedImage, roda_todo_frame, queue_size=4, buff_size=2**24)
    scanner    = rospy.Subscriber("/scan", LaserScan, callback)
    vel_saida  = rospy.Publisher("/cmd_vel", Twist, queue_size=3) 
    
    detectou_imagem = False
    vel = Twist(Vector3(0,0,0), Vector3(0,0,vel_rot))
    
    is_centralizando = True
    contador_centralizacao = 0 
    girando_direita_t1, girando_direita_t2 = False, False
    while not rospy.is_shutdown():
        # vel = Twist(Vector3(0,0,0), Vector3(0,0,0))
        if not para_tudo:
            if diminuir_velocidade:
                vel_lin = 0.02
            if is_centralizando: 
                if len(media) != 0 and len(centro) != 0:
                    contador_deteccao_creeper += 1
                    if contador_deteccao_creeper >= 10:
                        detectou_imagem = True
    
                if detectou_imagem and media[0] > centro[0]:
                    girando_direita_t1 = True
                    # print(centro)
    
                elif detectou_imagem and media[0] < centro[0]:
                    girando_direita_t1 = False
                    # print(centro)
    
                if girando_direita_t1 != girando_direita_t2:
                    vel_rot /= -2
                    contador_centralizacao += 1
                    print(contador_centralizacao)
                    if contador_centralizacao >= 8:
                        is_centralizando = False
                        rospy.sleep(1)
    
                girando_direita_t2 = girando_direita_t1
                vel = Twist(Vector3(0,0,0), Vector3(0,0, vel_rot)) 
                vel_saida.publish(vel)
                rospy.sleep(0.1)
                #print("centralizando")
    
            else:
                # print('centralizou')
                if andar_frente:#andar_frente:
                    vel = Twist(Vector3(vel_lin,0,0), Vector3(0,0, 0)) 
                    vel_saida.publish(vel)
                    rospy.sleep(3)
    
                    is_centralizando = True
                    print('comeca a centralizar')
                    contador_centralizacao = 0 
                    vel_rot = .4
        else:
            vel = Twist(Vector3(0,0,0), Vector3(0,0,0))
            vel_saida.publish(vel)
            rospy.sleep(0.2)


