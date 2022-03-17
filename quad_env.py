import gym
from gym import spaces
import quadcopter,gui,controller
import numpy as np
import signal
import sys

#PARAMS
TIME_SCALING = 1.0 # Any positive number(Smaller is faster). 1.0->Real Time, 0.0->Run as fast as possible
QUAD_DYNAMICS_UPDATE = 0.002 # seconds
CONTROLLER_DYNAMICS_UPDATE = 0.005 # seconds
GOALS = [(1,1,4),(1,-1,4)]
YAWS = [0,3.14,-1.54,1.54]
# Define the quadcopters
QUADCOPTER={'q1':{'position':[1,0,4],'orientation':[0,0,0],'L':0.3,'r':0.1,'prop_size':[10,4.5],'weight':1.2}}
# Controller parameters
CONTROLLER_PARAMETERS = {'Motor_limits':[4000,9000],
                    'Tilt_limits':[-10,10],
                    'Yaw_Control_Limits':[-900,900],
                    'Z_XY_offset':500,
                    'Linear_PID':{'P':[300,300,7000],'I':[0.04,0.04,4.5],'D':[450,450,5000]},
                    'Linear_To_Angular_Scaler':[1,1,0],
                    'Yaw_Rate_Scaler':0.18,
                    'Angular_PID':{'P':[22000,22000,1500],'I':[0,0,1.2],'D':[12000,12000,0]},
                    }


class DroneEnv(gym.Env):
    def __init__(self):
        super(DroneEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.motor_limits=CONTROLLER_PARAMETERS["Motor_limits"]
        self.action_space = spaces.Box(low=self.motor_limits[0], high=self.motor_limits[1], shape=())
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Tuple(spaces.Box(low=None, high=None , shape=(3)),
                                              spaces.Box(low= -np.pi, high=np.pi , shape=(3)),
                                              spaces.Box(low=None, high=None , shape=(3)),
                                              spaces.Box(low=None, high=None , shape=(3)))
        
        
        self.quad=quadcopter.Quadcopter(QUADCOPTER)
        self.gui_object = gui.GUI(quads=QUADCOPTER)
        self.ctrl = controller.Controller_PID_Point2Point(self.quad.get_state,self.quad.get_time, self.quad.set_motor_speeds,params=CONTROLLER_PARAMETERS,quad_identifier='q1')
        self.gui_object.quads['q1']['position'] = self.quad.get_position('q1')
        self.gui_object.quads['q1']['orientation'] = self.quad.get_orientation('q1')
        
    def step(self, action):
        # self.ctrl.update()
        self.quad.set_motor_speeds(action)
        self.quad.update(dt=QUAD_DYNAMICS_UPDATE)
        observation=self.quad.get_state()
        
        reward=10
    
        if self.quad.stop_thread()==False:
            done=True
        info = {}
        return observation, reward, done, info
    
    def reset(self):
        self.done = False
        self.quad.reset()
        observation=self.quad.get_state()
        return observation  # reward, done, info can't be included
    
    def render(self, mode='human'):
        print(f"GOAL: {GOALS} POS: {self.quad.get_position('q1')}")
        self.gui_object.update()
        return None
    
    