import sys
import time
from robot_controller import robot

HOME        = [0,           0,          0,          0,          -90,        30]
INT_Dice1   = [825.267,     351.151,    -180,       -179.286,   0.64,       31.021]
Dice_Grab1  = [825.267,     351.151,    -202.474,   -179.286,   0.64,       31.021]
INT_DICE2   = [803.57,      670,        -50,        -180,       0.64,       31.021]
DICE_DROP1  = [803.57,      670,        -202,       -180,       0.64,       31.021]
INT_DICE3   = [112.372,     684.5,      -50,        -180,       0.64,       31.021]
Dice_Grab2  = [112.372,     684.5,      -202,       -180,       0.64,       31.021]
DICE_DROP2  = [886,         315,        -202.5,     180,        0.696,      -59]
INT_DICE4   = [886,         315,        -180,       180,        0.696,      -59]
Rotate      = [0, 0, 0, 0, 90]

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
    
Robot_IP = '172.29.209.124'



        

def main():
    
    beaker = robot(Robot_IP)
    beaker.set_speed(200)
    cycles = 1
    beaker.conveyor("stop")
    Conveyor_Forward = False
    beaker.gripper("open")

    while cycles <= 1:
        
        print("--------------------")
        print(f"Cycle: {cycles}/3")
        print("--------------------")

        print("Moving HOME")
        move_robot_joint(beaker, HOME)
        
        print("Position Above Dice")
        move_robot_linear(beaker, INT_Dice1)
        

        print("Press 1 if dice is present to proceed or 0 to return to home position.")
        R_1 = input("Enter 1 if dice is present to proceed or 0 to return home: ")

        if R_1 == "1":
            print("Dice identified...Grabbing Dice")
            move_robot_linear(beaker, Dice_Grab1)
            gripper(beaker,"close",0.1)
            
            #print("Clearance Move")
            move_robot_linear(beaker, INT_DICE2)
            
            #print("Set Dice on Conveyor")
            move_robot_linear(beaker, DICE_DROP1)
            gripper(beaker,"open",0.1)
            
            #print("Clearance Move")
            move_robot_linear(beaker, INT_DICE2)


               #if left_prox:
               # print("Dice identified at right sensor")
               # beaker.conveyor("forward")
                
               # print("Postion above pickup")
               # move_robot_linear(beaker, INT_DICE3)
               
               # while not beaker.conveyor_proximity_sensor("right"):
               #     continue
               # print("Right sensor active, stopping belt")
               # beaker.conveyor("stop")
               # print("belt stopped")
            
            left_prox = beaker.conveyor_proximity_sensor("left")
            if left_prox:
                beaker.conveyor("forward")
                move_robot_linear(beaker, INT_DICE3)
                print("Dice identified at right sensor")
                Conveyor_Forward = True
                #print("Postion above pickup")
                while Conveyor_Forward:
                    right_prox = beaker.conveyor_proximity_sensor("right")
                    if right_prox:
                        beaker.conveyor("stop")
                        print("Dice identified at left sensor")
                        Conveyor_Forward = False
                    else:
                        print("Proximity Sensor Not Triggered")
                
            else:
                print("Proximity Sensor Not Triggered")

            
            
            #print("Grabbing Dice...")        
            move_robot_linear(beaker, Dice_Grab2)
            gripper(beaker,"close",0.1)
            
            print("Clearance Move")
            move_robot_linear(beaker, INT_DICE3)
            
            print("Moving dice to final position")
            move_robot_linear(beaker, INT_Dice1)
            print("Roataion")
            joint_offset(beaker, 6, -90)
            
            print("Dropping dice...")
            move_robot_linear(beaker, DICE_DROP2)
            gripper(beaker,"open",0.1)

            move_robot_linear(beaker, INT_DICE4)
            
            print("Moving HOME")
            move_robot_joint(beaker, HOME)
            break
            

        elif R_1 == "0":
            move_robot_joint(beaker, HOME)
            print("Returning to the home position.")
        else:
            print("Invalid input. Please enter 1 to proceed or 0 to return home.")

        print("--------------------")
        print("Final Position")
        print("--------------------")
        

        cycles += 1

    print("--------------------")
    print("Cycle STOP")
    print("--------------------")

if __name__ == "__main__":
    main()