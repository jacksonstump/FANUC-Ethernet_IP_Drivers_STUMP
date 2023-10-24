
import socket
import sys
import time
import pickle
import random
from os.path import dirname 
sys.path.append(dirname(__file__)+"\\src")
from robot_controller import robot



def move_robot_linear(beaker, cartcoords):
    beaker.write_cartesian_position(*cartcoords)
    beaker.start_robot()
    
def move_robot_joint(beaker, jointcoords):
    beaker.set_pose(jointcoords)
    beaker.start_robot()
    
def joint_offset(beaker, joint, offset):
    beaker.write_joint_offset(joint, offset)
    beaker.start_robot()
    
def gripper(beaker,position,dwell):
    beaker.schunk_gripper(position)
    if position == "open":
        gripper_status=False
    if position == "close":
        gripper_status=True
    time.sleep(dwell)
    return gripper_status

def Transform_A_to_B(A_coordinates):
    X=A_coordinates[0][0]  + 29.75
    Y=A_coordinates[0][1]  + 1431.5
    Z=A_coordinates[0][2]  + 57.5
    W=-A_coordinates[0][3] if A_coordinates[0][3] is not None else None
    P=-A_coordinates[0][4] if A_coordinates[0][4] is not None else None
    R=-A_coordinates[0][5] if A_coordinates[0][5] is not None else None
    offset_data = [X, Y, Z, W, P, R]
    
    return offset_data

def RandomPOS():
# Define the base point
    base_x = 600  
    base_y = 900 
    base_z = 195  
    
    # Generate random variations
    x_variation = random.uniform(-50, 50)  # Random variation for X between -5 and 5 cm
    y_variation = random.uniform(-50, 50)  # Random variation for Y between -5 and 5 cm
    z_variation = random.uniform(-100, 100)  # Random variation for Z between -10 and 10 cm
    
    # Calculate the final position
    random_x = base_x + x_variation
    random_y = base_y + y_variation
    random_z = base_z + z_variation

    Random_POS1=[random_x,random_y,random_z,-90,-30,0]

    return Random_POS1
    


HOME        = [690, 266, -175, 180,0, 30]    
Wait        = [550, 850,250,-90,-30,0]
Dice_Grab1  = [690, 266, -195, 180,-.5, 30]  



# Client configuration
server_ip =  '172.29.208.124'  # Replace with Robot B's IP address
server_port = 5011  # Replace with the same port number used on Robot A

# Sample list of coordinates      

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (Robot A)
client_socket.connect(('172.29.208.25',server_port))
print(f"Connected to {server_ip}:{server_port}")
beaker = robot(server_ip)
beaker.set_speed(350)

def main():
    loops=1
    
    while(loops <=2):
        
        
        gripper(beaker, "open",1)
        move_robot_linear(beaker,HOME)
        move_robot_linear(beaker,Wait)
        
        try:
            # Serialize and send the coordinates using pickle
            #data_to_send = pickle.dumps([INT_Dice1])
            #client_socket.send(data_to_send)
            #print(f"Sent coordinates to Robot A")
        
            while True:
                # Receive and deserialize data from Robot B
                data = client_socket.recv(250)
                if not data:
                    break
                
                received_coordinates = pickle.loads(data)
                Coords=Transform_A_to_B(received_coordinates)
                print(f"Transformed Coord From A: {Coords}")
                Coords[1]+=-20
                print(f"INT Coord From A: {Coords}")
                move_robot_linear(beaker, Coords)
                Coords[1]+=20
                move_robot_linear(beaker, Coords)
                gripper_status=gripper(beaker,"close",0.25)
                client_socket.send(pickle.dumps(gripper_status))
                time.sleep(0.5)
                move_robot_linear(beaker, HOME)
                move_robot_linear(beaker, Dice_Grab1)
                gripper(beaker,"open",0.25)
                gripper(beaker, "close", 0.25)
                Random_POS1=RandomPOS()
                move_robot_linear(beaker, Random_POS1)
                client_socket.send(pickle.dumps([Random_POS1]))
                A_Grabbed=False
                while A_Grabbed==False:
                    try:  
                        Gripper_StatusA = client_socket.recv(250)
                        if not data:
                            break
                        A_Grabbed=pickle.loads(Gripper_StatusA)
                    except KeyboardInterrupt:
                        print("Client terminated by user")
                gripper(beaker,"open",0)
                Random_POS1[1]+=-20
                move_robot_linear(beaker, Random_POS1)
                move_robot_linear(beaker,HOME)
                loops +=1
        
        except KeyboardInterrupt:
            print("Client terminated by user")
        
        finally:
            # Close the socket
            client_socket.close()

    
if __name__=="__main__":
    main()
