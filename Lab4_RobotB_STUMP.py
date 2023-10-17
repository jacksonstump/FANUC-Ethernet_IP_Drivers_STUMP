
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

def Transform_A_to_B(A_coordinates):


    #A_coordinates=Received_coord[0]
    X=A_coordinates[0][0]
    Y=A_coordinates[0][1]
    Z=A_coordinates[0][2]
    W=-A_coordinates[0][3] if A_coordinates[0][3] is not None else None
    P=-A_coordinates[0][4] if A_coordinates[0][4] is not None else None
    R=-A_coordinates[0][5] if A_coordinates[0][5] is not None else None
    X_off=X+23
    Y_off=Y +23
    Z_off=Z+23
    offset_data = [X_off, Y_off, Z_off, W, P, R]
    
    return offset_data
    
INT_Dice1   = [825.267,     351.151,    -180,       -179.286,   0.64,       31.021]    

# Client configuration
server_ip =  '172.29.208.124'  # Replace with Robot B's IP address
server_port = 5003  # Replace with the same port number used on Robot A

# Sample list of coordinates      

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (Robot A)
client_socket.connect(('172.29.208.25',server_port))
print(f"Connected to {server_ip}:{server_port}")

beaker = robot(server_ip)
beaker.set_speed(300)
beaker.gripper("open")

try:
    # Serialize and send the coordinates using pickle
    #data_to_send = pickle.dumps([INT_Dice1])
    #client_socket.send(data_to_send)
    #print(f"Sent coordinates to Robot A")

    while True:
        # Receive and deserialize data from Robot B
        data = client_socket.recv(1024)
        if not data:
            break
        
        received_coordinates = pickle.loads(data)
        
        # Process the received coordinates (replace this with your logic)
        for coords in received_coordinates:
            print("{coords}")
            print(f"Received coordinates from Robot A: {coords}")
            print(type(received_coordinates))
            #move_robot_linear(beaker, Coords)
    
    Coords=Transform_A_to_B(received_coordinates)
    print(f"Transformed Coord From A: {Coords}")
    move_robot_linear(beaker, cartcoords)



except KeyboardInterrupt:
    print("Client terminated by user")

finally:
    # Close the socket
    client_socket.close()
