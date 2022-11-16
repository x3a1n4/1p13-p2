ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P2B' # Enter the project identifier i.e. P2A or P2B
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
arm = qarm(project_identifier,ip_address,QLabs,hardware)
potentiometer = potentiometer_interface()
#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
i=1

def pickup_container():
    arm.move_arm(0.532, 0.046, 0.044)
    time.sleep(1)
    arm.control_gripper(40)
    time.sleep(1)
    arm.move_arm(0.406, 0.0, 0.483)
    i=0

def spawn(x):
    arm.spawn_cage(x)



while (i==0):
    if (potentiometer.left()>0.60):
        #for red block
        if (potentiometer.right() > 0.79) and (potentiometer.right() < 1.0):
            arm.move_arm(0.0, -0.572, 0.246)
            time.sleep(1)
            arm.control_gripper(-40)
            time.sleep(1)
            i=1
        #for green block
        if (potentiometer.right() > 0.39) and (potentiometer.right() <= 0.79):
            arm.move_arm(0.0, 0.572, 0.246)
            time.sleep(1)
            arm.control_gripper(-40)
            time.sleep(1)
            i=1
        #for blue block
        if (potentiometer.right() > 0.2) and (potentiometer.right() <= 0.39):
            arm.move_arm(-0.605, 0.22, 0.273)
            time.sleep(1)
            arm.control_gripper(-40)
            time.sleep(1)
            i=1




#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

