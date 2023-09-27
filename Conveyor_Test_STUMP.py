import sys
import time
from turtle import left
from robot_controller import robot

Robot_IP = '172.29.209.124'

def main():
    
    beaker = robot(Robot_IP)
    beaker.set_speed(100)
    cycles = 1
    beaker.conveyor("stop")
    Conveyor_Forward = False
    beaker.gripper("open")

    while cycles <= 1:
        right_prox = beaker.conveyor_proximity_sensor("right")
        left_prox = beaker.conveyor_proximity_sensor("left")
        if left_prox:
              print("Dice identified at right sensor")
              beaker.conveyor("forward")
              Conveyor_Forward = True
        
        else:
              print("Proximity Sensor Not Triggered")
        
        while Conveyor_Forward:
            right_prox = beaker.conveyor_proximity_sensor("right")
            left_prox = beaker.conveyor_proximity_sensor("left")
            if right_prox:
                   print("Dice identified at left sensor")
                   beaker.conveyor("stop")
                   Conveyor_Forward = False

        cycles += 1

    print("--------------------")
    print("Cycle STOP")
    print("--------------------")

if __name__ == "__main__":
    main()