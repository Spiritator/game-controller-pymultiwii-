# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 13:51:32 2017

@author: 蔡永聿
"""

"""ps3_contoller_multiwii.py: Test script to send RC commands to a MultiWii Board by a Xbox One controller."""

__author__ = "Leo Tsai"

__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Leo Tsai"
__email__ = "leo51leo51leo51@gmail.com"
__status__ = "Development"

import time,pygame
from pymultiwii import MultiWii

if __name__ == "__main__":
    
    butterfly = MultiWii("COM5")
    print("Butterfly Connected")
    time.sleep(1)
    pygame.init()
    pygame.joystick.init()
    controller = pygame.joystick.Joystick(0)
    controller.init()    
    print("Controller Connected")
    time.sleep(1)
    sensitivity=200 #max 500
    print('Default Sensitivity : 200')
    time.sleep(1)

    #lock=1
    pitch=1500
    roll=1500
    rotate=1500
    throttle=1000

    try:
        while True:
            #controller.update()
            
            if controller.get_button(1):
                butterfly.arm()
                #lock=0
                print ("Butterfly is armed now!")
            elif controller.get_button(0):
                butterfly.disarm()
                print ("Disarmed.")
            elif controller.get_button(3):
                break
        	#example of 4 RC channels to be send
            elif controller.get_button(2):
                pitch=1500
                roll=1500
                rotate=1500
                throttle=1000 
            elif controller.get_button(5):
                if sensitivity<500:
                    sensitivity=sensitivity+50
                    print('Sensitivity : %d' % sensitivity)
            elif controller.get_button(4):
                if sensitivity>100:
                    sensitivity=sensitivity-50
                    print('Sensitivity : %d' % sensitivity)
            
            pitch=int(controller.get_axis(3)*((-1)*sensitivity)+1500)
            roll=int(controller.get_axis(4)*sensitivity+1500)
            rotate=int(controller.get_axis(0)*sensitivity+1500)
            if controller.get_axis(1)<0:
                throttle=int(controller.get_axis(1)*((-2)*sensitivity)+1000)
            else:
                throttle=1000 
            
#            axes=controller.get_numaxes
#            for i in range(0,axes):
#                axis=controller.get_axis(i)
#                print(axis,end='')
#            print('')
            
            data = [pitch,roll,rotate,throttle]
            print(data)                
            butterfly.sendCMD(8,MultiWii.SET_RAW_RC,data)
            
            #time.sleep(0.02)
                       
    except Exception as error:
        print ("Error on Main: "+str(error))
    
    butterfly.disarm()
    time.sleep(3)
    butterfly.disarm()
    time.sleep(3)
    butterfly.disarm()