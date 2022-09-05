from ctypes import *
import mmap

class PKConfig(Structure):
    '''
    /// \struct 比赛配置信息
    struct PKConfig
    {
        double	MinFlyHeight	;//最小飞行高度(m)
        double  MaxFlyHeight	;//最大飞行高度(m)
        double  LeftDownLon		;//矩形左下角经度(rad)
        double  LeftDownLat		;//矩形左下角纬度(rad)
        double  RightUpLon		;//矩形右上角经度(rad)
        double	RightUpLat		;//矩形右上角纬度(rad)
        double  RedMissionLon	;//红方任务目标点经度(rad)
        double  RedMissionLat	;//红方任务目标点纬度(rad)
        double  BlueMissionLon	;//蓝方任务目标点经度(rad)
        double  BlueMissionLat	;//蓝方任务目标点纬度(rad)
    };
    '''
    _fields_=[('MinFlyHeight',c_double),
              ('MaxFlyHeight',c_double),
              ('LeftDownLon', c_double),
              ('LeftDownLat', c_double),
              ('RightUpLon', c_double),
              ('RightUpLat', c_double),
              ('RedMissionLon', c_double),
              ('RedMissionLat', c_double),
              ('BlueMissionLon', c_double),
              ('BlueMissionLat', c_double)]
class ACFlightStatus(Structure):
    '''
    /// \struct 飞机状态数据
    struct ACFlightStatus
    {
        unsigned long timeCounter;            ///< 时标(ms)
        unsigned int simuSpeed;               ///< 仿真倍速
        unsigned int flightID;                ///< 飞机编号(唯一标识)
        FLIGHT_TEAM flightTeam;               ///< 飞机阵营 \sa FLIGHT_TEAM
        FLIGHT_ROLE flightRole;               ///< 飞机角色 \sa FLIGHT_ROLE
        double lon;                           ///< 经度(rad)
        double lat;                           ///< 纬度(rad)
        double alt;                           ///< 海拔高度(m)
        double heading;                       ///< 航向角(rad 顺时针为正)
        double pitch;                         ///< 俯仰角(rad 上为正)
        double roll;                          ///< 横滚角(rad 右为正)
        double groundSpeed;                   ///< 地速(m/s)
        double machSpeed;                     ///< 马赫数(mach)
        double velNWU[3];                     ///< 地理系速度矢量(m/s)
        double overLoad;                      ///< 当前过载G
        bool isLinkSysAvailable;              ///< 数据链挂载状态(是否可用)
        bool isRdrSysAvailable;               ///< 雷达挂载状态(是否可用)
        bool isEwsSysAvailable;               ///< 电子战挂载状态(是否可用)
        bool isLinkSysOpen;                   ///< 数据链开机状态
        bool isRdrSysOpen;                    ///< 雷达开机状态
        bool isEwsSysOpen;                    ///< 电子战开机状态
        double maxRdrRange;                   ///< 雷达最大作用距离(m)
        double maxRdrAzAngle;                 ///< 雷达框架角(rad)
        unsigned int remainGuideNum;          ///< 剩余制导资源
        unsigned int remainWpnNum;            ///< 剩余武器数量
    };
    '''
    _fields_=[('timeCounter',c_ulong),
              ('simuSpeed',c_uint),
              ('flightID', c_uint),
              ('flightTeam', c_int),
              ('flightRole', c_int),
              ('lon', c_double),
              ('lat', c_double),
              ('alt', c_double),
              ('heading', c_double),
              ('pitch', c_double),
              ('roll', c_double),
              ('groundSpeed', c_double),
              ('machSpeed', c_double),
              ('velNWU', c_double*3),
              ('overLoad', c_double),
              ('isLinkSysAvailable', c_bool),
              ('isRdrSysAvailable', c_bool),
              ('isEwsSysAvailable', c_bool),
              ('isLinkSysOpen', c_bool),
              ('isRdrSysOpen', c_bool),
              ('isEwsSysOpen', c_bool),
              ('maxRdrRange', c_double),
              ('maxRdrAzAngle', c_double),
              ('remainGuideNum', c_uint),
              ('remainWpnNum', c_uint)]

class ACRdrTarget(Structure):
    '''
    /// \struct 雷达探测目标
    struct ACRdrTarget
    {
        unsigned long timeCounter; ///< 时标
        unsigned int flightID;     ///< 飞机编号(唯一标识)
        unsigned int tgtCnt;       ///< 目标数量(<=MAX_RDR_TGT_NUM)
        /// \struct 雷达目标信息
        struct RdrTgtInfo {
            unsigned int tgtID; ///< 目标编号(目标飞机编号)
            bool rngValid;      ///< 距离有效性
            bool velValid;      ///< 速度有效性
            bool angValid;      ///< 角度有效性
            double lon;         ///< 经度(rad)
            double lat;         ///< 纬度(rad)
            double alt;         ///< 海拔高度(m)
            double slantRange;  ///< 目标斜距(m)
            double velNWU[3];   ///< 地理系速度矢量(m/s)
            double sbsSpeed;    ///< 目标速度大小(m/s)
            double machSpeed;   ///< 目标马赫速(mac)
            double heading;     ///< 目标航向角(rad 顺时针为正)
            double aspect;      ///< 目标进入角(rad)
            double azGeo;       ///< 目标地理系方位(rad 右为正)
            double elGeo;       ///< 目标地理系俯仰(rad 上为正)
            double azBody;      ///< 目标机体系方位(rad 右为正)
            double elBody;      ///< 目标机体系俯仰(rad 上为正)
        } tgtInfos[MAX_RDR_TGT_NUM]; ///< 目标信息
    };
    '''

    class RdrTgtInfo(Structure):
        _fields_ = [('tgtID', c_uint),
                    ('rngValid', c_bool),
                    ('velValid', c_bool),
                    ('angValid', c_bool),
                    ('lon', c_double),
                    ('lat', c_double),
                    ('alt', c_double),
                    ('slantRange', c_double),
                    ('velNWU', c_double * 3),
                    ('sbsSpeed', c_double),
                    ('machSpeed', c_double),
                    ('heading', c_double),
                    ('aspect', c_double),
                    ('azGeo', c_double),
                    ('elGeo', c_double),
                    ('azBody', c_double),
                    ('elBody', c_double)]
    _fields_ = [('timeCounter', c_ulong),
                ('flightID', c_uint),
                ('tgtCnt', c_uint),
                ('tgtInfos', RdrTgtInfo*31)]

class ACEwsTarget(Structure):
    '''
    /// \struct 电子战探测目标
    struct ACEwsTarget
    {
        unsigned long timeCounter; ///< 时标
        unsigned int flightID;     ///< 飞机编号(唯一标识)
        unsigned int tgtCnt;       ///< 目标数量(<=MAX_EWS_TGT_NUM)
        /// \struct 电子战目标信息
        struct EwsTgtInfo {
            unsigned int tgtID; ///< 目标编号(目标的飞机编号)
            bool angValid;      ///< 角度有效性
            double azGeo;       ///< 目标地理系方位(rad 右为正)
            double azBody;      ///< 目标机体系方位(rad 右为正)
        } tgtInfos[MAX_EWS_TGT_NUM]; ///< 目标信息
    };
    '''
    class EwsTgtInfo(Structure):
        _fields_ = [('tgtID', c_uint),
                    ('angValid', c_bool),
                    ('azGeo', c_double),
                    ('azBody', c_double)]

    _fields_ = [('timeCounter', c_ulong),
                ('flightID', c_uint),
                ('tgtCnt', c_uint),
                ('tgtInfos', EwsTgtInfo*31)]

class ACMslWarning(Structure):
    '''
        /// \struct 导弹威胁告警
    struct ACMslWarning
    {
        unsigned long timeCounter; ///< 时标
        unsigned int flightID;     ///< 飞机编号(唯一标识)
        unsigned int mslCnt;       ///< 导弹数量(<=MAX_MSL_NUM)
        /// \struct 威胁导弹信息
        struct ThreatMslInfo {
            bool angValid; ///< 角度有效性
            double azGeo;  ///< 导弹地理系方位(rad 右为正)
            double azBody; ///< 导弹机体系方位(rad 右为正)
        } threatInfos[MAX_MSL_NUM]; ///< 威胁导弹信息
    };
    '''
    class ThreatMslInfo(Structure):
        _fields_ = [('angValid', c_bool),
                    ('azGeo', c_double),
                    ('azBody', c_double)]

    _fields_ = [('timeCounter', c_int),
                ('flightID', c_uint),
                ('mslCnt', c_uint),
                ('threatInfos', ThreatMslInfo*80)]


class ACFCCStatus(Structure):
    '''
    /// \struct 发射火控包线
    struct ACFCCStatus
    {
        unsigned long timeCounter; ///< 时标
        unsigned int flightID;     ///< 飞机编号(唯一标识)
        unsigned int tgtCnt;       ///< 目标数量(<=MAX_SHOOT_LIST_NUM)
        /// \struct 火控包线信息
        struct FccEnvInfo {
            unsigned int tgtID; ///< 目标编号
            bool isNTSTgt;      ///< 是否NTS目标
            bool shootFlag;     ///< 发射提示符
            double slantRange;  ///< 目标斜距(m)
            double aspect;      ///< 目标进入角(rad)
            double Rmax;        ///< 攻击包线Rmax(m)（假设导弹发射后目标不机动，导弹的最大攻击距离）
            double Rtr;         ///< 攻击包线Rtr(m)（假设导弹发射后目标水平置尾，导弹的最大攻击距离）
            bool APoleValid;    ///< A极有效性（A极表示导弹发射预计能够截获目标）
            bool FPoleValid;    ///< F极有效性（A极表示导弹发射预计能够命中目标）
            double APoleTime;   ///< A极时间（预计截获目标的时间）
            double FPoleTime;   ///< F极时间（预计命中目标的时间）
            double APoleRange;  ///< A极距离（预计截获目标时刻的载机和目标距离）
            double FPoleRange;  ///< F极距离（预计命中目标时刻的载机和目标距离）
            double FoeRmax;     ///< 敌包线Rmax(m)（假设敌方导弹发射后本机不机动，导弹的最大攻击距离）
            double FoeRtr;      ///< 敌包线Rtr(m)（假设敌方导弹发射后本机不机动，导弹的最大攻击距离）
        } envInfos[MAX_SHOOT_LIST_NUM]; ///< 火控包线信息
    };
    '''
    class FccEnvInfo(Structure):
        _fields_ = [('tgtID', c_uint),
                    ('isNTSTgt', c_bool),
                    ('shootFlag', c_bool),
                    ('slantRange', c_double),
                    ('aspect', c_double),
                    ('Rmax', c_double),
                    ('Rtr', c_double),
                    ('APoleValid', c_bool),
                    ('FPoleValid', c_bool),
                    ('APoleTime', c_double),
                    ('FPoleTime', c_double),
                    ('APoleRange', c_double),
                    ('FPoleRange', c_double),
                    ('FoeRmax', c_double),
                    ('FoeRtr', c_double)]
    _fields_=[('timeCounter',c_ulong),
              ('flightID',c_uint),
              ('tgtCnt', c_uint),
              ('envInfos', FccEnvInfo*31)]

class ACMSLInGuide(Structure):
    '''
    /// \struct 制导武器信息
    struct ACMSLInGuide
    {
        unsigned long timeCounter;  ///< 时标
        unsigned long lostCounter;  ///< 丢帧计数
        unsigned int guideFlightID; ///< 制导机编号
        unsigned int mslCnt;        ///< 导弹数量(<=MAX_GUIDE_MSL_NUM)
        /// \struct 制导武器信息
        struct GuideMslInfo {
            unsigned int launchFlightID; ///< 发射机编号
            unsigned int mslStaIndex;    ///< 导弹挂点下标
            unsigned int mslLockedTgtID; ///< 导弹锁定目标编号
            unsigned int mslLostCounter; ///< 导弹丢失计数
            double mslGuideRange;        ///< 导弹制导距离(m)
            double mslGuideAz;           ///< 导弹制导方位(rad)
            bool isGuideCmdValid;        ///< 制导指令有效性
        } guideInfos[MAX_GUIDE_MSL_NUM]; ///< 制导武器信息
    };
    '''
    class GuideMslInfo(Structure):
        _fields_ = [('launchFlightID', c_uint),
                    ('mslStaIndex', c_uint),
                    ('mslLockedTgtID', c_uint),
                    ('mslLostCounter', c_uint),
                    ('mslGuideRange', c_double),
                    ('mslGuideAz', c_double),
                    ('isGuideCmdValid', c_bool)]

    _fields_ = [('timeCounter', c_ulong),
                ('lostCounter', c_ulong),
                ('guideFlightID', c_uint),
                ('mslCnt', c_uint),
                ('guideInfos', GuideMslInfo*8)]
class TeamMSLLaunched(Structure):
    '''
        /// \struct 编队发射导弹实时信息
    struct TeamMSLLaunched
    {
        unsigned long timeCounter; ///< 时标
        unsigned int mslCnt;       ///< 导弹数量(<=MAX_MSL_NUM)
        /// \struct 导弹弹道信息
        struct MslTrajectoryInfo {
            unsigned int launchFlightID; ///< 发射机编号
            unsigned int mslStaIndex;    ///< 导弹挂点下标
            unsigned int mslLockedTgtID; ///< 导弹锁定目标编号
            double lon;                  ///< 导弹经度(rad)
            double lat;                  ///< 导弹纬度(rad)
            double alt;                  ///< 导弹海拔高度(m)
            double velNWU[3];            ///< 地理系速度矢量(m/s)
            double flyTime;              ///< 导弹已飞时间(s)
            double remainTime;           ///< 导弹剩余飞行时间(s)
            bool isSeekerCaptured;       ///< 导引头是否截获
            bool APoleValid;             ///< A极有效性
            bool FPoleValid;             ///< F极有效性
            double APoleTime;            ///< A极时间(s)
            double FPoleTime;            ///< F极时间(s)
            double APoleRange;           ///< A极距离(m)
            double FPoleRange;           ///< F极距离(m)
        } trajectoryInfos[MAX_MSL_NUM]; ///< 导弹弹道信息
    };
    '''
    class MslTrajectoryInfo(Structure):
        _fields_ = [('launchFlightID', c_uint),
                    ('mslStaIndex', c_uint),
                    ('mslLockedTgtID', c_uint),
                    ('lon', c_double),
                    ('lat', c_double),
                    ('alt', c_double),
                    ('velNWU', c_double * 3),
                    ('flyTime', c_double),
                    ('remainTime', c_double),
                    ('isSeekerCaptured', c_bool),
                    ('APoleValid', c_bool),
                    ('FPoleValid', c_bool),
                    ('APoleTime', c_double),
                    ('FPoleTime', c_double),
                    ('APoleRange', c_double),
                    ('FPoleRange', c_double)]
    _fields_ = [('timeCounter', c_ulong),
                ('mslCnt', c_uint),
                ('trajectoryInfos', MslTrajectoryInfo*80)]

class COFlightStatus(Structure):
    '''
    /// \struct 编队成员飞机状态数据
    struct COFlightStatus
    {
        unsigned int flightMemCnt; ///< 飞机成员数
        ACFlightStatus memFlightStatus[MAX_FLIGHT_NUM]; ///< 成员飞机状态数据信息
    };
    '''
    _fields_ = [('flightMemCnt', c_uint),
                ('memFlightStatus', ACFlightStatus*32)]

class CORdrTarget(Structure):
    '''
    /// \struct 编队成员雷达探测目标
    struct CORdrTarget
    {
        unsigned int flightMemCnt; ///< 飞机成员数
        ACRdrTarget memRdrTarget[MAX_FLIGHT_NUM]; ///< 成员雷达探测目标信息
    };
    '''
    _fields_ = [('flightMemCnt', c_uint),
                ('memRdrTarget', ACRdrTarget*32)]


class COEwsTarget(Structure):
    '''
    /// \struct 编队成员电子战探测目标
    struct COEwsTarget
    {
        unsigned int flightMemCnt; ///< 飞机成员数
        ACEwsTarget memEwsTarget[MAX_FLIGHT_NUM]; ///< 成员电子战探测目标信息
    };
    '''
    _fields_ = [('flightMemCnt', c_uint),
                ('memEwsTarget', ACEwsTarget*32)]

class COMslWarning(Structure):
    '''
    /// \struct 编队成员电子战导弹告警
    struct COMslWarning
    {
        unsigned int flightMemCnt; ///< 飞机成员数
        ACMslWarning memMslWarning[MAX_FLIGHT_NUM]; ///< 成员电子战导弹告警信息
    };
    '''
    _fields_ = [('flightMemCnt', c_uint),
                ('memMslWarning', ACMslWarning*32)]

class COFCCStatus(Structure):
    '''
    /// \struct 编队成员发射火控包线
    struct COFCCStatus
    {
        unsigned int flightMemCnt; ///< 飞机成员数
        ACFCCStatus memFCCStatus[MAX_FLIGHT_NUM]; ///< 成员发射火控包线信息
    };
    '''
    _fields_ = [('flightMemCnt', c_uint),
                ('memFCCStatus', ACFCCStatus*32)]

class COMSLInGuide(Structure):
    '''
    /// \struct 编队成员制导武器信息
    struct COMSLInGuide
    {
        unsigned int flightMemCnt; ///< 飞机成员数
        ACMSLInGuide memMSLInGuide[MAX_FLIGHT_NUM]; ///< 成员制导武器信息信息
    };
    '''
    _fields_ = [('flightMemCnt', c_uint),
                ('memMSLInGuide', ACMSLInGuide*32)]

class ACAIStatus(Structure):
    '''
    struct {
		ACAI::PKConfig mPKConfig;               ///< 比赛配置信息 \sa ACAI::PKConfig
		ACAI::ACFlightStatus mACFlightStatus;   ///< 本机飞机状态数据 \sa ACAI::ACFlightStatus
		ACAI::ACRdrTarget mACRdrTarget;         ///< 本机雷达探测目标 \sa ACAI::ACRdrTarget
		ACAI::ACEwsTarget mACEwsTarget;         ///< 本机电子战探测目标 \sa ACAI::ACEwsTarget
		ACAI::ACMslWarning mACMslWarning;       ///< 本机导弹威胁告警 \sa ACAI::ACMslWarning
		ACAI::ACFCCStatus mACFCCStatus;         ///< 本机发射火控包线 \sa ACAI::ACFCCStatus
		ACAI::ACMSLInGuide mACMSLInGuide;       ///< 本机制导武器信息 \sa ACAI::ACMSLInGuide
		ACAI::TeamMSLLaunched mTeamMSLLaunched; ///< 编队发射导弹实时信息 \sa ACAI::TeamMSLLaunched
		ACAI::COFlightStatus mCOFlightStatus;   ///< 编队成员飞机状态数据 \sa ACAI::COFlightStatus
		ACAI::CORdrTarget mCORdrTarget;         ///< 编队成员雷达探测目标 \sa ACAI::CORdrTarget
		ACAI::COEwsTarget mCOEwsTarget;         ///< 编队成员电子战探测目标 \sa ACAI::COEwsTarget
		ACAI::COMslWarning mCOMslWarning;       ///< 编队成员电子战导弹告警 \sa ACAI::COMslWarning
		ACAI::COFCCStatus mCOFCCStatus;         ///< 编队成员发射火控包线 \sa ACAI::COFCCStatus
		ACAI::COMSLInGuide mCOMSLInGuide;       ///< 编队成员制导武器信息 \sa ACAI::COMSLInGuide
		//ACAI::InTeamDataBag mCOTeamDataBag;     ///< 编队成员编队内部数据包 \sa ACAI::InTeamDataBag
	}data_if;
    '''
    _fields_ = [('mPKConfig', PKConfig),
                ('mACFlightStatus', ACFlightStatus),
                ('mACRdrTarget', ACRdrTarget),
                ('mACEwsTarget', ACEwsTarget),
                ('mACMslWarning', ACMslWarning),
                ('mACFCCStatus', ACFCCStatus),
                ('mACMSLInGuide', ACMSLInGuide),
                ('mTeamMSLLaunched', TeamMSLLaunched),
                ('mCOFlightStatus', COFlightStatus),
                ('mCORdrTarget', CORdrTarget),
                ('mCOEwsTarget', COEwsTarget),
                ('mCOMslWarning', COMslWarning),
                ('mCOFCCStatus', COFCCStatus),
                ('mCOMSLInGuide', COMSLInGuide)]


class ACAIDataIf:
    def __init__(self):
        self.status=ACAIStatus()
        self.status_size = sizeof(self.status)#345016
        EVENT_ALL_ACCESS = 0x000F0000 | 0x00100000 | 0x3
        self.shm = mmap.mmap(0, self.status_size, "shared_memory")
        self.m_hEvent1 = windll.kernel32.OpenEventW(EVENT_ALL_ACCESS, True, "statusUpdateEvent")
        self.m_hEvent2 = windll.kernel32.OpenEventW(EVENT_ALL_ACCESS, True, "actionUpdateEvent")
        if (self.m_hEvent1 and self.m_hEvent2):
            pass
        else:
            print("同步事件打开失败")
            return None

        '''
         data=ACAIDataIf()

         print(sizeof(data))
         print(sizeof(data.mPKConfig))
         print(sizeof(data.mACFlightStatus))
         print(sizeof(data.mACRdrTarget))
         print(sizeof(data.mACEwsTarget))
         print(sizeof(data.mACMslWarning))
         print(sizeof(data.mACFCCStatus))
         print(sizeof(data.mACMSLInGuide))
         print(sizeof(data.mTeamMSLLaunched))
         print(sizeof(data.mCOFlightStatus))
         print(sizeof(data.mCORdrTarget))
         print(sizeof(data.mCOEwsTarget))
         print(sizeof(data.mCOMslWarning))
         print(sizeof(data.mCOFCCStatus))
         print(sizeof(data.mCOMSLInGuide))
         '''

    def wait_for_status_update(self):
        windll.kernel32.WaitForSingleObject(self.m_hEvent1, -1)
        self.shm.seek(0)
        memmove(addressof(self.status), bytes(self.shm.read(self.status_size)), self.status_size);
    def continue_to_do_action(self):
        windll.kernel32.SetEvent(self.m_hEvent2)
        #memmmove action

import time
if __name__ == '__main__':
    #example
    acaiif=ACAIDataIf()
    if(acaiif):
        while True:
            acaiif.wait_for_status_update()


            #do some trainning and choose policy.....
            print((acaiif.status.mACFlightStatus.lat,acaiif.status.mACFlightStatus.lon))
            #time.sleep(1)
            #......



            acaiif.continue_to_do_action()
