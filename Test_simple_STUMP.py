from pickle import FALSE, TRUE
import sys
import time

from robot_controller import robot

Robot_IP= '172.29.209.124'


def main ():
    # P[1:HOME]
    J1=    0;	J2=    0;	J3=   0; 
    J4=    0;	J5=  -90;	J6=  30;
    HOME=[J1,J2,J3,J4,J5,J6]

    # P[2:INT_DICE1]
    X =  825.267;	Y =   351.151;	Z =  -180;
    W =  -179.286;	P =    0.64;	R =  31.021;
    INT_Dice1=[X,Y,Z,W,P,R]
    
    # P[3:Dice_Grab1]
    X =  825.267;	Y =   351.151;	Z =  -202.474;
    W =  -179.286;	P =    0.64;	R =  31.021;
    Dice_Grab1=[X,Y,Z,W,P,R]

    # P[4:INT_DICE2]
    X =  803.57;	Y =  668.72;	Z =  0;
    W =   -179.286;	P =    0.64;	R =  31.021;
    INT_DICE2=[X,Y,Z,W,P,R]

    # P[5:DICE_DROP1]
    X =  803.57;	Y =  668.72;	Z =  -201.963;
    W =   -179.286;	P =    0.64;	R =  31.021;
    DICE_DROP1=[X,Y,Z,W,P,R]
    ## P[6:DICE_DROP1]
    #X =  803.57;	Y =  668.72;	Z =  0;
    #W =   -179.286;	P =    0.64;	R =  31.021;
    #Dice_Drop1=[X,Y,Z,W,P,R]


    


    beaker = robot(Robot_IP)
  
    beaker.set_speed(100)
    cycles =1 

    while(cycles <= 1):
        print("--------------------")
        print(f"Cycle: {cycles}/3")
        print("--------------------")
        

        beaker.conveyor("stop")
        Conveyor_Forward=False
        beaker.gripper("open")

        beaker.set_pose(HOME)
        beaker.start_robot()

        beaker.send_coords(INT_Dice1[0],INT_Dice1[1], INT_Dice1[2], INT_Dice1[3], INT_Dice1[4], INT_Dice1[5])
        beaker.start_robot()

        print("Press 1 if dice is present proceed or 0 to return to home position.")
    
        R_1 = input("Enter 1  if dice is present to proceed or 0 to return home: ")   
        if R_1 == "1":
            print("Dice identified...Proceeding with the operation.")
            beaker.send_coords(Dice_Grab1[0],Dice_Grab1[1], Dice_Grab1[2], Dice_Grab1[3], Dice_Grab1[4], Dice_Grab1[5])
            beaker.start_robot()
            
            beaker.gripper("close")
            time.sleep(0.5)
            
            beaker.send_coords(INT_DICE2[0],INT_DICE2[1], INT_DICE2[2], INT_DICE2[3], INT_DICE2[4], INT_DICE2[5])
            beaker.start_robot()

            beaker.send_coords(DICE_DROP1[0],DICE_DROP1[1], DICE_DROP1[2], DICE_DROP1[3], DICE_DROP1[4], DICE_DROP1[5])
            beaker.start_robot()

            beaker.gripper("open")
            time.sleep(0.5)

            beaker.send_coords(INT_DICE2[0],INT_DICE2[1], INT_DICE2[2], INT_DICE2[3], INT_DICE2[4], INT_DICE2[5])
            beaker.start_robot()

            #right_prox=beaker.conveyor_proximity_sensor("right")
            #left_prox=beaker.conveyor_proximity_sensor("left")

            #if right_prox and not left_prox:
            #    beaker.conveyor("forward")
            #    Conveyor_Forward= True
            #    time.sleep(0.5)
            #else:
            #    print("Start Proximity Sensor Not Triggered")
            #while Conveyor_Forward is True:
            #    beaker.send_coords(INT_DICE3[0],INT_DICE3[1], INT_DICE3[2], INT_DICE3[3], INT_DICE3[4], INT_DICE[5])
            #    beaker.start_robot()
            #    if left_prox and not right_prox:
            #        beaker.conveyor("stop")
            #        Conveyor_Forward= False
            #        time.sleep(0.5)
            #    else:
            #        print("Stop...Proximity Sensor Not Triggered")
            #        beaker.conveyor("stop")





        elif R_1 == "0":
            beaker.set_pose(HOME)
            beaker.start_robot()
            print("Returning to the home position.")
        else:
            print("Invalid input. Please enter 1 to proceed or 0 to return home.")

        print("--------------------")
        print("Final Position")
        print("--------------------")
        beaker.read_current_joint_position()
        
        cycles += 1
    print("--------------------")
    print("Cycle STOP")
    print("--------------------")
    


if __name__=="__main__":
    main()