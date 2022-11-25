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

# Required starting conditions:
# Left potentiometer must be >threshold. (as this is the end condition)

# Once arm enters rotation phase, movement is controlled with right potentiometer
# To end rotation phase, move left potentiometer below  threshold

# Once arm enters placement phase, movement is controlled with left potentiometer
# Move the potentiometer between 50% and 100% for position 1, move to 100% for position 2
# (Position 1 is in autoclave, position 2 is on top of autoclave)

# Spawn location of container
SPAWN_LOCATION = (0.63, 0.05, 0.05)
# Home location of arm
HOME_LOCATION = (0.406, 0.0, 0.483)

# Strength of grippers, when grabbing and releasing container
GRIPPER_STRENGTH = 40

# Sets threshold of left potentiometer
POS_1_THRESHOLD = 0.5
POS_2_THRESHOLD = 0.9

# Tuple of all containers
# In formate (id, size, colour)
CONTAINER_LIST = (
    (1, "small", "red"),
    (2, "small", "green"),
    (3, "small", "blue"),
    (4, "large", "red"),
    (5, "large", "green"),
    (6, "large", "blue")
    )

def get_container(c_id):
    """Returns container specified by container ID

    Args:
        c_id (int): A container ID ranging from 1-6

    Return:
        container (tuple): A tuple specifying container details of format (id, size, colour)
    """
    # For each container, check if ID matches
    for container in CONTAINER_LIST:
        if c_id == container[0]:
            # If so, return container
            return container

def move_arm(coordinates):
    """Move the QArm to the specified coordinates in 3D space

    Args:
        coordinates (tuple): 3-element tuple in format XYZ.
    """
    X = coordinates[0]
    Y = coordinates[1]
    Z = coordinates[2]
    arm.move_arm(X, Y, Z)
    time.sleep(1)

def check_left_potentiometer(threshold):
    """Checks whether left potentiometer is greater than given threshold

    Args:
        threshold (float): A threshold from 0->1

    Return:
        is_larger (bool): True if left potentiometer is larger than threshold, otherwise false
    """

    left_pot = potentiometer.left()
    is_larger = left_pot > threshold
    return is_larger

def spawn(x):
    """Spawn the container with specified ID

    Args:
        x (int): A container ID ranging from 1-6
    """
    arm.spawn_cage(x)

def pick_up():
    """Pick up the container from the spawn location
    """
    move_arm(SPAWN_LOCATION)
    arm.control_gripper(GRIPPER_STRENGTH)

    # Wait for grippers to close
    time.sleep(1)
    
    move_arm(HOME_LOCATION)

def rotate_base(c_id):
    """Rotate the QArm with input from right potentiometer, until left
    potentiometer is moved below threashold of 50%. Checks if aligned with
    specified container ID

    Args:
        c_id (int): A container ID ranging from 1-6
    """

    while True:
        
        # Map potentiometer input to reasonable range (0 to 1)->(-20 to 20)
        right_pot = potentiometer.right()
        right_pot = (right_pot - 0.5) * 40

        # Rotate base of arm accordingly
        arm.rotate_base(right_pot)
        time.sleep(0.5)

        # Check if left potentiometer is below threashold
        if not check_left_potentiometer(POS_1_THRESHOLD):
            
            # Get checked container
            container = get_container(c_id)
            colour = container[2]
            
            # Check if correct autoclave
            if arm.check_autoclave(colour):
                # If correct, continue
                return

def drop_off(c_id):
    """Drops off held container in autoclave, based off whether it is small or large

    Args:
        c_id (int): A container ID ranging from 1-6
    """
    container = get_container(c_id)
    size = container[1]
    colour = container[2]

    # Wait until left potentiometer is above threshold
    while not check_left_potentiometer(POS_1_THRESHOLD):
        continue
    # Wait to assert correct position
    # (so that operator can move potentiometer full distance)
    time.sleep(2)

    if check_left_potentiometer(POS_2_THRESHOLD):
        # Position 2

        # Activate autoclaves
        arm.activate_autoclaves()
        time.sleep(1)

        # Open target autoclave
        arm.open_autoclave(colour)

        time.sleep(1)

        # Rotate joints to place object in autoclave
        arm.rotate_elbow(15)
        arm.rotate_shoulder(25)

        time.sleep(1)

        # Drop off object, by opening grippers
        arm.control_gripper(-GRIPPER_STRENGTH)

        time.sleep(1)

        # Close target autoclave
        arm.open_autoclave(colour, False)

        time.sleep(1)
        
    else: 
        # Position 1

        # Rotate joints to place object on top of autoclave
        arm.rotate_elbow(-40)
        arm.rotate_shoulder(50)

        time.sleep(1)

        # Drop off object, by opening grippers
        arm.control_gripper(-GRIPPER_STRENGTH)

        time.sleep(1)

    # Deactivate autoclaves for safety
    arm.deactivate_autoclaves()
    

# Create randomized list of digits 1->6, this will be the cycle order
# For simulation purposes only
container_order = [1, 2, 3, 4, 5, 6]
random.shuffle(container_order)
print(container_order)

def __main__():
    # Loop through container ids
    for container_id in container_order:
        # Spawn container
        spawn(container_id)

        # Pick up container
        pick_up()

        # Rotate base
        rotate_base(container_id)

        # Drop off
        drop_off(container_id)

        # Return home
        arm.home()
    
    
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
    

