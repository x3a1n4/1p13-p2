ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P2B' # Enter the project identifier i.e. P2A or P2B
#--------------------------------------------------------------------------------
import sys, random
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
arm = qarm(project_identifier,ip_address,QLabs,hardware)
potentiometer = potentiometer_interface()
#--------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
PICKUP_POSITION = (0.532, 0.046, 0.044)
HOME_POSITION = (0.406, 0.0, 0.483)

RED_POSITION = (0.0, -0.572, 0.246)
GREEN_POSITION = (0.0, 0.572, 0.246)
BLUE_POSITION =(-0.605, 0.22, 0.273)

def move_arm(position):
    """Moves QArm to position specified by tuple
    Parameters
    ----------
    position : tuple
        The target position of the arm, in (X, Y, Z) coordinates
    """
    arm.move_arm(position[0], position[1], position[2])
    # move_arm does not stop program, so wait approximate amount
    # until movement is completed
    time.sleep(1)

def pickup_container():
    """Picks up container at pickup position, returns to home position
    """
    move_arm(PICKUP_POSITION)
    arm.control_gripper(40)
    time.sleep(1)
    move_arm(HOME_POSITION)

# I believe that this isn't neccesarily what the doc wants, edit
def rotate_base():
    """Moves QArm to autoclave position specified by right potentiometer
    Parameters
    ----------
    colour : str
        Target autoclave colour, either "red", "green", or "blue"
    Returns
    -------
    string
        A string of either "red", "green", or "blue"
    """
    
    right_pot = potentiometer.right()
    
    #for red block
    if (potentiometer.right() > 0.79):
        move_arm(RED_POSITION)
        colour = "red"
    #for green block
    elif (potentiometer.right() > 0.39):
        move_arm(GREEN_POSITION)
        colour = "green"
    #for blue block
    else:
        move_arm(BLUE_POSITION)
        colour = "blue"

    # Let go of block
    arm.control_gripper(-40)
    time.sleep(1)

    return colour

def drop_off():
    """Drops off container in autoclave position, specified by left potentiometer
    """
    left_pot = potentiometer.left()

    # position 1
    if 1 < left_pot < 0.5:
        raise NotImplemented()
    else:
        raise NotImplemented()

def __main__():
    # Spawn random container
    spawn(random.randint(1, 6))

    # Pick up container, return home
    pickup_container()

    # Wait, so operator can input correct drop off position w/ potentiometer
    time.sleep(5)

    # Rotate to autoclave position specified by potentiometer
    colour = rotate_base()

    # Verify autoclave
    # TODO: Look at alternate implementation (yield?)
    # this currently doen't affect program flow
    arm.check_autoclave(colour)

    # Wait, so operator can input correct drop off position w/ potentiometer
    time.sleep(5)

    drop_off()

def spawn(x):
    arm.spawn_cage(x)

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

