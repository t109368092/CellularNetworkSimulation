import numpy as np
import matplotlib.pyplot as plt
import csv

simulation_data = list()

system_throughput = list()
mn_throughput = list()
sn_throughput = list()
avg_throughput = list()
dc_avg_ue_throughput = list()

fairness = list()
dc_fairness = list()
mn_fairness = list()
sn_fairness = list()

mn_cbr_delay = list()
mn_voice_delay = list()
mn_video_delay = list()
mn_avg_delay = list()
sn_cbr_delay = list()
sn_voice_delay = list()
sn_video_delay = list()
sn_avg_delay = list()

mn_cbr_loss = list()
mn_voice_loss = list()
mn_video_loss = list()
mn_avg_loss = list()
sn_cbr_loss = list()
sn_voice_loss = list()
sn_video_loss = list()
sn_avg_loss = list()

path = "simulation_result.csv"
with open(path, 'r') as f:
    simulation_data_object = csv.reader(f)

    for i in simulation_data_object:
        simulation_data.append(i)

for i in simulation_data[1:]:
    system_throughput.append(round(float(i[0]), 2))
    mn_throughput.append(round(float(i[1]), 2))
    sn_throughput.append(round(float(i[2]), 2))
    avg_throughput.append(round(float(i[3]), 2))
    dc_avg_ue_throughput.append(round(float(i[4]), 2))

    fairness.append(round(float(i[5]), 2))
    dc_fairness.append(round(float(i[6]), 2))
    mn_fairness.append(round(float(i[7]), 2))
    sn_fairness.append(round(float(i[8]), 2))

    mn_cbr_delay.append(round(float(i[9]), 2))
    mn_voice_delay.append(round(float(i[10]), 2))
    mn_video_delay.append(round(float(i[11]), 2))
    mn_avg_delay.append(round(float(i[12]), 2))
    sn_cbr_delay.append(round(float(i[13]), 2))
    sn_voice_delay.append(round(float(i[14]), 2))
    sn_video_delay.append(round(float(i[15]), 2))
    sn_avg_delay.append(round(float(i[16]), 2))

    mn_cbr_loss.append(round(float(i[17]), 2))
    mn_voice_loss.append(round(float(i[18]), 2))
    mn_video_loss.append(round(float(i[19]), 2))
    mn_avg_loss.append(round(float(i[20]), 2))
    sn_cbr_loss.append(round(float(i[21]), 2))
    sn_voice_loss.append(round(float(i[22]), 2))
    sn_video_loss.append(round(float(i[23]), 2))
    sn_avg_loss.append(round(float(i[24]), 2))


method = ['50%', 'GA1', 'GA2', 'GA3']
method_color = ['red', 'green', 'blue', 'yellow']
plt_value = {"throughput": [system_throughput, mn_throughput, sn_throughput, avg_throughput, dc_avg_ue_throughput],
             "fairness": [fairness, dc_fairness, mn_fairness, sn_fairness],
             "delay": [mn_cbr_delay, mn_voice_delay, mn_video_delay, mn_avg_delay, sn_cbr_delay, sn_voice_delay, sn_video_delay, sn_avg_delay],
             "loss": [mn_cbr_loss, mn_voice_loss, mn_video_loss, mn_avg_loss, sn_cbr_loss, sn_voice_loss, sn_video_loss, sn_avg_loss]}
plt_title = {"throughput": ["System Throughput(Mbps)", "MN Throughput(Mbps)", "SN Throughput(Mbps)", "Average UE Throughput(Mbps)", "Average DC UE Throughput(Mbps)"], 
             "fairness": ["UE Fairness", "DC UE Fairness", "MN UE Fairness", "SN UE Fairness"],
             "delay": ["MN CBR Delay", "MN Voice Delay", "MN Video Delay", "MN Average Delay", "SN CBR Delay", "SN Voice Delay", "SN Video Delay", "SN Average Delay"],
             "loss": ["MN CBR Loss", "MN Voice Loss", "MN Video Loss", "MN Average Loss", "SN CBR Loss", "SN Voice Loss", "SN Video Loss", "SN Average Losss"]}

len_x = np.arange(len(method))
max_data = {"throughput": 0, "fairness": 0, "delay": 0, "loss": 0}
for item, value in plt_value.items():
    for data_list in value:
        max_value = max(data_list)
        if max_value > max_data[item]:
            max_data[item] = max_value

for item, value in plt_value.items():
    for j in range(len(value)):
        plt.subplot(3, 3, j+1)
        plt.bar(len_x, value[j], color=method_color)
        plt.xlabel('Method')
        plt.xticks(len_x, method)
        plt.ylabel(plt_title[item][j])
        plt.yticks((0, max_data[item]))

#    plt.subplots_adjust(left=0.075,
#                        bottom=0.1, 
#                        right=0.95, 
#                        top=0.85, 
#                        wspace=0.7, 
#                        hspace=0.7)
    plt.tight_layout()
    plt.show()