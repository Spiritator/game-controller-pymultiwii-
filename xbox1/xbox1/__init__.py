#!/usr/bin/env python
########################################################################
#All Reference from Reference from Karan Nayan https://github.com/DexterInd/GoPiGo/blob/master/Software/Python/Examples/PS3_Control/ps3.py
########################################################################                                               
# This is the library to read values from PS3 Dualshock 3 controller
#                                
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     	Date      		Comments
# Karan Nayan   11 July 14		Initial Authoring                                                   
'''
## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2017  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''        
#
# Dependencies- pygame
# Pairing the controller using bluetooth
# http://booting-rpi.blogspot.ro/2012/08/dualshock-3-and-raspberry-pi.html
# PS3 Key configuration http://wiki.ros.org/ps3joy
# 
# Key values can be obtained by creating a ps3 object and calling update() regularly
########################################################################
import pygame, sys, time ,os
from pygame.locals import *

#PS3 functions and variables
class xbox1:
	joystick=0
	joystick_count=0
	numaxes=0
	numbuttons=0
	left=right=up=down=lb=rb=A=B=X=Y=share=menu=xbox=joystick_left=joystick_right=0
	a_joystick_left_x=a_joystick_left_y=a_joystick_right_x=a_joystick_right_y=a_trigger=0
	
	#Initialize the controller when the oject is created
	def __init__(self):
		#Make the stdout buffer as 0,because of bug in Pygame which keeps on printing debug statements
		#http://stackoverflow.com/questions/107705/python-output-buffering
		#sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
		
		pygame.init()
		pygame.joystick.init()
		xbox1.joystick = pygame.joystick.Joystick(0)
		xbox1.joystick.init()
		xbox1.joystick_count = pygame.joystick.get_count()
		xbox1.numaxes = xbox1.joystick.get_numaxes()
		xbox1.numbuttons = xbox1.joystick.get_numbuttons()
        #modified
		#get count of joysticks=1, axes=27, buttons=19 for DualShock 3
	
	#Update the button values
	def update(self):
		loopQuit = False
		button_state=[0]*self.numbuttons
		button_analog=[0]*self.numaxes
		#while loopQuit == False:
		outstr = ""
		
		#Start suppressing the output on stdout from Pygame
		#devnull = open('/dev/null', 'w')
		#oldstdout_fno = os.dup(sys.stdout.fileno())
		#os.dup2(devnull.fileno(), 1)
		
		#Read analog values
		for i in range(0,self.numaxes):
			button_analog[i] = self.joystick.get_axis(i)	

		self.a_joystick_left_x	=button_analog[0]
		self.a_joystick_left_y	=button_analog[1]
		self.a_joystick_right_y	=button_analog[3]
		self.a_joystick_right_x	=button_analog[4]
		self.a_trigger	        =button_analog[2]

		
		#Read digital values
		for i in range(0,self.numbuttons):
			button_state[i]=self.joystick.get_button(i)
            
		self.A			      =button_state[0]
		self.B	            =button_state[1]
		self.X	            =button_state[2]
		self.Y			      =button_state[3]
		self.lb				   =button_state[4]
		self.rb				   =button_state[5]
		self.share		      =button_state[6]
		self.menu			   =button_state[7]
		self.joystick_left   =button_state[8]
		self.joystick_right  =button_state[9]
		
		self.up				=self.joystick.get_hat(0)[1]
		self.right			=self.joystick.get_hat(0)[0]
		self.down			=self.joystick.get_hat(0)[1]*(-1)
		self.left			=self.joystick.get_hat(0)[0]*(-1)

		#Enable output on stdout
		#os.dup2(oldstdout_fno, 1)	
		#os.close(oldstdout_fno)
		
		#refresh
		pygame.event.get()
		return button_analog
	