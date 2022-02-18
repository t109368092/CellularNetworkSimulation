import numpy as np
import math
import random
from NetworkSettings import NetworkSettings

class RateCalculateMN:
    def __init__(self,bs_id):
        self.bs_id = bs_id
        self.mapping_table = NetworkSettings.ue_to_bs_mapping_table
        self.distance = NetworkSettings.bs_ue_distance #儲存距離
        self.frequency = NetworkSettings.mn_center_frequency #中心頻率
        self.BS_antenna_gain = NetworkSettings.BS_antenna_gain
        self.UE_antenna_gain = NetworkSettings.UE_antenna_gain
        self.Thermal_noise = NetworkSettings.Thermal_noise_dbm
        self.bandwidth = NetworkSettings.mn_system_bandwidth
        self.BS_power = NetworkSettings.mn_transmission_power
        self.Number_resource_block = NetworkSettings.Number_resource_block

    def sinr_rate_Calculate(self): #https://ir.nctu.edu.tw/bitstream/11536/72785/1/025601.pdf
        need_pathloss = list() #https://www.electronics-notes.com/articles/antennas-propagation/propagation-overview/free-space-path-loss.php
        need_received_power = list()
        sinr = list()
        current_rate_ue_index = list()
        noise_power = self.Thermal_noise + 10 * np.log10(self.bandwidth * (10 ** 6)) #dbm thermal noise power
        noise_power = 10 ** ((noise_power-30)/10) #Watt thermal noise power
        #print("self.distance = ",self.distance)
        for ue_id, map_bs in self.mapping_table.items(): #這個pathloss已經生成該bs下所有ue的pathloss了
            ue_index = NetworkSettings.ue_id_list.index(ue_id) #所有ue的位置
            for bs_index in range(len(map_bs)):
                if map_bs[bs_index] == self.bs_id:
                    need_pathloss.append(20 * np.log10(self.distance[ue_id][bs_index]/1000) + 20 * np.log10(self.frequency) + 32.44 - self.BS_antenna_gain - self.UE_antenna_gain)
                    current_rate_ue_index.append(ue_index)
        #print("need_pathloss = ",need_pathloss) #這個pathloss包含 該bs下的ue所有連接到其餘bs的path loss
        #print("interference_pathloss = ",interference_pathloss)
        for i in range(len(need_pathloss)):
            need_received_power.append(self.BS_power - need_pathloss[i] - 2.15) #dbm = dbm + db
            need_received_power[i] = 10 **((need_received_power[i]-30)/10) # bs下ue的接收power Watt

        need_index = 0
        for ue_id,map_bs in self.mapping_table.items():
            if self.bs_id in map_bs:
                sinr.append(need_received_power[need_index] / noise_power)
                need_index = need_index + 1 

        sinr_db = 10 * np.log10(sinr) #np.array
        sinr_numpy = np.asarray(sinr)
        rate = self.bandwidth* (10 ** 6) * np.log2(1 + sinr_numpy) #因為sinr為負值 沒有data rate 收不到訊號
        rate_mpbs_sec = rate * (10**-6)
        rb_rate_ms = rate_mpbs_sec / 1000 / self.Number_resource_block

        #print("ue_rate_mbps = ",rate_mpbs_sec)
        #print("rb_rate_mbp_ms = ",rb_rate_ms)
        #print("bs_id = ",self.bs_id)
        #print("sinr = ",sinr_numpy)
        #print("sinr_db = ",sinr_db)
        #print("self.mapping_table",self.mapping_table)

        return rb_rate_ms, current_rate_ue_index


class RateCalculateSN:
    def __init__(self,bs_id):
        self.bs_id = bs_id
        self.mapping_table = NetworkSettings.ue_to_bs_mapping_table
        self.distance = NetworkSettings.bs_ue_distance #儲存距離
        self.frequency = NetworkSettings.sn_center_frequency #中心頻率
        self.BS_antenna_gain = NetworkSettings.BS_antenna_gain
        self.UE_antenna_gain = NetworkSettings.UE_antenna_gain
        self.Thermal_noise = NetworkSettings.Thermal_noise_dbm
        self.bandwidth = NetworkSettings.sn_system_bandwidth
        self.BS_power = NetworkSettings.sn_transmission_power
        self.Number_resource_block = NetworkSettings.Number_resource_block

    def sinr_rate_Calculate(self): #https://ir.nctu.edu.tw/bitstream/11536/72785/1/025601.pdf
        need_pathloss = list() #https://www.electronics-notes.com/articles/antennas-propagation/propagation-overview/free-space-path-loss.php
        need_received_power = list()
        sinr = list()
        current_rate_ue_index = list()
        noise_power = self.Thermal_noise + 10 * np.log10(self.bandwidth * (10 ** 6)) #dbm thermal noise power
        noise_power = 10 ** ((noise_power-30)/10) #Watt thermal noise power
        #print("self.distance = ",self.distance)
        for ue_id, map_bs in self.mapping_table.items(): #這個pathloss已經生成該bs下所有ue的pathloss了
            ue_index = NetworkSettings.ue_id_list.index(ue_id) #所有ue的位置
            for bs_index in range(len(map_bs)):
                if map_bs[bs_index] == self.bs_id:
                    need_pathloss.append(20 * np.log10(self.distance[ue_id][bs_index]/1000) + 20 * np.log10(self.frequency) + 32.44 - self.BS_antenna_gain - self.UE_antenna_gain)
                    current_rate_ue_index.append(ue_index)
        #print("need_pathloss = ",need_pathloss) #這個pathloss包含 該bs下的ue所有連接到其餘bs的path loss
        #print("interference_pathloss = ",interference_pathloss)
        
        for i in range(len(need_pathloss)):
            need_received_power.append(self.BS_power - need_pathloss[i] - 2.15) #dbm = dbm + db
            need_received_power[i] = 10 **((need_received_power[i]-30)/10) # bs下ue的接收power Watt

        need_index = 0
        for ue_id,map_bs in self.mapping_table.items():
            if self.bs_id in map_bs:
                sinr.append(need_received_power[need_index] / noise_power)
                need_index = need_index + 1 

        sinr_db = 10 * np.log10(sinr) #np.array
        sinr_numpy = np.asarray(sinr)
        rate = self.bandwidth* (10 ** 6) * np.log2(1 + sinr_numpy) #因為sinr為負值 沒有data rate 收不到訊號
        rate_mpbs_sec = rate * (10**-6)
        rb_rate_ms = rate_mpbs_sec / 1000 / self.Number_resource_block

        #print("ue_rate_mbps = ",rate_mpbs_sec)
        #print("rb_rate_mbp_ms = ",rb_rate_ms)
        #print("bs_id = ",self.bs_id)
        #print("sinr = ",sinr_numpy)
        #print("sinr_db = ",sinr_db)
        #print("self.mapping_table",self.mapping_table)

        return rb_rate_ms, current_rate_ue_index