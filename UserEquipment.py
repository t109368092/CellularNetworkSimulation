import random
from TrafficGenerator import TrafficGenerator
from NetworkSettings import NetworkSettings


class UeProcessData:
    def __init__(self, event_details, event_manager, ue_id):
        self.event_details = event_details
        self.event_manager = event_manager
        self.ue = NetworkSettings.object_info_dict[ue_id]
        
    def execute(self):
        received_amount = self.event_details['data_amount']
        self.ue.add_received_data_amount(received_amount)


class UserEquipment:
    event_handler_dict = {
        "incoming_downlink_data": UeProcessData,
    }

    def __init__(self, ue_id, event_manager):
        self.received_data_amount = 0
        self.ue_id = "ue{}".format(ue_id)
        self.event_manager = event_manager
        data_type = ['voice','video','CBR']
        for i in range(len(data_type)):
            tg_id = self.ue_id + "{}".format(data_type[i])
            tg = TrafficGenerator(self.ue_id, tg_id, event_manager)
            NetworkSettings.object_info_dict[tg_id] = tg

    def event_handler(self, event_content):
        event_name = event_content['event_name']
        if event_name in self.event_handler_dict:
            self.event_handler_dict[event_name](event_content['event_details'], self.event_manager, self.ue_id).execute()
        else:
            print("The {} cannot handle this event {}".format(self.ue_id, event_name))

    def add_received_data_amount(self, data_amount):
        self.received_data_amount += data_amount
