#! /usr/bin/env python
# -*- coding:utf-8 -*-
import rospy
from geometry_msgs.msg import Twist, Vector3
import math

alfa = math.pi/2
contador = 0
pula = 100
vel_ang = math.pi/8
vel_lin = 0.2
sleep_rot = alfa/vel_ang
sleep_trans = 2/vel_lin #distancia / velocidade

if __name__ == "__main__":
    rospy.init_node("quadrado_odom")
    pub = rospy.Publisher("cmd_vel", Twist, queue_size=3)
    t0 = rospy.get_rostime()

    try:
        while not rospy.is_shutdown():
            vel0 = Twist(Vector3(0,0,0), Vector3(0,0,0))
            velocidade_ang = Twist(Vector3(0,0,0), Vector3(0,0,vel_ang)) 

            #publish bobo
            pub.publish(vel0)
            rospy.sleep(0.1)

            print("t0", t0)
            if t0.nsecs == 0:
                t0 = rospy.get_rostime()
                print("waiting for timer")
                continue      

            t1 = rospy.get_rostime()
            elapsed = (t1 - t0)
            print("Passaram ", elapsed.secs, " segundos")

            velocidade_l = Twist(Vector3(vel_lin,0,0), Vector3(0,0,0)) 
            pub.publish(velocidade_l)
            rospy.sleep(sleep_trans)

            pub.publish(vel0)
            rospy.sleep(0.5)

            pub.publish(velocidade_ang)
            rospy.sleep(sleep_rot)

            pub.publish(vel0) 
            rospy.sleep(0.5)

    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")
        