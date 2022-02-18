class NetworkSettings:
    num_of_ue = 15 #基地台的UE數量
    data_amount = 60 #正常Data量倍數
    simulation_time = 150000 #模擬時間 ms
    flow_control_method = 1 #1->GA, 2->50%
    fairness_method = 2 #1->Old Method, 2->New Method
    delay_method = 2 #1->Old Method, 2->New Method
    write_data = True
    #write_data = False

    #MN parameters
    #mn_bs_range = 1000 #MN基地台覆蓋範圍(m)
    #mn_center_frequency = 3500 #基地台中心頻率(MHZ)
    #mn_transmission_power = 75 #基地台傳輸功率(dBm)
    #mn_system_bandwidth = 20 #系統帶寬(MHZ)
    mn_bs_range = 600 #MN基地台覆蓋範圍(m)
    mn_center_frequency = 28000 #基地台中心頻率(MHZ)
    mn_transmission_power = 45 #基地台傳輸功率(dBm)
    mn_system_bandwidth = 50 #系統帶寬(MHZ)

    #SN parameters
    num_of_sn_bs = 3 #SN基地台數量
    bs_min_distance = 300 #SN基地台最小間隔
    sn_bs_range = 300 #SN基地台覆蓋範圍(m)
    sn_center_frequency = 28000 #基地台中心頻率(MHZ)
    sn_transmission_power = 23 #基地台傳輸功率(dBm)
    sn_system_bandwidth = 50 #系統帶寬(MHZ)
    #num_of_sn_bs = 3 #SN基地台數量
    #bs_min_distance = 300 #SN基地台最小間隔
    #sn_bs_range = 300 #SN基地台覆蓋範圍(m)
    #sn_center_frequency = 3500 #基地台中心頻率(MHZ)
    #sn_transmission_power = 23 #基地台傳輸功率(dBm)
    #sn_system_bandwidth = 20 #系統帶寬(MHZ)

    #Other parameters
    Number_resource_block = 25 #資源快數量
    BS_antenna_gain = 8 #dbi
    UE_antenna_gain = 5
    Thermal_noise_dbm = -174 #熱聲噪

    #List
    ue_id_list = list() #所有ue的儲存用列表
    bs_id_list = list() #所有bs的儲存用列表
    object_info_dict = dict() #事件物件的字典
    ue_to_bs_mapping_table = dict() #ue和bs的連接關係以字典表示
    bs_ue_distance = dict() #基地台與UE的距離

class SystemInfo:
    system_time = 0
    event_priority = 0
    interval_time = 5 #實際值100 暫時以5作為標準

class Simulation:
    interval_delay_time = dict()

class GAParameters:
    fitness_method = 3
    select_method = 2

    mutation_rate = 0.1
    population_size = 10
    chromosome_run_time = 1000
