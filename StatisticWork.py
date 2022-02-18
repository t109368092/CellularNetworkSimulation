from NetworkSettings import NetworkSettings
from ValueCalculate import ValueCalculate ,ValueCalculateData
from GeneticAlgorithm import GeneticAlgorithmData
import csv

class StatisticWork:
    def __init__(self):
        self.total_received_data = 0
        self.total_unsent_data = 0

    def execute(self):
        self.calculate_ue_data()
        self.calculate_bs_data()
        self.print_all_results()
        if NetworkSettings.write_data == True:
            self.write_csv()
    
    def calculate_ue_data(self):
        for ue in NetworkSettings.ue_id_list:
            self.total_received_data += NetworkSettings.object_info_dict[ue].received_data_amount
            #print("ue = ",ue)
            #print("self.total_received_data = ",self.total_received_data)
    def calculate_bs_data(self):
        for bs in NetworkSettings.bs_id_list:
            bs_queue = NetworkSettings.object_info_dict[bs].queue_for_ue
            for ue_id, ue_type_data in bs_queue.items():
                for data_type,data_amount in ue_type_data.items(): 
                    self.total_unsent_data += data_amount
            #print("bs = {} , bs_queue = {} ".format(bs,bs_queue))
            #print("self.total_unsent_data = ",self.total_unsent_data)

    def print_all_results(self):
        #print("ValueCalculateData.dc_ue_data: ", ValueCalculateData.dc_ue_data)
        print("GeneticAlgorithmData.ue_gene_mappig_table: ", GeneticAlgorithmData.ue_gene_mappig_table)
        print("NetworkSettings.bs_ue_distance: ", NetworkSettings.bs_ue_distance)
        print("total_received_data: {}".format(self.total_received_data))
        print("total_unsent_data: {}".format(self.total_unsent_data))

        ValueCalculate.throughput_fairness_calculate()
        print("System Throughput(Mbps): ", ValueCalculateData.system_throughput)
        print("MN Throughput(Mbps): ",ValueCalculateData.mn_throughput)
        print("SN Throughput(Mbps): ",ValueCalculateData.sn_throughput)
        print("Average UE Throughput(Mbps): ", ValueCalculateData.avg_ue_throughput)
        print("Average DC UE Throughput(Mbps): ", ValueCalculateData.dc_avg_ue_throughput)
        print("UE Fairness: ", ValueCalculateData.fairness)
        print("DC UE Fairness: ", ValueCalculateData.dc_fairness)
        print("MN UE Fairness: ", ValueCalculateData.mn_fairness)
        print("SN UE Fairness: ", ValueCalculateData.sn_fairness)

        ValueCalculate.delay_calculate()
        ValueCalculate.loss_calculate()
        print("MN CBR Delay: ", ValueCalculateData.mn_cbr_delay)
        print("MN Voice Delay: ", ValueCalculateData.mn_voice_delay)
        print("MN Video Delay: ", ValueCalculateData.mn_video_delay)
        print("MN Average Delay: ", ValueCalculateData.mn_avg_delay)
        print("SN CBR Delay: ", ValueCalculateData.sn_cbr_delay)
        print("SN Voice Delay: ", ValueCalculateData.sn_voice_delay)
        print("SN Video Delay: ", ValueCalculateData.sn_video_delay)
        print("SN Average Delay: ", ValueCalculateData.sn_avg_delay)
        print("MN CBR Loss: ", ValueCalculateData.mn_cbr_loss)
        print("MN Voice Loss: ", ValueCalculateData.mn_voice_loss)
        print("MN Video Loss: ", ValueCalculateData.mn_video_loss)
        print("MN Average Loss: ", ValueCalculateData.mn_avg_loss)
        print("SN CBR Loss: ", ValueCalculateData.sn_cbr_loss)
        print("SN Voice Loss: ", ValueCalculateData.sn_voice_loss)
        print("SN Video Loss: ", ValueCalculateData.sn_video_loss)
        print("SN Average Loss: ", ValueCalculateData.sn_avg_loss)

    def write_csv(self):
        path  = "simulation_result.csv"
        with open(path, 'a+') as f:
            csv_write = csv.writer(f)
            data_row = [ValueCalculateData.system_throughput, ValueCalculateData.mn_throughput, ValueCalculateData.sn_throughput, ValueCalculateData.avg_ue_throughput, ValueCalculateData.dc_avg_ue_throughput,
                        ValueCalculateData.fairness, ValueCalculateData.dc_fairness, ValueCalculateData.mn_fairness, ValueCalculateData.sn_fairness,
                        ValueCalculateData.mn_cbr_delay, ValueCalculateData.mn_voice_delay, ValueCalculateData.mn_video_delay, ValueCalculateData.mn_avg_delay,
                        ValueCalculateData.sn_cbr_delay, ValueCalculateData.sn_voice_delay, ValueCalculateData.sn_video_delay, ValueCalculateData.sn_avg_delay,
                        ValueCalculateData.mn_cbr_loss, ValueCalculateData.mn_voice_loss, ValueCalculateData.mn_video_loss, ValueCalculateData.mn_avg_loss,
                        ValueCalculateData.sn_cbr_loss, ValueCalculateData.sn_voice_loss, ValueCalculateData.sn_video_loss, ValueCalculateData.sn_avg_loss]
            csv_write.writerow(data_row)

    
