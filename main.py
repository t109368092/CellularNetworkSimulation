from math import pi
from EventManager import EventManagerGA, EventManagerFifty
from BaseStation import BaseStation
from UserEquipment import UserEquipment
from NetworkSettings import NetworkSettings
import numpy as np
import random

ue_location_list = list()
bs_location_list = list()

flow_control_method_dict = {
    1: EventManagerGA,
    2: EventManagerFifty
}

def create_bs(event_manager):
    #Create MN
    bs_x = 0
    bs_y = 0
    bs_location_list.append((bs_x, bs_y))

    bs = BaseStation(0, event_manager)
    bs_id = "bs0"
    NetworkSettings.object_info_dict[bs_id] = bs
    NetworkSettings.bs_id_list.append(bs_id)

    #Create SN
    while len(bs_location_list) - 1 < NetworkSettings.num_of_sn_bs:
        bs_location_available = True
        sn_mn_distance = random.uniform(NetworkSettings.bs_min_distance, NetworkSettings.mn_bs_range)
        sn_mn_angle = random.uniform(0, (2 * pi))
        bs_location = pol2cart(sn_mn_distance, sn_mn_angle)

        for i in range(len(bs_location_list) - 1):
            sn_distance_x = bs_location[0] - bs_location_list[i + 1][0]
            sn_distance_y = bs_location[1] - bs_location_list[i + 1][1]
            sn_distance = np.sqrt((sn_distance_x ** 2) + (sn_distance_y ** 2))

            if sn_distance < NetworkSettings.bs_min_distance:
                bs_location_available = False

        if bs_location_available == True:
            bs_location_list.append(bs_location)

            bs = BaseStation(len(bs_location_list) - 1, event_manager)
            bs_id = "bs{}".format(len(bs_location_list) - 1)
            NetworkSettings.object_info_dict[bs_id] = bs
            NetworkSettings.bs_id_list.append(bs_id)

def create_bs_temp(event_manager):
    #Create MN
    bs_x = 0
    bs_y = 0
    bs_location_list.append((bs_x, bs_y))

    bs = BaseStation(0, event_manager)
    bs_id = "bs0"
    NetworkSettings.object_info_dict[bs_id] = bs
    NetworkSettings.bs_id_list.append(bs_id)

    #Create SN
    sn_mn_distance = 300
    sn_mn_angle = pi / 4
    bs_location = pol2cart(sn_mn_distance, sn_mn_angle)
    bs_location_list.append(bs_location)
    bs = BaseStation(1, event_manager)
    bs_id = "bs1"
    NetworkSettings.object_info_dict[bs_id] = bs
    NetworkSettings.bs_id_list.append(bs_id)

    sn_mn_distance = 300
    sn_mn_angle = 3 * pi / 4
    bs_location = pol2cart(sn_mn_distance, sn_mn_angle)
    bs_location_list.append(bs_location)
    bs = BaseStation(2, event_manager)
    bs_id = "bs2"
    NetworkSettings.object_info_dict[bs_id] = bs
    NetworkSettings.bs_id_list.append(bs_id)

    sn_mn_distance = 300
    sn_mn_angle = 3 * pi / 2
    bs_location = pol2cart(sn_mn_distance, sn_mn_angle)
    bs_location_list.append(bs_location)
    bs = BaseStation(3, event_manager)
    bs_id = "bs3"
    NetworkSettings.object_info_dict[bs_id] = bs
    NetworkSettings.bs_id_list.append(bs_id)

def create_ue(event_manager):
    for i in range(NetworkSettings.num_of_ue):
        ue_bs_distance = random.uniform(1, NetworkSettings.mn_bs_range)
        ue_bs_angle = random.uniform(0, (2 * pi))
        ue_location = pol2cart(ue_bs_distance, ue_bs_angle)
        ue_location_list.append(ue_location)

        ue = UserEquipment(i, event_manager)
        ue_id = "ue{}".format(i)
        NetworkSettings.object_info_dict[ue_id] = ue
        NetworkSettings.ue_id_list.append(ue_id)

def create_ue_temp(event_manager):
    for j in range(3):
        ue_bs_distance = 10
        ue_bs_angle = 0
        for i in range(int(NetworkSettings.num_of_ue / 3)):
            if (int(i / 2) >= 1) and (i % 2) == 0:
                ue_bs_distance += 100
            ue_bs_angle += pi / 2
            ue_location = pol2cart(ue_bs_distance, ue_bs_angle)
            ue_location_list.append(((bs_location_list[j + 1][0] + ue_location[0]),(bs_location_list[j + 1][1] + ue_location[1])))

            ue = UserEquipment(5 * j + i, event_manager)
            ue_id = "ue{}".format(5 * j + i)
            NetworkSettings.object_info_dict[ue_id] = ue
            NetworkSettings.ue_id_list.append(ue_id)
    
    #ue_bs_distance = 100
    #ue_bs_angle = 0
    #for i in range(int(NetworkSettings.num_of_ue / 4)):
    #    if (int(i / 2) >= 1) and (i % 2) == 0:
    #        ue_bs_distance += 200
    #    ue_bs_angle += pi / 2
    #    ue_location = pol2cart(ue_bs_distance, ue_bs_angle)
    #    ue_location_list.append(ue_location)

    #    ue = UserEquipment(15 + i, event_manager)
    #    ue_id = "ue{}".format(15 + i)
    #    NetworkSettings.object_info_dict[ue_id] = ue
    #    NetworkSettings.ue_id_list.append(ue_id)

def mapping_bs_and_ue():
    for i in range(NetworkSettings.num_of_ue):
        #Mapping MN BS
        ue_bs_x_distance = abs(ue_location_list[i][0] - bs_location_list[0][0])
        ue_bs_y_distance = abs(ue_location_list[i][1] - bs_location_list[0][1])
        ue_bs_distance = np.sqrt((ue_bs_x_distance ** 2) + (ue_bs_y_distance ** 2))
        if  ue_bs_distance <= NetworkSettings.mn_bs_range:
            NetworkSettings.ue_to_bs_mapping_table.setdefault("ue{}".format(i), [])
            NetworkSettings.ue_to_bs_mapping_table["ue{}".format(i)].append("bs0")
            NetworkSettings.bs_ue_distance.setdefault("ue{}".format(i), [])
            NetworkSettings.bs_ue_distance["ue{}".format(i)].append(ue_bs_distance)

        #Mapping SN BS
        ue_bs_distance_dict = dict()
        for j in range(NetworkSettings.num_of_sn_bs):
            ue_bs_x_distance = abs(ue_location_list[i][0] - bs_location_list[j + 1][0])
            ue_bs_y_distance = abs(ue_location_list[i][1] - bs_location_list[j + 1][1])
            ue_bs_distance = np.sqrt((ue_bs_x_distance ** 2) + (ue_bs_y_distance ** 2))
            if  ue_bs_distance <= NetworkSettings.sn_bs_range:
                ue_bs_distance_dict["bs{}".format(j + 1)] = ue_bs_distance
        
        if len(ue_bs_distance_dict) >= 1:
            ue_bs_min_distance_bs = min(ue_bs_distance_dict, key = ue_bs_distance_dict.get)
            ue_bs_min_distance = ue_bs_distance_dict[ue_bs_min_distance_bs]

            NetworkSettings.ue_to_bs_mapping_table.setdefault("ue{}".format(i), [])
            NetworkSettings.ue_to_bs_mapping_table["ue{}".format(i)].append(ue_bs_min_distance_bs)
            NetworkSettings.bs_ue_distance.setdefault("ue{}".format(i), [])
            NetworkSettings.bs_ue_distance["ue{}".format(i)].append(ue_bs_min_distance)
    #print("NetworkSettings.ue_to_bs_mapping_table: ", NetworkSettings.ue_to_bs_mapping_table)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x,y)

def main():
    event_manager = flow_control_method_dict[NetworkSettings.flow_control_method]()
    create_bs_temp(event_manager)
    create_ue_temp(event_manager)
    mapping_bs_and_ue()
    event_manager.execute()


if __name__ == '__main__':
    main()