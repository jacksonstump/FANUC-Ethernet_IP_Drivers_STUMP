import socket
import sys
import time
import pickle
import random
from os.path import dirname 
sys.path.append(dirname(__file__)+"\\src")
from robot_controller import robot

HOME        = [0,           0,          0,          0,          -90,        30]
INT_Dice1   = [825.267,     351.151,    -180,       -179.286,   0.64,       31.021]
Dice_Grab1  = [825.267,     351.151,    -202.474,   -179.286,   0.64,       31.021]
INT_DICE2   = [803.57,      670,        -50,        -180,       0.64,       31.021]
DICE_DROP1  = [803.57,      670,        -202,       -180,       0.64,       31.021]
INT_DICE3   = [112.372,     675,        -50,        -180,       0.64,       31.021]
Dice_Grab2  = [112.372,     675,        -202,       -180,       0.64,       31.021]
DICE_DROP2  = [886,         320,        -202.5,     180,        0.696,      -59]
INT_DICE4   = [886,         320,        -180,       180,        0.696,      -59]
Rotate      = [0, 0, 0, 0, 90]

def move_robot_linear(beaker, cartcoords):
    beaker.write_cartesian_position(*cartcoords)
    beaker.start_robot()
    
def move_robot_joint(beaker, jointcoords):
    beaker.set_pose(jointcoords)
    beaker.start_robot()
    
def joint_offset(beaker, joint, offset):
    beaker.write_joint_offset(joint, offset)
    beaker.start_robot()
    
    
Robot_IP = '172.29.208.124'



        

def main():
    
    beaker = robot(Robot_IP)
    beaker.set_speed(300)
    cycles = 1


    while cycles <= 1:
        
        print("--------------------")
        print(f"Cycle: {cycles}/3")
        print("--------------------")

        print("Moving HOME")
        move_robot_joint(beaker, HOME)
        
        


        print("--------------------")
        print("Final Position")
        print("--------------------")
        

        cycles += 1

    print("--------------------")
    print("Cycle STOP")
    print("--------------------")

if __name__ == "__main__":
    main()