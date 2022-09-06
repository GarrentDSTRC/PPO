import logging
import random
import numpy as np
import torch
import ACAIDataIf
from geographiclib.geodesic import Geodesic

#logger = logging.getLogger(__name__)


class Env():
    def __init__(self):

        self.actions = range(9)  #0-8
        self.size = 9
        self.state = []

        self.acaiif = ACAIDataIf()

    def wait_for_status_update(self):
        self.acaiif.wait_for_status_update()
    def continue_to_do_action(self):
        self.continue_to_do_action()
    def step(self,action):             #action 0-8
        # 系统当前状态
        action
        prevstate
        self.continue_to_do_action()
        self.wait_for_status_update()
        self.getstate()
        reward, Terminal


    def reset(self):
        #self.state = self.states[int(random.random() * len(self.states))]
        self.state=15
        return self.state

    def getstate(self):
        state=[]
        Lon=self.acaiif.ACFlightStatus.lon
        Lat=self.acaiif.ACFlightStatus.lat
        Alt=self.acaiif.ACFlightStatus.alt
        #到四个边界 4X 高度  1X
        state.append(self.acaiif.PKConfig.RightUpLon-Lon)
        state.append(self.acaiif.PKConfig.LeftDownLon - Lon)
        state.append(self.acaiif.PKConfig.RightUpLat - Lat)
        state.append(self.acaiif.PKConfig.LeftDownLat - Lat)
        state.append(Alt-self.acaiif.PKConfig.MinFlyHeight)
        #目标点距离方位 2X
        if self.acaiif.ACFlightStatus.flightTeam==0:
        #red 0 blue 1
            state.append(Lon - self.acaiif.PKConfig.RedMissionLon)
            state.append(Lat - self.acaiif.PKConfig.RedMissionLat)
        else:
            state.append(Lon - self.acaiif.PKConfig.BlueMissionLon)
            state.append(Lat - self.acaiif.PKConfig.BlueMissionLat)
        #速度  3X友方是否生存 1X友方距离方位 3X
        state.append(self.acaiif.ACFlightStatus.velNWU[0],self.acaiif.ACFlightStatus.velNWU[1],self.acaiif.ACFlightStatus.velNWU[2])
        state.append(self.acaiif.COFlightStatus.flightMemCnt-1)

        state.append(Lon - self.acaiif.COFlightStatus.memFlightStatus[0].lon,Lat - self.acaiif.COFlightStatus.memFlightStatus[0].lat,Alt - self.acaiif.COFlightStatus.memFlightStatus[0].alt)
        state.append(Lat - self.acaiif.PKConfig.BlueMissionLat)
        #敌方是否被探测 1x速度 3X方位 2X距离 1X 进入角 1X} * x2
        if self.acaiif.ACRdrTarget.tgtCnt>=1:
            state.append(1,self.acaiif.ACRdrTarget.tgtInfos[0].sbsSpeed,Lon-self.acaiif.ACRdrTarget.tgtInfos[0].lon,Lat-self.acaiif.ACRdrTarget.tgtInfos[0].lat,Alt-self.acaiif.ACRdrTarget.tgtInfos[0].Alt)
            state.append(self.acaiif.ACRdrTarget.tgtInfos[0].slantRange,self.acaiif.ACRdrTarget.tgtInfos[0].aspect)
            if self.acaiif.ACRdrTarget.tgtCnt>1:
                state.append(1,self.acaiif.ACRdrTarget.tgtInfos[1].sbsSpeed,Lon-self.acaiif.ACRdrTarget.tgtInfos[1].lon,Lat-self.acaiif.ACRdrTarget.tgtInfos[1].lat,Alt-self.acaiif.ACRdrTarget.tgtInfos[1].Alt)
                state.append(self.acaiif.ACRdrTarget.tgtInfos[1].slantRange,self.acaiif.ACRdrTarget.tgtInfos[1].aspect)
            else:
                state.append(0,0,0,0,0,0,0,0)
        else:
            state.append(0,0,0,0,0,0,0,0)
            state.append(0,0,0,0,0,0,0,0)
        self.state=torch.tensor(state)
        return self.state

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None