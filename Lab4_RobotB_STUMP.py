import socket  # Import the Python socket library for network communication
import sys  # Import the sys module (not used in the code)
import time  # Import the time module for time-related functions
import pickle  # Import the pickle module for serializing and deserializing data
import random  # Import the random module for generating random variations
from os.path import dirname # Change Directory to look for relevant functions and information
sys.path.append(dirname(__file__)+"\\src")
from robot_controller import robot  # Import the 'robot' class from the 'robot_controller' module

# Define functions for robot movements and actions
def move_robot_linear(beaker, cartcoords):
    beaker.write_cartesian_position(*cartcoords)  # Set the robot's position using Cartesian coordinates
    beaker.start_robot()  # Start the robot's movement

def move_robot_joint(beaker, jointcoords):
    beaker.set_pose(jointcoords)  # Set the robot's pose using joint coordinates
    beaker.start_robot()  # Start the robot's movement

def joint_offset(beaker, joint, offset):
    beaker.write_joint_offset(joint, offset)  # Adjust the robot's joint offset
    beaker.start_robot()  # Start the robot's movement

def gripper(beaker, position, dwell):
    beaker.schunk_gripper(position)  # Control the gripper to open or close
    if position == "open":
        gripper_status = False  # Set gripper status to open
    if position == "close":
        gripper_status = True  # Set gripper status to close
    time.sleep(dwell)  # Wait for the specified time
    return gripper_status  # Return the gripper status

# Function to transform coordinates from A to B
def Transform_A_to_B(A_coordinates):
    X = A_coordinates[0][0] + 29.75  # Offset X coordinate
    Y = A_coordinates[0][1] + 1431.5  # Offset Y coordinate
    Z = A_coordinates[0][2] + 57.5  # Offset Z coordinate
    W = -A_coordinates[0][3] if A_coordinates[0][3] is not None else None  # Adjust W angle
    P = -A_coordinates[0][4] if A_coordinates[0][4] is not None else None  # Adjust P angle
    R = -A_coordinates[0][5] if A_coordinates[0][5] is not None else None  # Adjust R angle
    offset_data = [X, Y, Z, W, P, R]  # Store the offset data
    return offset_data  # Return the transformed coordinates

# Function to generate random positions
def RandomPOS():
    # Define the base point
    base_x = 600  # X-coordinate base point
    base_y = 900  # Y-coordinate base point
    base_z = 195  # Z-coordinate base point

    # Generate random variations
    x_variation = random.uniform(-50, 50)  # Random X variation between -5 and 5 cm
    y_variation = random.uniform(-50, 50)  # Random Y variation between -5 and 5 cm
    z_variation = random.uniform(-100, 100)  # Random Z variation between -10 and 10 cm

    # Calculate the final position
    random_x = base_x + x_variation  # Calculate the final X coordinate
    random_y = base_y + y_variation  # Calculate the final Y coordinate
    random_z = base_z + z_variation  # Calculate the final Z coordinate

    Random_POS1 = [random_x, random_y, random_z, -90, -30, 0]  # Store the random position
    return Random_POS1  # Return the random position

# Define constant coordinates
HOME = [690, 266, -175, 180, 0, 30]  # Predefined HOME position
Wait = [550, 850, 250, -90, -30, 0]  # Predefined Wait position
Dice_Grab1 = [690, 266, -195, 180, -0.5, 30]  # Predefined Dice_Grab1 position

# Client configuration
server_ip = '172.29.208.124'  # Replace with Robot B's IP address
server_port = 5011  # Replace with the same port number used in the sister program

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (Robot A)
client_socket.connect(('172.29.208.25', server_port))  # Connect to Robot A's IP and port
print(f"Connected to {server_ip}:{server_port}")  # Print a connection message

beaker = robot(server_ip)  # Create a robot object for controlling Robot B
beaker.set_speed(350)  # Set the robot's speed

# Main function for coordination and communication
def main():
    loops = 1  # Initialize a loop counter

    while loops <= 2:  # Repeat the task twice

        gripper(beaker, "open", 1)  # Initialize the gripper in the open position
        move_robot_linear(beaker, HOME)  # Move Robot B to the HOME position
        move_robot_linear(beaker, Wait)  # Move Robot B to the Wait position

        try:
            while True:
                # Receive and deserialize data from Robot A
                data = client_socket.recv(250)  # Receive data from Robot A
                if not data:  # If there is no data, exit the loop
                    break

                received_coordinates = pickle.loads(data)  # Deserialize received data
                Coords = Transform_A_to_B(received_coordinates)  # Transform coordinates
                print(f"Transformed Coord From A: {Coords}")  # Print transformed coordinates
                Coords[1] += -20  # Adjust the Y coordinate
                print(f"INT Coord From A: {Coords}")  # Print the adjusted coordinates
                move_robot_linear(beaker, Coords)  # Move Robot B to the adjusted coordinates
                Coords[1] += 20  # Restore the Y coordinate
                move_robot_linear(beaker, Coords)  # Move Robot B back to the original coordinates
                gripper_status = gripper(beaker, "close", 0.25)  # Close the gripper and get its status
                client_socket.send(pickle.dumps(gripper_status))  # Send the gripper status to Robot A
                time.sleep(0.5)  # Sleep for 0.5 seconds
                move_robot_linear(beaker, HOME)  # Move Robot B back to the HOME position
                move_robot_linear(beaker, Dice_Grab1)  # Move Robot B to Dice_Grab1 position
                gripper(beaker, "open", 0.25)  # Open and close the gripper
                gripper(beaker, "close", 0.25)  
                Random_POS1 = RandomPOS()  # Generate a random position
                move_robot_linear(beaker, Random_POS1)  # Move Robot B to the random position
                client_socket.send(pickle.dumps([Random_POS1]))  # Send the random position to Robot A
                A_Grabbed = False  # Initialize a flag for Robot A's gripper status

                while A_Grabbed == False:
                    try:
                        Gripper_StatusA = client_socket.recv(250)  # Receive gripper status from Robot A
                        if not Gripper_StatusA:  # If there is no status, exit the loop
                            break
                        A_Grabbed = pickle.loads(Gripper_StatusA)  # Deserialize Robot A's gripper status
                    except KeyboardInterrupt:  # Handle a user-initiated interruption
                        print("Client terminated by user")

                gripper(beaker, "open", 0)  # Open the gripper
                Random_POS1[1] += -20  # Adjust the Y coordinate
                move_robot_linear(beaker, Random_POS1)  # Move Robot B to the adjusted position
                move_robot_linear(beaker, HOME)  # Move Robot B back to the HOME position
                loops += 1  # Increment the loop counter

        except KeyboardInterrupt:  # user-initiated interruption
            print("Client terminated by user")

        finally:
            client_socket.close()  # Close the socket connection

if __name__ == "__main__":
    main()  # Start the main function
