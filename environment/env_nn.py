import logging
import random
import numpy as np
import torch
import ACAIDataIf
#from geographiclib.geodesic import Geodesic

#logger = logging.getLogger(__name__)


class Env():
    def __init__(self):

        self.actions = range(9)  #0-8
        self.size = 9
        self.state = []

        self.myflight=2
        self.enemyflight=2
        self.count=0
        self.acaiif = ACAIDataIf.ACAIDataIf()
        self.running_flag = False


    def wait_for_status_update(self):
        self.acaiif.wait_for_status_update()
    def continue_to_do_action(self):
        self.acaiif.continue_to_do_action()   
    def step(self,action):             #action 0-8
        # 系统当前状态
        self.acaiif.action.choose(int(action))
        #prevstate=self.state
        self.continue_to_do_action()   
        self.wait_for_status_update()
        self.state=self.getstate()
        reward=0
        Terminal=0
        self.count+=1
        if int(action)==8:
            if self.acaiif.status.mACFCCStatus.envInfos[0].FPoleValid==1:
                reward+=0.5
                pass
            else:
                reward-=0.2
                pass
        for event in self.acaiif.check_event():
            if(self.acaiif.EVENT_PKSTART==event.type):
                pass
                #print("开始")
                self.running_flag=True
            elif(self.acaiif.EVENT_PKEND==event.type):
                #print("结束")
                if self.running_flag==True:
                    self.terminalcount=0
                    Terminal=1
                    if self.enemyflight==0 or (np.abs(self.state[5])+np.abs(self.state[6]))<0.01 or (np.abs(self.state[11]-self.TLon)+np.abs(self.state[12]-self.TLat))<0.01:
                        reward+=50
                        print("win")
                    else:
                        reward-=50
                        print("loss")
                    self.running_flag = False
            elif(self.acaiif.EVENT_PKOUT==event.type):
                if self.acaiif.event.flightID==self.acaiif.status.mCOFlightStatus.memFlightStatus[0].flightID:
                    reward-=4
                    self.myflight-=1
                    print("Friend die")
                elif self.acaiif.event.flightID==self.acaiif.status.mACFlightStatus.flightID:
                    reward-=5
                    self.myflight-=1
                    print("I die")
                else:
                    reward+=8
                    print("PKoutEnemy")
                    self.enemyflight-=1
        #目标距离reward
        #reward+=0.01*(0.01)**(np.abs(self.state[5])+np.abs(self.state[6]))
        reward+=0.001*np.log10(self.count)
        #print(self.enemyflight, np.abs(self.state[5])+np.abs(self.state[6]), np.abs(self.state[11]-self.TLon)+np.abs(self.state[12]-self.TLat))
        #print("live reward",0.001*np.log10(self.count))
        #print("到目标",self.state[5],self.state[6],"distance_reward",0.1*(0.5)**(np.abs(self.state[5])+np.abs(self.state[6])))
        return self.state,reward, Terminal

    def reset(self):
        #self.state = self.states[int(random.random() * len(self.states))]
        self.state=15
        return self.state

    def getstate(self):
        state=[]
        #经纬高边界
        EnvUpLon=self.acaiif.status.mPKConfig.RightUpLon
        EnvUpLat=self.acaiif.status.mPKConfig.RightUpLat
        EnvDownLon = self.acaiif.status.mPKConfig.LeftDownLon
        EnvDownLat = self.acaiif.status.mPKConfig.LeftDownLat
        MaxFlyHeight = self.acaiif.status.mPKConfig.MaxFlyHeight
        MinFlyHeight = self.acaiif.status.mPKConfig.MinFlyHeight
        self.EnvLonrange = EnvUpLon-EnvDownLon
        self.EnvLatrange = EnvUpLat - EnvDownLat
        self.EnvHeightrange = MaxFlyHeight-MinFlyHeight
        #本机经纬高
        Lon=self.acaiif.status.mACFlightStatus.lon
        Lat=self.acaiif.status.mACFlightStatus.lat
        Alt=self.acaiif.status.mACFlightStatus.alt

        if self.acaiif.status.mACFlightStatus.flightTeam==0:
            #red 0 blue 1
                self.TLon=(EnvUpLon-self.acaiif.status.mPKConfig.RedMissionLon)/self.EnvLonrange
                self.TLat=(EnvUpLat-self.acaiif.status.mPKConfig.RedMissionLat)/self.EnvLatrange
        else:
                self.TLon= (EnvUpLon-self.acaiif.status.mPKConfig.BlueMissionLon)/self.EnvLonrange
                self.TLat= (EnvUpLat-self.acaiif.status.mPKConfig.BlueMissionLat)/self.EnvLatrange

        #print("target",self.TLon,self.TLat)
        #print("lON LAT ALT",Lon,Lat,Alt)
        #到四个边界 4X 高度  1X
        state.append((EnvUpLon-Lon)/self.EnvLonrange)
        state.append((EnvDownLon-Lon)/self.EnvLonrange)
        state.append((EnvUpLat-Lat)/self.EnvLatrange)
        state.append((EnvDownLat-Lat)/self.EnvLatrange)
        state.append((Alt-MinFlyHeight)/self.EnvHeightrange)
        #目标点距离方位 2X  7
        state.append((EnvUpLon-Lon)/self.EnvLonrange- self.TLon)
        state.append((EnvUpLat-Lat)/self.EnvLatrange - self.TLat)
        #速度  3X友方是否生存 1X友方方位 3X 14
        state.append(self.acaiif.status.mACFlightStatus.velNWU[0])
        state.append(self.acaiif.status.mACFlightStatus.velNWU[1])
        state.append(self.acaiif.status.mACFlightStatus.velNWU[2])
        state.append(self.acaiif.status.mCOFlightStatus.flightMemCnt)
        state.append((EnvUpLon-self.acaiif.status.mCOFlightStatus.memFlightStatus[0].lon)/self.EnvLonrange)
        state.append((EnvUpLat-self.acaiif.status.mCOFlightStatus.memFlightStatus[0].lat)/self.EnvLatrange)
        state.append((self.acaiif.status.mCOFlightStatus.memFlightStatus[0].alt-MinFlyHeight)/self.EnvHeightrange)

        #敌方是否被探测 1x速度 3X方位 2X距离 1X 进入角 1X} * x2
        if self.acaiif.status.mACRdrTarget.tgtCnt>=1:
            state.append(1)
            state.append(self.acaiif.status.mACRdrTarget.tgtInfos[0].sbsSpeed)
            state.append((Lon-self.acaiif.status.mACRdrTarget.tgtInfos[0].lon)/self.EnvLonrange)
            state.append((Lat-self.acaiif.status.mACRdrTarget.tgtInfos[0].lat)/self.EnvLatrange)
            state.append((Alt-self.acaiif.status.mACRdrTarget.tgtInfos[0].alt)/self.EnvHeightrange)
            state.append(self.acaiif.status.mACRdrTarget.tgtInfos[0].slantRange)
            state.append(self.acaiif.status.mACRdrTarget.tgtInfos[0].aspect)
            if self.acaiif.status.mACRdrTarget.tgtCnt>1:
                state.append(1)
                state.append(self.acaiif.status.mACRdrTarget.tgtInfos[1].sbsSpeed)
                state.append((Lon-self.acaiif.status.mACRdrTarget.tgtInfos[0].lon)/self.EnvLonrange)
                state.append((Lat-self.acaiif.status.mACRdrTarget.tgtInfos[0].lat)/self.EnvLatrange)
                state.append((Alt-self.acaiif.status.mACRdrTarget.tgtInfos[0].alt)/self.EnvHeightrange)
                state.append(self.acaiif.status.mACRdrTarget.tgtInfos[1].slantRange)
                state.append(self.acaiif.status.mACRdrTarget.tgtInfos[1].aspect)
            else:
                for k in range(7):
                    state.append(0)
        else:
            for k in range(14):
                    state.append(0)
        #导弹是否雷达告警 1X 导弹方位  1X
        state.append(self.acaiif.status.mACMslWarning.mslCnt)
        state.append(self.acaiif.status.mACMslWarning.threatInfos[0].azBody)
        #print(self.acaiif.status.mACRdrTarget.tgtInfos[0].lon)
        #print("yujing fangwei youfangweidu",self.acaiif.status.mACMslWarning.mslCnt,self.acaiif.status.mACMslWarning.threatInfos[0].azBody,self.acaiif.status.mCOFlightStatus.memFlightStatus[0].lon)

        self.state=torch.tensor(state)
        return self.state

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None