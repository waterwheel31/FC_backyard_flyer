import argparse
import time
from enum import Enum

import numpy as np

from udacidrone import Drone
from udacidrone.connection import MavlinkConnection, WebSocketConnection  
from udacidrone.messaging import MsgID


class States(Enum):
    MANUAL = 0
    ARMING = 1
    TAKEOFF = 2
    WAYPOINT = 3
    LANDING = 4
    DISARMING = 5


class BackyardFlyer(Drone):

    def __init__(self, connection):
        super().__init__(connection)
        self.target_position = np.array([10.0, 0.0, 0.0])
        self.all_waypoints = []
        self.in_mission = True
        self.check_state = {}
        self.torrelance_p = 0.05
        

        # initial state
        self.flight_state = States.MANUAL

        self.register_callback(MsgID.LOCAL_POSITION, self.local_position_callback)
        self.register_callback(MsgID.LOCAL_VELOCITY, self.velocity_callback)
        self.register_callback(MsgID.STATE, self.state_callback)

    def local_position_callback(self):
        
        print('local position:', self.local_position)
        
        if abs(self.local_position[0] - self.target_position[0]) < self.torrelance_p and \
           abs(self.local_position[1] - self.target_position[1]) < self.torrelance_p and \
           abs(self.local_position[2]*-1 - self.target_position[2]) < self.torrelance_p:

            print('reached to target position')

            north_t, east_t  = self.target_position[0], self.target_position[1]

            if north_t == 10.0 and east_t == 0.0: 
                self.target_position[0] = 10.0
                self.target_position[1] = 10.0
                self.waypoint_transition()
            elif north_t == 10.0 and east_t == 10.0: 
                self.target_position[0] = 0.0
                self.target_position[1] = 10.0
                self.waypoint_transition()
            elif north_t == 0.0 and east_t == 10.0: 
                self.target_position[0] = 0.0
                self.target_position[1] = 0.0
                self.waypoint_transition()
            elif north_t == 0.0 and east_t == 0.0: 

                self.landing_transition()



    def velocity_callback(self):
        
        if self.flight_state == States.LANDING:
            self.disarming_transition()

    def state_callback(self):
        
        if not self.in_mission:
            return 

        if self.flight_state == States.MANUAL:
            self.arming_transition()
        elif self.flight_state == States.ARMING:
            self.takeoff_transition()
        elif self.flight_state == States.TAKEOFF:
            self.waypoint_transition()
        elif self.flight_state == States.LANDING:
            self.disarming_transition()
        elif self.flight_state == States.DISARMING:
            self.manual_transition()

    def calculate_box(self):
        
        pass

    def arming_transition(self):
        
        self.take_control()
        self.arm()
        self.flight_state = States.ARMING

        print("arming transition")

    def takeoff_transition(self):

        self.target_position[2] = 3.0
        self.takeoff(3.0)
        self.flight_state = States.TAKEOFF

        print("takeoff transition")

    def waypoint_transition(self):
      
        self.cmd_position(*(self.target_position),0 )
        self.flight_state = States.WAYPOINT

        print("waypoint transition")

    def landing_transition(self):
       
        self.land()
        self.flight_state = States.LANDING
        print("landing transition")

    def disarming_transition(self):
      
        self.disarm()
        self.flight_state = States.DISARMING
        
        print("disarm transition")

    def manual_transition(self):
      
        print("manual transition")

        self.release_control()
        self.stop()
        self.in_mission = False
        self.flight_state = States.MANUAL

    def start(self):
        
        print("Creating log file")
        self.start_log("Logs", "NavLog.txt")
        print("starting connection")
        self.connection.start()
        print("Closing log file")
        self.stop_log()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5760, help='Port number')
    parser.add_argument('--host', type=str, default='127.0.0.1', help="host address, i.e. '127.0.0.1'")
    args = parser.parse_args()

    conn = MavlinkConnection('tcp:{0}:{1}'.format(args.host, args.port), threaded=False, PX4=False)
    #conn = WebSocketConnection('ws://{0}:{1}'.format(args.host, args.port))
    drone = BackyardFlyer(conn)
    time.sleep(2)
    drone.start()

    # 

    
