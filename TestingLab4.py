import socket
import time
import pickle
from robot_controller import robot

def move_robot_linear(beaker, cartcoords):
    beaker.send_coords(*cartcoords)
    beaker.start_robot()
    
def move_robot_joint(beaker, jointcoords):
    beaker.set_pose(jointcoords)
    beaker.start_robot()
    
def joint_offset(beaker, joint, offset):
    beaker.write_joint_offset(joint, offset)
    beaker.start_robot()
    
def gripper(beaker,position,dwell):
    beaker.gripper(position)
    time.sleep(dwell)    

Beaker = '172.29.208.124'

HOME        = [0,           0,          0,          0,          -90,        30]
INT_Dice1   = [825.267,     351.151,    -180,       -179.286,   0.64,       31.021]        

def main():
    
    beaker = robot(Beaker)
    cycles = 1
    beaker.set_speed(300)
    beaker.gripper("open")



    while cycles <= 1:
        
        print("--------------------")
        print(f"Cycle: {cycles}/3")
        print("--------------------")

        print("Moving HOME")
        move_robot_joint(beaker, HOME)
        
        print("Position Above Dice")
        move_robot_linear(beaker, INT_Dice1)
        
        cycles += 1

    print("--------------------")
    print("Cycle STOP")
    print("--------------------")

if __name__ == "__main__":
    main()