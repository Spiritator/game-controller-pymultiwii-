# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 14:13:52 2017

@author: 蔡永聿
"""
#This is a code for using logitech extreme 3D game controller through pygame and pymultiwii to control multiwii system drone.
import pygame,time,datetime,csv
from pymultiwii import MultiWii

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 80)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 50
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10


pygame.init()
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()


    
# Set the width and height of the screen [width,height]
size = [1000, 450]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Control Panel")

#Loop until the user clicks the close button.
done = False

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)


if __name__ == "__main__":
    
    screen.fill(WHITE)
    textPrint.reset()

    controller = pygame.joystick.Joystick(0)
    controller.init()    

    butterfly = MultiWii("COM5")
    print("Butterfly Connected")
    time.sleep(1)
    print("Controller Connected")
    time.sleep(1)
    sensitivity=500 #max 500
    print('Default Sensitivity : %d' % sensitivity)
    time.sleep(1)

    roll=1500
    pitch=1500
    rotate=1500
    throttle=1000
    
    butterfly.disarm()
    
    console_messege_timer_start=0
    auto_land=0
    
#    control_signal_log={}
    control_signal_log_timer_start=time.time()
    
    try:
        # -------- Main Program Loop -----------
        while done==False:
            # EVENT PROCESSING STEP
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop
            
            # DRAWING STEP
            # First, clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command.
            screen.fill(WHITE)
            textPrint.reset()
                         
           # controller.update()
                        
            if time.time() - console_messege_timer_start > 2:
                console_messege=" "
                
            if controller.get_button(0):
                butterfly.arm()
                console_messege="Armed."
                console_messege_timer_start =  time.time()
            elif controller.get_button(1):
                butterfly.disarm()
                console_messege="Disarmed."
                console_messege_timer_start =  time.time()
            elif controller.get_button(10):
                done=True        	
            #example of 4 RC channels to be send
            elif controller.get_button(11):
                pitch=1500
                roll=1500
                rotate=1500
                throttle=1000 
            else:
                pitch=int(controller.get_axis(1)*(-1)*sensitivity+1500)
                roll=int(controller.get_axis(0)*sensitivity+1500)
                rotate=int(controller.get_axis(3)*sensitivity+1500)
                throttle=int(controller.get_axis(2)*((-1)*sensitivity)+1500)
                
            data = [roll,pitch,rotate,throttle]
            butterfly.sendCMD(8,MultiWii.SET_RAW_RC,data)        
            
            textPrint.print(screen, "Console Messege: {}".format(console_messege) )

            textPrint.print(screen, " {}".format(" ") )
            
            textPrint.print(screen, "Roll:      {}".format(roll) )
            textPrint.print(screen, "Pitch:     {}".format(pitch) )
            textPrint.print(screen, "Rotate:    {}".format(rotate) )
            textPrint.print(screen, "Throttle: {}".format(throttle) )
            
            textPrint.print(screen, " {}".format(" ") )
            
            textPrint.print(screen, "Sensitivity: {}".format(sensitivity) )
    
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
            
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            
            #recording flight control signal
#            if throttle!=1000:
#                control_signal_log["%.2f" % (time.time()-control_signal_log_timer_start)]=data
        
            # Limit to 20 frames per second
            clock.tick(20)
            
    except Exception as error:
        print ("Error on Main: "+str(error))


    butterfly.disarm()
    time.sleep(1)
    butterfly.disarm()
    time.sleep(1)
    butterfly.disarm()    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()

#if len(control_signal_log>0):
#    file_name=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
#    
#    with open('control_signal_log/'+file_name+'.csv', 'w', newline='') as csvfile:
#        fieldnames=['time','roll','pitch','rotate','throttle']
#        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#    
#        writer.writeheader()
#        for item in control_signal_log:
#            writer.writerow({'time':item,'pitch':control_signal_log[item][0],'roll':control_signal_log[item][1],'rotate':control_signal_log[item][2],'throttle':control_signal_log[item][3]})
#        
