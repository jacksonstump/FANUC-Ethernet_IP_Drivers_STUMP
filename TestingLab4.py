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
Bunson = '172.29.208.123'


HOME        = [0,           0,          0,          0,          -90,        30]
        

def main():
    
    beaker = robot(Beaker)
    bunson = robot(Bunson)
    cycles = 1
    beaker.set_speed(300)
    beaker.gripper("open")
    bunson.set_speed(300)
    bunson.gripper("open")

    while cycles <= 1:
        
        print("--------------------")
        print(f"Cycle: {cycles}/3")
        print("--------------------")

        print("Moving HOME")
        move_robot_joint(beaker, HOME)
        move_robot_joint(bunson, HOME)
        cycles += 1

    print("--------------------")
    print("Cycle STOP")
    print("--------------------")

if __name__ == "__main__":
    main()