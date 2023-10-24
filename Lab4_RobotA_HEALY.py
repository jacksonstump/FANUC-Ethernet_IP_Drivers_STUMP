# Script setup
import sys
import socket
import time
import random
from os.path import dirname
sys.path.append(dirname(__file__) + "\\FANUC-Ethernet_IP_Drivers\src")
from robot_controller import robot
import pickle

# Server configuration
server_ip = ''
server_port = 5011

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address
server_socket.bind((server_ip, server_port))

# Listen for incoming connections (1 connection at a time)
server_socket.listen(1)
print(f"Server listening on {server_ip}: {server_port}")

# Accept a connection from Robot B
client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address}")

ip = '172.29.208.123' #Bunsen ip

# Pose list (joint coords)
pose1 = [30.915, 28.212, -39.464, -0.907, -51.638, -0.294]
pose2 = [30.915, 32.111, -45.944, -1.003, -45.159, -0.149]

# Offsets for coordinate transformation between robots
B_x_offset = 30
B_y_offset = 1431.5
B_z_offset = 55

# Generates random coordinates
def randX():
    randX = 570+random.randrange(-50, 50)
    return randX

def randY():
    randY = -520+random.randrange(-50, 50)
    return randY

def randZ():
    randZ = 135+random.randrange(-100, 100)
    return randZ

# Saving lines with a quick move function
def move(pose, delay):
    crx10.write_joint_pose(pose)
    crx10.start_robot()
    time.sleep(delay)
    
# Coordinate transformation from one robot to the other
def coord_transform(coords):
    new_coords = [0, 0, 0, 0, 0, 0]
    new_coords[0] = coords[0] - B_x_offset
    new_coords[1] = coords[1] - B_y_offset
    new_coords[2] = coords[2] - B_z_offset
    new_coords[3] = -coords[3]
    new_coords[4] = -coords[4]
    new_coords[5] = coords[5]
    return new_coords

"""
Actions
"""

# Define robot and speed. Set to starting position
crx10 = robot(ip)
crx10.set_speed(350)
crx10.schunk_gripper('open')
move(pose1, 0)
cycles = 1

while cycles <= 2:
    # repeat the loop
    cycles += 1

    B_grabbed = False
    A_grabbed = False    

    # Pick up die and move to random location, then read coordinates
    move(pose2, 0)
    crx10.schunk_gripper('close')
    time.sleep(0.4)
    crx10.write_cartesian_position(randX(), randY(), randZ(), 90, 30, 0)
    crx10.start_robot()
    coords = crx10.CurCartesianPosList[2:8]
    
    # Send coordinates to robot B
    try:
        data_to_send = pickle.dumps([coords])
        client_socket.send(data_to_send)
        print("Sent coordinates to Robot A")
    
    except KeyboardInterrupt:
        print("Server terminated by user")
        
    # Wait for robot B to signal that it has the die
    while B_grabbed == False:
        try:
            data = client_socket.recv(250)
            if not data:
                break
            B_grabbed = pickle.loads(data)
            
        except KeyboardInterrupt:
            print("Server terminated by user")
    
    # Open the gripper and move back
    crx10.schunk_gripper('open')
    crx10.write_robot_connection_bit(0)
    crx10.write_cartesian_position(coords[0], coords[1]+100, coords[2], 90, 30, 0)
    crx10.start_robot()
    
    # Wait for robot B to send new coordinates; receive them
    coords = [0, 0, 0, 0, 0, 0]
    received_coordinates = coords
    while received_coordinates == [0, 0, 0, 0, 0, 0]:
        try:
            data = client_socket.recv(250)
            if not data:
                break
            received_coordinates = pickle.loads(data)
            
        except KeyboardInterrupt:
            print("Server terminated by user")
            
    # transform received coordinates and move to them, grabbing the die
    new_coords = coord_transform(received_coordinates[0])
    crx10.write_cartesian_position(new_coords[0], new_coords[1]+50, new_coords[2], 90, 30, 0)
    crx10.start_robot()      
    crx10.write_cartesian_position(new_coords[0], new_coords[1], new_coords[2], 90, 30, 0)
    crx10.start_robot()
    crx10.schunk_gripper('close')
    time.sleep(0.4)
    
    # signal to robot B that die is in gripper
    A_grabbed = True
    try:
        data_to_send = pickle.dumps(A_grabbed)
        client_socket.send(data_to_send)
        print("Sent coordinates to Robot A")
    
    except KeyboardInterrupt:
        print("Server terminated by user")
    time.sleep(0.4)
    
    # place die back in original position; return to mounting position
    move(pose1, 0)
    move(pose2, 0)
    crx10.schunk_gripper('open')
    time.sleep(0.4)
    move(pose1, 0)

# close socket connection
client_socket.close()
server_socket.close()