from GeneticAlgorithm import GeneticAlgorithm, GeneticAlgorithmData
from NetworkSettings import NetworkSettings
from NetworkSettings import SystemInfo
from RateCalculate import RateCalculateMN, RateCalculateSN
from ProportionalFair import ProportionalFair
import math
import numpy as np
import random
from ValueCalculate import ValueCalculateData, ValueCalculate


class BsProcessData:
    def __init__(self, event_details, event_manager, event_trigger_time, bs_id):
        self.event_details = event_details
        self.event_manager = event_manager
        self.event_trigger_time = event_trigger_time
        self.bs = NetworkSettings.object_info_dict[bs_id]

    def execute(self):
        target_ue = self.event_details['target_ue']
        data_amount = self.event_details['data_amount']
        #print("BsProcessData: receive {} for data with size {}".format(target_ue, data_amount))
        self.bs.add_data_for_ue(target_ue, data_amount, self.event_trigger_time)

class BsSched:
    def __init__(self, event_details, event_manager, bs_id, history_rate):
        self.event_details = event_details
        self.event_manager = event_manager
        self.bs_id = bs_id
        self.bs = NetworkSettings.object_info_dict[bs_id]
        self.current_rate = list()
        self.current_rate_ue_index = list()
        self.history_rate = history_rate
        #self.history_rate = HistoryDate(NetworkSettings.ue_id_list,NetworkSettings.Number_resource_block) #創建儲存過去資料的rate

    def execute(self):
        self.generate_event_to_self()
        #print("SystemInfo.system_time = {} SystemInfo.interval_time = {}".format(SystemInfo.system_time,SystemInfo.interval_time))
        #if SystemInfo.system_time % SystemInfo.interval_time == 0:
        #    self.rate = RateCalculate(bs_id) #所有基地台都會執行sinr計算(但為一個個bs依序執行)
        if self.bs_id == "bs0":
            self.current_rate, self.current_rate_ue_index = RateCalculateMN(self.bs_id).sinr_rate_Calculate()
        else:
            self.current_rate, self.current_rate_ue_index = RateCalculateSN(self.bs_id).sinr_rate_Calculate()
        #print("self.current_rate = ",self.current_rate)
        self.perform_resource_assignment()
        
        return self.history_rate

    def perform_resource_assignment(self): #RB分配
        ue_data = self.bs.queue_for_ue
        #print("ue_data: ", ue_data)
        #print("self.bs_id", self.bs_id)
        #print("self.current_rate: ", self.current_rate)
        allowed_data, self.history_rate = ProportionalFair(self.history_rate, self.current_rate, self.bs_id, ue_data, self.current_rate_ue_index).execute()
        #print("allowed_data: ", allowed_data)
        ue_data_amount = {}
        for ue_id, ue_type_data in allowed_data.items():
            ue_data_amount.setdefault(ue_id, 0)
            for data_type, data_amount in ue_type_data.items():
                if data_amount > 0:
                    ue_data_amount[ue_id] += data_amount
                    self.bs.dec_data_for_ue(ue_id, data_type, data_amount)
                    self.generate_event_to_ue(ue_id, data_amount)

                self.bs.drop_data_for_ue(ue_id, data_type)

        if NetworkSettings.fairness_method == 2:
            self.fairness_calculate(ue_data_amount)

    def fairness_calculate(self, ue_data_amount):
        throughput_sum = 0
        square_throughput_sum = 0
        dc_throughput_sum = 0
        dc_square_throughput_sum = 0
        dc_ue_amount = 0
        mn_throughput_sum = 0
        mn_square_throughput_sum = 0
        mn_ue_amount = 0
        sn_throughput_sum = 0
        sn_square_throughput_sum = 0
        sn_ue_amount = 0

        have_data = False
        dc_have_data = False
        mn_have_data = False
        sn_have_data = False
        for ue_id, data_amount in ue_data_amount.items():
            if data_amount > 0:
                have_data = True
            throughput_sum += data_amount
            square_throughput_sum += (data_amount ** 2)

            if len(NetworkSettings.ue_to_bs_mapping_table[ue_id]) == 2:
                if data_amount > 0:
                    dc_have_data = True
                dc_ue_amount += 1
                dc_throughput_sum += data_amount
                dc_square_throughput_sum += (data_amount ** 2)

                if self.bs_id == "bs0":
                    if data_amount > 0:
                        mn_have_data = True
                    mn_ue_amount += 1
                    mn_throughput_sum += data_amount
                    mn_square_throughput_sum += (data_amount ** 2)
                else:
                    if data_amount > 0:
                        sn_have_data = True
                    sn_ue_amount += 1
                    sn_throughput_sum += data_amount
                    sn_square_throughput_sum += (data_amount ** 2)

        if have_data == True:
            jain_fairness = (throughput_sum ** 2) / (len(ue_data_amount) * square_throughput_sum)
            ValueCalculateData.fairness_list.append(jain_fairness)
        if dc_have_data == True:
            dc_jain_fairness = (dc_throughput_sum ** 2) / (dc_ue_amount * dc_square_throughput_sum)
            ValueCalculateData.dc_fairness_list.append(dc_jain_fairness)
            GeneticAlgorithmData.chromosomes_data["fairness"].append(dc_jain_fairness)
        if mn_have_data == True:
            mn_jain_fairness = (mn_throughput_sum ** 2) / (mn_ue_amount * mn_square_throughput_sum)
            ValueCalculateData.mn_fairness_list.append(mn_jain_fairness)    
        if sn_have_data == True:
            sn_jain_fairness = (sn_throughput_sum ** 2) / (sn_ue_amount * sn_square_throughput_sum)
            ValueCalculateData.sn_fairness_list.append(sn_jain_fairness)    

    def generate_event_to_ue(self, target_ue, data_amount): #傳給UE的data
        event = {
            "event_target": target_ue,
            "event_name": "incoming_downlink_data",
            "event_trigger_time": SystemInfo.system_time + 1,
            "event_details": {
                "data_amount": data_amount
            }
        }
        self.event_manager.add_new_event(event['event_trigger_time'], event)


    def generate_event_to_self(self): #執行schedule
        event = {
            "event_target": self.bs_id,
            "event_name": "schedule",
            "event_trigger_time": SystemInfo.system_time + 1,
            "event_details": {}
        }
        self.event_manager.add_new_event(event['event_trigger_time'], event)


class BaseStation:
    event_handler_dict = {
        "incoming_video_data": BsProcessData, #有接收到TrafficGenetator的incoming_data才會觸發
        "incoming_voice_data": BsProcessData,
        "incoming_CBR_data": BsProcessData,
        "schedule": BsSched
    }

    def __init__(self, bs_id, event_manager):
        self.bs_id = "bs{}".format(bs_id)
        self.event_manager = event_manager
        self.queue_for_ue = dict() #queue_for_ue的每個ue都要再放一個dict
        self.queue_trigger_time = dict()
        self.history_rate = [(10 ** -6) for _ in range(NetworkSettings.num_of_ue)] #創建儲存過去資料的rate
        self.generate_first_event()

    def generate_first_event(self):
        event = {
            "event_target": self.bs_id,
            "event_name": "schedule",
            "event_trigger_time": 1,
            "event_details": {}
        }
        self.event_manager.add_new_event(event['event_trigger_time'], event)

    def event_handler(self, event_content):
        event_name = event_content['event_name']
        if event_name in self.event_handler_dict:
            if event_name == "schedule":
                #print("BS: ", self.bs_id)
                #print("RATE: ", self.history_rate)
                self.history_rate = self.event_handler_dict[event_name](event_content['event_details'], self.event_manager, self.bs_id,self.history_rate).execute()
            else:
                self.event_handler_dict[event_name](event_content['event_details'], self.event_manager, event_content['event_trigger_time'], self.bs_id).execute()
        else:
            print("BaseStation: The {} cannot handle this event {}".format(self.bs_id, event_name))

    #update
    def add_data_for_ue(self,ue_id, data_amount, event_trigger_time):
        if ue_id not in self.queue_for_ue:
            self.queue_for_ue[ue_id] = {"CBR":0,"voice":0,"video":0} #這邊要改成CBR、video、voice
        if ue_id not in self.queue_trigger_time:
            self.queue_trigger_time[ue_id] = {"CBR":[],"voice":[],"video":[]}
        if data_amount == 1460 * 8 : #1460 * 8 = 11680
            self.queue_for_ue[ue_id]['CBR'] += data_amount
            self.queue_trigger_time[ue_id]["CBR"].append(event_trigger_time)
        elif data_amount == 10 * 8: #10 * 8 = 80
            self.queue_for_ue[ue_id]['voice'] += data_amount
            self.queue_trigger_time[ue_id]["voice"].append(event_trigger_time)
        elif data_amount == 1000 * 8:
            self.queue_for_ue[ue_id]['video'] += data_amount
            self.queue_trigger_time[ue_id]["video"].append(event_trigger_time)
    
    #update
    def dec_data_for_ue(self, ue_id, data_type, data_amount):
        type_data_amount_dict = {
            "CBR": (1460 * 8),
            "voice": (10 * 8),
            "video": (1000 * 8)
        }

        self.queue_for_ue[ue_id][data_type] -= data_amount
        ValueCalculate.add_data_amount(self.bs_id, ue_id, data_amount)
        ValueCalculate.add_loss_sent_data(self.bs_id, ue_id, data_type, data_amount)

        if len(NetworkSettings.ue_to_bs_mapping_table[ue_id]) == 2:
            GeneticAlgorithmData.chromosomes_data["throughput"].setdefault(ue_id, 0)
            GeneticAlgorithmData.chromosomes_data["throughput"][ue_id] += data_amount
            GeneticAlgorithmData.chromosomes_data["loss"]["sent_data_amount"] += data_amount
        queue_packets_amount = math.ceil(self.queue_for_ue[ue_id][data_type] / type_data_amount_dict[data_type])
        sent_packets_amount = len(self.queue_trigger_time[ue_id][data_type]) - queue_packets_amount

        for i in range(sent_packets_amount):
            queue_time = SystemInfo.system_time - self.queue_trigger_time[ue_id][data_type][0]
            ValueCalculate.add_delay_data(self.bs_id, ue_id, data_type, queue_time)
            if len(NetworkSettings.ue_to_bs_mapping_table[ue_id]) == 2:
                GeneticAlgorithmData.chromosomes_data["delay"]["data_amount"] += type_data_amount_dict[data_type]
                GeneticAlgorithmData.chromosomes_data["delay"]["queue_time"] += type_data_amount_dict[data_type] * queue_time
            del self.queue_trigger_time[ue_id][data_type][0]

        #print("ue_id {} dec type {} data {} for ue".format(ue_id,data_type,data_amount))

    def drop_data_for_ue(self, ue_id, data_type):
        packet_deadline_dict = {
            "CBR": 300,
            "voice": 100,
            "video": 150
        }
        type_data_amount_dict = {
            "CBR": (1460 * 8),
            "voice": (10 * 8),
            "video": (1000 * 8)
        }

        while len(self.queue_trigger_time[ue_id][data_type]) > 0:
            queue_time = SystemInfo.system_time - self.queue_trigger_time[ue_id][data_type][0]
            if queue_time >= packet_deadline_dict[data_type]:
                del self.queue_trigger_time[ue_id][data_type][0]
                self.queue_for_ue[ue_id][data_type] = type_data_amount_dict[data_type] * len(self.queue_trigger_time[ue_id][data_type])
                ValueCalculate.add_loss_drop_data(self.bs_id, ue_id, data_type)
                if NetworkSettings.delay_method == 2:
                    ValueCalculate.add_delay_data(self.bs_id, ue_id, data_type, queue_time)
                if len(NetworkSettings.ue_to_bs_mapping_table[ue_id]) == 2:
                    GeneticAlgorithmData.chromosomes_data["loss"]["drop_data_amount"] += type_data_amount_dict[data_type]
            else:
                break