import sys
import time
from FANUCethernetipDriver import readR_Register
from robot_controller import robot

Robot_IP= ''

def main ():
   #position list
    # P[1:HOME]
    X =  1358.619385;   Y =   628.138123;  Z =  -528.780518
    W =   165.444672;   P =    79.211945;  R =  -163.535934 
    Home=[X,Y,Z,W,P,R]
    
    # P[2:INT_DICE1]
    X =  1384.826660;	Y =   822.305420;	Z =  -800.476013;
    W =  -179.089447;   P =    78.491074;	R =  -150.679184;
    INT_Dice1=[X,Y,Z,W,P,R]
    
    # P[6:DICE_GRAB1]
    X =  1384.649170;	Y =   823.763428;	Z =  -830.000000;
    W =  -179.144485;	P =    78.505295;	R =  -150.738312;
    Dice_Grab1=[X,Y,Z,W,P,R]
    
    # P[3:INT_CONV1]
    X =  1373.505127;	Y =  1093.897461;	Z =  -657.433167;
    W =   179.956573;	P =    79.835083;	R =  -153.279144;
    INT_Conv1=[X,Y,Z,W,P,R]
    
    # P[4:INT_CONV2]
    J1=    66.061096;	J2=    12.661455;	J3=   -49.939487; 
    J4=  -182.052795;	J5=    47.565453;	J6=  -216.394882;
    INT_Conv2=[X,Y,Z,W,P,R]
    
    # P[5:TOUCHOFF]                                         
    X =  1379.544434;	Y =   820.394165;	Z =  -861.960754;
    W =   179.047836;	P =    77.626503;	R =  -152.601563;
    TouchOff=[X,Y,Z,W,P,R]
    
    # P[7:DICE_DROP1]
    X =  1373.505127;	Y =  1093.897461;	Z =  -800.000000;
    W =   179.956573;	P =    79.835083;	R =  -153.279144;
    Dice_Drop1=[X,Y,Z,W,P,R]
    
    # P[8:DICE_ROTATE_RETURN]
    X =    45.067261;	Y =  1021.144409;	Z =  -467.579895;
    W =    88.577110;	P =    82.706642;	R =  -153.810410;
    Dice_Rotate_Return=[X,Y,Z,W,P,R]
    
    # P[9:DICE_GRAB2]
    X =   770.885010;	Y =   969.535645;	Z =  -827.562500;
    W =  -145.796127;	P =    77.823456;	R =  -118.574516;
    Dice_Grab2=[X,Y,Z,W,P,R]
    
    # P[10:DICE_DROP2]
    X =    54.686035;	Y =  1024.975708;	Z =  -610.205200;
    W =    87.318657;	P =    82.641441;	R =  -154.531509;
    Dice_Drop2=[X,Y,Z,W,P,R]
    

    
    beaker = robot(Robot_IP)
  
    beaker.set_speed(200)
    cycles =1 

    while(cycles <= 1):
        print("--------------------")
        print(f"Cycle: {cycles}/3")
        print("--------------------")
        

        beaker.conveyor("stop")
        beaker.gripper("open")
        beaker.set_joints_to_home_position()
        beaker.start_robot()
        
        beaker.send_coords(INT_Dice1)
        beaker.start_robot()


        print("Press 1 if dice is present proceed or 0 to return to home position.")
    
    while True:
        R_1 = input("Enter 1  if dice is present to proceed or 0 to return home: ")
        # R_1= readR_Register(1)
        
        if R_1 == "1":
            print("Dice identified...Proceeding with the operation.")
            beaker.send_coords(Dice_Grab1)
            beaker.start_robot()
            
            beaker.gripper("close")
            time.sleep(0.5)

            beaker.send_coords(INT_Conv1)
            beaker.start_robot()
            
            beaker.send_coords(Dice_Drop1)
            beaker.start_robot()
            
            beaker.gripper("open")
            time.sleep(0.5)
            try: 
                R_Prox = beaker.conveyor_proximity_sensor("right")
                L_Prox = beaker.conveyor_proximity_sensor("left")
                if R_Prox and not L_Prox:
                    beaker.conveyor("forward")
                    conveyer_on=True
                    beaker.send_coords(INT_Conv2)
                    beaker.start_robot()
                    time.sleep(0.5)
                elif not L_Prox and R_Prox:
                    beaker.conveyor("stop")
                    conveyer_on=False
                    time.sleep(0.5)
            except:
                beaker.conveyor("stop")
                beaker.send_coords(Home)
                beaker.start_robot()
                
                
            beaker.send_coords(Dice_Grab2)
            beaker.start_robot()
            
            beaker.gripper("close")
            time.sleep(0.5)
            
            beaker.send_coords(INT_Conv2)
            beaker.start_robot()

            beaker.set_pose(Dice_Rotate_Return)
            beaker.start_robot()

            beaker.send_coords(Dice_Drop2)
            beaker.start_robot()

            beaker.gripper("open")
            time.sleep(0.5)
            
            
            break
        elif R_1 == "0":
            beaker.set_joints_to_home_position()
            print("Returning to the home position.")
        else:
            print("Invalid input. Please enter 1 to proceed or 0 to return home.")
        


    
        
        
     
    
    
    
        print("--------------------")
        print("Final Position")
        print("--------------------")
        beaker.read_current_cartesian_position()
        
        cycles += 1
    print("--------------------")
    print("Cycle STOP")
    print("--------------------")
    


if __name__=="__main__":
    main()