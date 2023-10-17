import socket
import time
from robot_controller import robot
import pickle

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

# Server configuration
server_ip = '172.29.20.123'  # Replace with Robot A's IP address
server_port = 5002 # Replace with your desired port number

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address
server_socket.bind(('', server_port))

# Listen for incoming connections (1 connection at a time)
server_socket.listen(1)
print(f"Server listening on {server_ip}:{server_port}")

# Accept a connection from Robot B
client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address}")

try:
    while True:
        # Receive and deserialize data from Robot B
        data = client_socket.recv(1024)
        if not data:
            break
        
        received_coordinates = pickle.loads(data)
        
        # Process the received coordinates (replace this with your logic)
        for coords in received_coordinates:
            print(f"Received coordinates from Robot B: {coords}")
            

except KeyboardInterrupt:
    print("Server terminated by user")

finally:
    # Close the sockets
    client_socket.close()
    server_socket.close()
