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

        self.myflight=2
        self.enemyflight=2

        self.acaiif = ACAIDataIf()
        if self.acaiif.status.mACFlightStatus.flightTeam==0:
            #red 0 blue 1
                self.TLon=self.acaiif.status.mPKConfig.RedMissionLon
                self.TLat=self.acaiif.status.mPKConfig.RedMissionLat
        else:
                self.TLon= self.acaiif.status.mPKConfig.BlueMissionLon
                self.TLat= self.acaiif.status.mPKConfig.BlueMissionLat

    def wait_for_status_update(self):
        self.acaiif.wait_for_status_update()
    def continue_to_do_action(self):
        self.continue_to_do_action()
    def step(self,action):             #action 0-8
        # 系统当前状态
        self.acaiif.action.choose(int(action))
        #prevstate=self.state
        self.continue_to_do_action()
        self.wait_for_status_update()
        self.state=self.getstate()
        reward=0
        Terminal=0
        if int(action)==8:
           reward-=35
        for event in self.acaiif.check_event():
            if(self.acaiif.EVENT_PKSTART==event.type):
                pass
            elif(self.acaiif.EVENT_PKEND==event.type):
                Terminal=1
                if self.enemyflight==0 or (np.abs(self.state[5])+np.abs(self.state[6]))<0.1 or (np.abs(self.state[11]-self.TLon)+np.abs(self.state[12]-self.TLat))<0.1:
                    reward+=100
                else: reward-=100
            elif(self.acaiif.EVENT_PKOUT==event.type):
                if self.acaiif.event.flightID==self.acaiif.status.mCOFlightStatus.memFlightStatus[0].flightID:
                    reward-=40
                    self.myflight-=1
                elif self.acaiif.event.flightID==self.acaiif.status.mACFlightStatus.flightID:
                    reward-=50
                    self.myflight-=1
                else:
                    reward+=40
                    self.enemyflight-=1
        #目标距离reward
        reward+=1*(0.5)**(np.abs(self.state[5])+np.abs(self.state[6]))
        return self.state,reward, Terminal

    def reset(self):
        #self.state = self.states[int(random.random() * len(self.states))]
        self.state=15
        return self.state

    def getstate(self):
        state=[]
        Lon=self.acaiif.status.mACFlightStatus.lon
        Lat=self.acaiif.status.mACFlightStatus.lat
        Alt=self.acaiif.status.mACFlightStatus.alt
        #到四个边界 4X 高度  1X
        state.append(self.acaiif.status.mPKConfig.RightUpLon-Lon)
        state.append(self.acaiif.status.mPKConfig.LeftDownLon - Lon)
        state.append(self.acaiif.status.mPKConfig.RightUpLat - Lat)
        state.append(self.acaiif.status.mPKConfig.LeftDownLat - Lat)
        state.append(Alt-self.acaiif.status.mPKConfig.MinFlyHeight)
        #目标点距离方位 2X

        state.append(Lon - self.TLon)
        state.append(Lat - self.TLat)
        #速度  3X友方是否生存 1X友方距离方位 3X
        state.append(self.acaiif.status.mACFlightStatus.velNWU[0],self.acaiif.status.mACFlightStatus.velNWU[1],self.acaiif.status.mACFlightStatus.velNWU[2])
        state.append(self.acaiif.status.mCOFlightStatus.flightMemCnt-1)
        state.append(Lon - self.acaiif.status.mCOFlightStatus.memFlightStatus[0].lon,Lat - self.acaiif.status.mCOFlightStatus.memFlightStatus[0].lat,Alt - self.acaiif.status.mCOFlightStatus.memFlightStatus[0].alt)
        state.append(Lat - self.acaiif.status.mPKConfig.BlueMissionLat)

        #敌方是否被探测 1x速度 3X方位 2X距离 1X 进入角 1X} * x2
        if self.acaiif.status.mACRdrTarget.tgtCnt>=1:
            state.append(1,self.acaiif.status.mACRdrTarget.tgtInfos[0].sbsSpeed,Lon-self.acaiif.status.mACRdrTarget.tgtInfos[0].lon,Lat-self.acaiif.status.mACRdrTarget.tgtInfos[0].lat,Alt-self.acaiif.status.mACRdrTarget.tgtInfos[0].Alt)
            state.append(self.acaiif.status.mACRdrTarget.tgtInfos[0].slantRange,self.acaiif.status.mACRdrTarget.tgtInfos[0].aspect)
            if self.acaiif.ACRdrTarget.tgtCnt>1:
                state.append(1,self.acaiif.status.mACRdrTarget.tgtInfos[1].sbsSpeed,Lon-self.acaiif.status.mACRdrTarget.tgtInfos[1].lon,Lat-self.acaiif.status.mACRdrTarget.tgtInfos[1].lat,Alt-self.acaiif.status.mACRdrTarget.tgtInfos[1].Alt)
                state.append(self.acaiif.status.mACRdrTarget.tgtInfos[1].slantRange,self.acaiif.status.mACRdrTarget.tgtInfos[1].aspect)
            else:
                state.append(0,0,0,0,0,0,0,0)
        else:
            state.append(0,0,0,0,0,0,0,0)
            state.append(0,0,0,0,0,0,0,0)
        #导弹是否雷达告警 1X 导弹方位  1X
        state.append(self.acaiif.status.mACMslWarning.mslCnt,self.acaiif.status.mACMslWarning.threatInfos[0].azBody)

        self.state=torch.tensor(state)
        return self.state

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None