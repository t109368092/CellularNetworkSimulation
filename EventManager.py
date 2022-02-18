from queue import PriorityQueue
from NetworkSettings import NetworkSettings
from NetworkSettings import SystemInfo
from StatisticWork import StatisticWork
import random
from GeneticAlgorithm import GeneticAlgorithm, GeneticAlgorithmData, GAParameters


class EventManagerGA:
    def __init__(self):
        self.event_list = PriorityQueue()
        #將事件 設定為優先順序佇列 
    def execute(self):
        GeneticAlgorithm.chromosomes_generate()
        GeneticAlgorithm.change_current_chromosome()
        #print(GeneticAlgorithmData.current_chromosome)
        chromosome_change_time = 0
        show_time = 0
        while self.event_list.qsize() > 0 and SystemInfo.system_time < NetworkSettings.simulation_time: #事件不為空 and 模擬時間未到
            if SystemInfo.system_time - show_time >= 100:
                print("System Time: ", SystemInfo.system_time)
                show_time = SystemInfo.system_time
            event = self.event_list.get()
            event_content = event[2]
            SystemInfo.system_time = event_content['event_trigger_time']
            if SystemInfo.system_time - chromosome_change_time >= GAParameters.chromosome_run_time:
                GeneticAlgorithm.save_data_to_buffer()
                GeneticAlgorithm.change_current_chromosome()
                #print(GeneticAlgorithmData.current_chromosome)
                chromosome_change_time = SystemInfo.system_time
            #print ("EventManager: current_system_time: {}, event_content: {}".format(event_content['event_trigger_time'], event_content))
            if type(event_content['event_target']) is list: #單一ue複數bs(list)
                for value in range(len(event_content['event_target'])):
                    #print("NetworkSettings.object_info_dict[event_content['event_target'][value]] = ",NetworkSettings.object_info_dict[event_content['event_target'][value]])
                    NetworkSettings.object_info_dict[event_content['event_target'][value]].event_handler(event_content)
            else: #單一ue 單一bs
                NetworkSettings.object_info_dict[event_content['event_target']].event_handler(event_content)
        StatisticWork().execute()

    def add_new_event(self, event_time, event_content):
        self.event_list.put((event_time, SystemInfo.event_priority, event_content))
        SystemInfo.event_priority += 1
        #print("EventManager: insert event ", event_content)


class EventManagerFifty:
    def __init__(self):
        self.event_list = PriorityQueue()
        #將事件 設定為優先順序佇列 
    def execute(self):
        show_time = 0
        while self.event_list.qsize() > 0 and SystemInfo.system_time < NetworkSettings.simulation_time: #事件不為空 and 模擬時間未到
            if SystemInfo.system_time - show_time >= 100:
                print("System Time: ", SystemInfo.system_time)
                show_time = SystemInfo.system_time
            event = self.event_list.get()
            event_content = event[2]
            SystemInfo.system_time = event_content['event_trigger_time']
            #print ("EventManager: current_system_time: {}, event_content: {}".format(event_content['event_trigger_time'], event_content))
            
            if type(event_content['event_target']) is list: #單一ue複數bs(list)
                for value in range(len(event_content['event_target'])):
                    #print("NetworkSettings.object_info_dict[event_content['event_target'][value]] = ",NetworkSettings.object_info_dict[event_content['event_target'][value]])
                    NetworkSettings.object_info_dict[event_content['event_target'][value]].event_handler(event_content)
            else: #單一ue 單一bs
                NetworkSettings.object_info_dict[event_content['event_target']].event_handler(event_content)
        StatisticWork().execute()

    def add_new_event(self, event_time, event_content):
        self.event_list.put((event_time, SystemInfo.event_priority, event_content))
        SystemInfo.event_priority += 1
        #print("EventManager: insert event ", event_content)