from NetworkSettings import NetworkSettings, SystemInfo, Simulation
import numpy as np
import math
import cmath

#update
class ValueCalculateData:
    total_ue_data = {} #{"ue0": 10, "ue1": 20}
    dc_ue_data = {}
    mn_ue_data = {}
    sn_ue_data = {}
    mn_delay_data = {"CBR": {"data_amount": 0, "queue_time": 0}, "voice": {"data_amount": 0, "queue_time": 0}, "video": {"data_amount": 0, "queue_time": 0}}
    sn_delay_data = {"CBR": {"data_amount": 0, "queue_time": 0}, "voice": {"data_amount": 0, "queue_time": 0}, "video": {"data_amount": 0, "queue_time": 0}}
    mn_loss_data = {"CBR": {"drop_data_amount": 0, "sent_data_amount": 0}, "voice": {"drop_data_amount": 0, "sent_data_amount": 0}, "video": {"drop_data_amount": 0, "sent_data_amount": 0}}
    sn_loss_data = {"CBR": {"drop_data_amount": 0, "sent_data_amount": 0}, "voice": {"drop_data_amount": 0, "sent_data_amount": 0}, "video": {"drop_data_amount": 0, "sent_data_amount": 0}}

    system_throughput = 0
    mn_throughput = 0
    sn_throughput = 0
    avg_ue_throughput = 0
    dc_avg_ue_throughput = 0

    fairness = 0
    dc_fairness = 0
    mn_fairness = 0
    sn_fairness = 0
    fairness_list = []
    dc_fairness_list = []
    mn_fairness_list = []
    sn_fairness_list = []

    mn_cbr_delay = 0
    mn_voice_delay = 0
    mn_video_delay = 0
    mn_avg_delay = 0
    sn_cbr_delay = 0
    sn_voice_delay = 0
    sn_video_delay = 0
    sn_avg_delay = 0
    
    mn_cbr_loss = 0
    mn_voice_loss = 0
    mn_video_loss = 0
    mn_avg_loss = 0
    sn_cbr_loss = 0
    sn_voice_loss = 0
    sn_video_loss = 0
    sn_avg_loss = 0

class ValueCalculate: #基地台每打一次波束就會執行一次 (當執行beam_number次的時候就會進行統整)
    def add_data_amount(bs_id, ue_id, data_amount):
        ValueCalculateData.total_ue_data.setdefault(ue_id, 0)
        ValueCalculateData.total_ue_data[ue_id] += data_amount

        if len(NetworkSettings.ue_to_bs_mapping_table[ue_id]) == 2:
            ValueCalculateData.dc_ue_data.setdefault(ue_id, 0)
            ValueCalculateData.dc_ue_data[ue_id] += data_amount

            if bs_id == "bs0":
                ValueCalculateData.mn_ue_data.setdefault(ue_id, 0)
                ValueCalculateData.mn_ue_data[ue_id] += data_amount
            else:
                ValueCalculateData.sn_ue_data.setdefault(ue_id, 0)
                ValueCalculateData.sn_ue_data[ue_id] += data_amount

    def add_delay_data(bs_id, ue_id, data_type, queue_time):
        type_data_amount_dict = {
            "CBR": (1460 * 8),
            "voice": (10 * 8),
            "video": (1000 * 8)
        }

        if len(NetworkSettings.ue_to_bs_mapping_table[ue_id]) == 2:
            if bs_id == "bs0":
                ValueCalculateData.mn_delay_data[data_type]["data_amount"] += type_data_amount_dict[data_type]
                ValueCalculateData.mn_delay_data[data_type]["queue_time"] += type_data_amount_dict[data_type] * queue_time
            else:
                ValueCalculateData.sn_delay_data[data_type]["data_amount"] += type_data_amount_dict[data_type]
                ValueCalculateData.sn_delay_data[data_type]["queue_time"] += type_data_amount_dict[data_type] * queue_time

    def add_loss_sent_data(bs_id, ue_id, data_type, data_amount):
        if len(NetworkSettings.ue_to_bs_mapping_table[ue_id]) == 2:
            if bs_id == "bs0":
                ValueCalculateData.mn_loss_data[data_type]["sent_data_amount"] += data_amount
            else:
                ValueCalculateData.sn_loss_data[data_type]["sent_data_amount"] += data_amount

    def add_loss_drop_data(bs_id, ue_id, data_type):
        type_data_amount_dict = {
            "CBR": (1460 * 8),
            "voice": (10 * 8),
            "video": (1000 * 8)
        }
        
        if len(NetworkSettings.ue_to_bs_mapping_table[ue_id]) == 2:
            if bs_id == "bs0":
                ValueCalculateData.mn_loss_data[data_type]["drop_data_amount"] += type_data_amount_dict[data_type]
            else:
                ValueCalculateData.sn_loss_data[data_type]["drop_data_amount"] += type_data_amount_dict[data_type]

    def throughput_fairness_calculate():
        total_ue_data_amount = 0
        total_square_data_amount = 0
        for ue_id, data_amount in ValueCalculateData.total_ue_data.items():
            total_ue_data_amount += data_amount
            total_square_data_amount += (data_amount ** 2)
        ValueCalculateData.system_throughput = total_ue_data_amount * 1000 / SystemInfo.system_time / (10 ** 6)
        ValueCalculateData.avg_ue_throughput = total_ue_data_amount * 1000 / SystemInfo.system_time / (len(NetworkSettings.ue_to_bs_mapping_table)) / (10 ** 6)

        dc_ue_data_amount = 0
        dc_square_data_amount = 0
        for ue_id, data_amount in ValueCalculateData.dc_ue_data.items():
            dc_ue_data_amount += data_amount
            dc_square_data_amount += (data_amount ** 2)
        ValueCalculateData.dc_avg_ue_throughput = dc_ue_data_amount * 1000 / SystemInfo.system_time / (len(ValueCalculateData.dc_ue_data)) / (10 ** 6)

        mn_ue_data_amount = 0
        mn_square_data_amount = 0
        for ue_id, data_amount in ValueCalculateData.mn_ue_data.items():
            mn_ue_data_amount += data_amount
            mn_square_data_amount += (data_amount ** 2)
        ValueCalculateData.mn_throughput = mn_ue_data_amount * 1000 / SystemInfo.system_time / (10 ** 6)

        sn_ue_data_amount = 0
        sn_square_data_amount = 0
        for ue_id, data_amount in ValueCalculateData.sn_ue_data.items():
            sn_ue_data_amount += data_amount
            sn_square_data_amount += (data_amount ** 2)
        ValueCalculateData.sn_throughput = sn_ue_data_amount * 1000 / SystemInfo.system_time / (10 ** 6)

        if NetworkSettings.fairness_method == 1:
            ValueCalculateData.fairness = (total_ue_data_amount ** 2) / ((len(NetworkSettings.ue_to_bs_mapping_table)) * total_square_data_amount)
            ValueCalculateData.dc_fairness = (dc_ue_data_amount ** 2) / ((len(ValueCalculateData.dc_ue_data)) * dc_square_data_amount)
            ValueCalculateData.mn_fairness = (mn_ue_data_amount ** 2) / ((len(ValueCalculateData.mn_ue_data)) * mn_square_data_amount)
            ValueCalculateData.sn_fairness = (sn_ue_data_amount ** 2) / ((len(ValueCalculateData.sn_ue_data)) * sn_square_data_amount)

        if NetworkSettings.fairness_method == 2:
            ValueCalculateData.fairness = sum(ValueCalculateData.fairness_list) / len(ValueCalculateData.fairness_list)
            ValueCalculateData.dc_fairness = sum(ValueCalculateData.dc_fairness_list) / len(ValueCalculateData.dc_fairness_list)
            ValueCalculateData.mn_fairness = sum(ValueCalculateData.mn_fairness_list) / len(ValueCalculateData.mn_fairness_list)
            ValueCalculateData.sn_fairness = sum(ValueCalculateData.sn_fairness_list) / len(ValueCalculateData.sn_fairness_list)

    def delay_calculate():
        ValueCalculateData.mn_cbr_delay = ValueCalculateData.mn_delay_data["CBR"]["queue_time"] / ValueCalculateData.mn_delay_data["CBR"]["data_amount"]
        ValueCalculateData.mn_voice_delay = ValueCalculateData.mn_delay_data["voice"]["queue_time"] / ValueCalculateData.mn_delay_data["voice"]["data_amount"]
        ValueCalculateData.mn_video_delay = ValueCalculateData.mn_delay_data["video"]["queue_time"] / ValueCalculateData.mn_delay_data["video"]["data_amount"]
        mn_delay_data_queue_time = ValueCalculateData.mn_delay_data["CBR"]["queue_time"] + ValueCalculateData.mn_delay_data["voice"]["queue_time"] + ValueCalculateData.mn_delay_data["video"]["queue_time"]
        mn_delay_data_data_amount = ValueCalculateData.mn_delay_data["CBR"]["data_amount"] + ValueCalculateData.mn_delay_data["voice"]["data_amount"] + ValueCalculateData.mn_delay_data["video"]["data_amount"]
        ValueCalculateData.mn_avg_delay = mn_delay_data_queue_time / mn_delay_data_data_amount

        ValueCalculateData.sn_cbr_delay = ValueCalculateData.sn_delay_data["CBR"]["queue_time"] / ValueCalculateData.sn_delay_data["CBR"]["data_amount"]
        ValueCalculateData.sn_voice_delay = ValueCalculateData.sn_delay_data["voice"]["queue_time"] / ValueCalculateData.sn_delay_data["voice"]["data_amount"]
        ValueCalculateData.sn_video_delay = ValueCalculateData.sn_delay_data["video"]["queue_time"] / ValueCalculateData.sn_delay_data["video"]["data_amount"]
        sn_delay_data_queue_time = ValueCalculateData.sn_delay_data["CBR"]["queue_time"] + ValueCalculateData.sn_delay_data["voice"]["queue_time"] + ValueCalculateData.sn_delay_data["video"]["queue_time"]
        sn_delay_data_data_amount = ValueCalculateData.sn_delay_data["CBR"]["data_amount"] + ValueCalculateData.sn_delay_data["voice"]["data_amount"] + ValueCalculateData.sn_delay_data["video"]["data_amount"]
        ValueCalculateData.sn_avg_delay = sn_delay_data_queue_time / sn_delay_data_data_amount

    def loss_calculate():
        ValueCalculateData.mn_cbr_loss = ValueCalculateData.mn_loss_data["CBR"]["drop_data_amount"] / (ValueCalculateData.mn_loss_data["CBR"]["drop_data_amount"] + ValueCalculateData.mn_loss_data["CBR"]["sent_data_amount"])
        ValueCalculateData.mn_voice_loss = ValueCalculateData.mn_loss_data["voice"]["drop_data_amount"] / (ValueCalculateData.mn_loss_data["voice"]["drop_data_amount"] + ValueCalculateData.mn_loss_data["voice"]["sent_data_amount"])
        ValueCalculateData.mn_video_loss = ValueCalculateData.mn_loss_data["video"]["drop_data_amount"] / (ValueCalculateData.mn_loss_data["video"]["drop_data_amount"] + ValueCalculateData.mn_loss_data["video"]["sent_data_amount"])
        mn_loss_data_drop_data_amount = ValueCalculateData.mn_loss_data["CBR"]["drop_data_amount"] + ValueCalculateData.mn_loss_data["voice"]["drop_data_amount"] + ValueCalculateData.mn_loss_data["video"]["drop_data_amount"]
        mn_loss_data_sent_data_amount = ValueCalculateData.mn_loss_data["CBR"]["sent_data_amount"] + ValueCalculateData.mn_loss_data["voice"]["sent_data_amount"] + ValueCalculateData.mn_loss_data["video"]["sent_data_amount"]
        ValueCalculateData.mn_avg_loss = mn_loss_data_drop_data_amount / (mn_loss_data_drop_data_amount + mn_loss_data_sent_data_amount)

        ValueCalculateData.sn_cbr_loss = ValueCalculateData.sn_loss_data["CBR"]["drop_data_amount"] / (ValueCalculateData.sn_loss_data["CBR"]["drop_data_amount"] + ValueCalculateData.sn_loss_data["CBR"]["sent_data_amount"])
        ValueCalculateData.sn_voice_loss = ValueCalculateData.sn_loss_data["voice"]["drop_data_amount"] / (ValueCalculateData.sn_loss_data["voice"]["drop_data_amount"] + ValueCalculateData.sn_loss_data["voice"]["sent_data_amount"])
        ValueCalculateData.sn_video_loss = ValueCalculateData.sn_loss_data["video"]["drop_data_amount"] / (ValueCalculateData.sn_loss_data["video"]["drop_data_amount"] + ValueCalculateData.sn_loss_data["video"]["sent_data_amount"])
        sn_loss_data_drop_data_amount = ValueCalculateData.sn_loss_data["CBR"]["drop_data_amount"] + ValueCalculateData.sn_loss_data["voice"]["drop_data_amount"] + ValueCalculateData.sn_loss_data["video"]["drop_data_amount"]
        sn_loss_data_sent_data_amount = ValueCalculateData.sn_loss_data["CBR"]["sent_data_amount"] + ValueCalculateData.sn_loss_data["voice"]["sent_data_amount"] + ValueCalculateData.sn_loss_data["video"]["sent_data_amount"]
        ValueCalculateData.sn_avg_loss = sn_loss_data_drop_data_amount / (sn_loss_data_drop_data_amount + sn_loss_data_sent_data_amount)