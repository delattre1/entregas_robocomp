#! /usr/bin/env python

import rospy
import numpy as np
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan

#robô avançar quando o obstáculo bem à sua frente estiver a menos de 1.0m e recuar quando estiver a mais de 1.02 m.
andar_pra_frente = True

def scaneou(dado):
	global andar_pra_frente
	print("Faixa valida: ", dado.range_min , " - ", dado.range_max )
	print("Leituras:")
	print("leitura em zero grau", dado.ranges[0])
	distancia = dado.ranges[0]

	if distancia < 1.0:
		andar_pra_frente = False
	elif distancia >= 1.02:
		andar_pra_frente = True

if __name__=="__main__":

	rospy.init_node("le_scan")
	velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 3)
	recebe_scan = rospy.Subscriber("/scan", LaserScan, scaneou)
	vel = 0.4

	while not rospy.is_shutdown():
		print("Oeee")
		## ir em frente enquanto nao houver objeto a 1m ou menos
		if andar_pra_frente:
			velocidade = Twist(Vector3(vel, 0, 0), Vector3(0, 0, 0))
		else:
			velocidade = Twist(Vector3(-vel, 0, 0), Vector3(0, 0, 0))
		velocidade_saida.publish(velocidade)
		rospy.sleep(0.01)
