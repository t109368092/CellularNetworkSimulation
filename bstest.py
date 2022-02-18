import numpy as np
import math
import random

#ue_number = 3
distance = [400] #ue1 與 bs1,bs2,bs3距離
BS_center_frequency = 28000 #基地台中心頻率(MHZ) -> 總共28GHZ
BS_transmission_power = 45 #基地台傳輸功率(tx power) dbm
BS_antenna_gain = 8 #dbi
UE_antenna_gain = 5
Thermal_noise_dbm = -174 #熱聲噪
#Number_resource_block = 25 
system_bandwidth = 75 #(MHZ)
numerology = 3 #子載波間隔

#prb_size = 15*(2**numerology) * 12 #一個prb有12個subcarriers(15khz)
#Number_resource_block = 264 # 400MHZ 信道帶寬 FR2 (信道带宽也就是在基站上配置的系统带宽) 資源塊數量範圍 24~275皆可
#total_prb = Number_resource_block * (10 * 2**numerology)
#https://www.everythingrf.com/rf-calculators/noise-power-calculator
#https://en.wikipedia.org/wiki/Johnson%E2%80%93Nyquist_noise
N0 = Thermal_noise_dbm + 10 * np.log10(system_bandwidth * (10 ** 6)) #dbm thermal noise power
print("N0_dbm",N0)
N0 = 10 ** ((N0-30)/10)
print("N0_Watt",N0)
for i in range(len(distance)):
    distance[i] = distance[i]/1000 #換算成公里為單位
#https://www.electronics-notes.com/articles/antennas-propagation/propagation-overview/free-space-path-loss.php
pathloss = 20 * np.log10(distance)+ 20 * np.log10(BS_center_frequency) + 32.44 - BS_antenna_gain - UE_antenna_gain #db
#https://www.cerio.com.tw/services/rf-power-tool/
#https://www.pczone.com.tw/vbb3/thread/44/99395/ #dbm EIRP
#https://www.electronics-notes.com/articles/antennas-propagation/propagation-overview/radio-link-budget-formula-calculator.php
received_power = BS_transmission_power - pathloss - 2.15 #dbm = dbm - db
print("received_power_dbm = ",received_power)
received_power = 10 **((received_power-30)/10) # Watt
#https://ithelp.ithome.com.tw/articles/10227252
#https://blog.csdn.net/Kathleen_yuan/article/details/89817487
print("received_power_Watt = ",received_power)
snr = received_power / N0 # use power(dbm ) /noise (dbm) = Watt / Watt
interference = list()
#https://www.google.com.tw/search?q=5g+distance+snr&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjXlsHenM_0AhVuklYBHUqLDWIQ_AUoAnoECAEQBA&biw=1707&bih=740&dpr=1.13#imgrc=UJipPy7zal-8CM
for i in range(len(received_power)):
    interference.append(sum(received_power) - received_power[i]) #不需要的基地台功率 Watt
print("interference = ",interference)
sinr = received_power / (interference + N0)
sinr_db = 10 * np.log10(sinr)
#https://www.rfwireless-world.com/calculators/channel-capacity-calculator.html
#https://baike.baidu.hk/item/%E9%A6%99%E8%BE%B2%E5%85%AC%E5%BC%8F/857947
rate = system_bandwidth*(10 ** 6) * np.log2(1 + sinr) #因為sinr為負值 沒有data rate 收不到訊號
rate_sec = rate * (10**-6)
#https://www.youtube.com/watch?v=FrYaT3lIeto
#https://www.youtube.com/watch?v=DKEBTifZs9o
Number_resource_block = math.floor(system_bandwidth * (10 ** 3) / (12 * 15)) # KHZ / KHZ
Guard = system_bandwidth * (10 ** 3) - (Number_resource_block - 1) * (12 * 15) #KHz
Number_resource_block = math.floor((system_bandwidth * (10 ** 3) - Guard) / (12 * 15)) #KHz
rb_rate_ms = rate_sec / 1000 / Number_resource_block
snr_db = 10 * np.log10(snr)
print("sinr = ",sinr)
print("sinr_db = ",sinr_db )
print("snr = ",snr)
print("snr_db = ",snr_db)
print("ue_rate_Mbits/sec = ",rate_sec)
print("Guard_KHz = ",Guard)
print("Number_resource_block = ",Number_resource_block)
print("rb_rate_Mbits/ms = {} rb_rate_kbits/ms = {} ".format(rb_rate_ms,rb_rate_ms*1000))