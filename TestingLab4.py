import socket
import sys
import time
import pickle
import sys
import time
from os.path import dirname 
sys.path.append(dirname(__file__)+"\\src")
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


# Client configuration
server_ip =  '172.29.208.124'  # Replace with Robot B's IP address
server_port = 5007  # Replace with the same port number used on Robot A

# Sample list of coordinates      

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (Robot A)
client_socket.connect(('172.29.208.25',server_port))
print(f"Connected to {server_ip}:{server_port}")


try:
    # Serialize and send the coordinates using pickle
    #data_to_send = pickle.dumps([INT_Dice1])
    #client_socket.send(data_to_send)
    #print(f"Sent coordinates to Robot A")


        client_socket.send(pickle.dumps([INT_Dice1]))



except KeyboardInterrupt:
    print("Client terminated by user")

finally:
    # Close the socket
    client_socket.close()
