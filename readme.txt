<一> main.py
目的:程式開始

1.create_bs(事件處理器環境)
-->創建基地台
bs = BaseStation.BaseStation object 位置

2.create_ue(事件處理器環境)
-->創建使用者
ue = UserEquipment.UserEquipment object 位置

3.mapping_bs_and_ue
-->基地台與使用者的連接關係
--------------------------------------------------------------------------------------------------------------------
<二> EventManager.py
目的:事件環境管理器

1.execute
--> 事件開始執行(之前生成的事件已經導入)
event :(系統時間, {'event_target': , 'event_name': , 'event_trigger_time': , 'event_details': {'data_amount':}})
event_target = 事件目標
event_name = 事件名稱
event_trigger_time = 事件觸發時間(整數)
event_details = 事件資訊
event_content = event[1]
Queue.qsize()：返回 Queue 的大小
Queue.get([block[, timeout]])：取出 Queue，timeout 可以指定等待時間

2.add_new_event(事件時間、甚麼事件)
添加已產生的事件
event_time = 事件時間
event_content = 甚麼事件
Queue.put(item)：放入 Queue，timeout 可以指定等待時間
--------------------------------------------------------------------------------------------------------------------
<三> NetworkSettings.py
目的:設定網路環境

1.class NetworkSettings
-->網路系統設定
num_of_bs、num_of_ue = 基地台數量、使用者數量
simulation_time = 模擬時間
ue_id_list、bs_id_list = 使用者列表、基地台列表
object_info_dict = (BaseStation 或 UserEquipment object的位置)

2.SystemInfo
-->系統開始時間

--------------------------------------------------------------------------------------------------------------------
<四> StatisticWork.py
目的:靜態工作 計算UE和基地台資料

1.execute
calculate_ue_data -> calculate_bs_data -> print_all_results

2.calculate_ue_data
-->計算UE data
received_data_amount = 該UE的接收資料

3.calculate_bs_data
-->計算BS data

4.print_all_results
self.total_received_data = 接收到的數據總量
self.total_unsent_data = 未發送數據總數

--------------------------------------------------------------------------------------------------------------------
<五> BaseStation.py
目的:基地台資料處理
1.class BsProcessData
-->基地台背景程式傳輸資料
self.event_details = {'target_ue': 目標UE, 'data_amount': 資料size}
execute():連接 add_data_for_ue()

2.class BsSched
-->基地台要執行的schedule動作
execute(): generate_event_to_self() -> perform_resource_assignment()
generate_event_to_self():每1ms會生成基地台'schedule'動作事件 更新event_manager的時間與事件
perform_resource_assignment():執行資源分配
generate_event_to_ue(target_ue, data_amount): 每1ms生成事件'下行傳輸資料'給目標UE
ue_data = {'ue':'data_amount'}
3.class BaseStation
-->
event_handler_dict: 事件池
generate_first_event(): 生成所有BS第一個事件 schedule 在第1ms的時候
event_handler(event_content): 檢查該BS的事件是否在 event_handler_dict 內，若在則執行 event_handler_dict內事件
add_data_for_ue(ue_id, data_amount): 該基地台將資料傳給目標ue(UE資料會累加) -->基地台滯留的資料
dec_data_for_ue(ue_id, data_amount): 將基地台滯留的資料 -->基地台送出的資料
--------------------------------------------------------------------------------------------------------------------
<六> UserEquipment.py
目的:使用者資料處理
1.class UeProcessData
-->使用者背景程式傳輸資料
self.event_details =  {'data_amount':}
execute():連接到add_received_data_amount()

2.class UserEquipment
-->使用者設備
__init__(ue_id, event_manager):定義tg_id、連接到TrafficGenerator
event_handler(event_content):檢查該UE的事件是否在 event_handler_dict 內
add_received_data_amount(data_amount):UE接收資料大小累加

--------------------------------------------------------------------------------------------------------------------
<七>TrafficGenerator
目的:流量隨機生成器
1.class GenerateData:
execute(): self.generate_event_to_target_bs() -> self.generate_event_to_self()
generate_event_to_target_bs(target_bs, event_details):生成傳入資料事件給目標基地台
generate_event_to_self():生成 隨機(0~50時間)生成資料事件給目標ue tg_id

2.class TrafficGenerator:
generate_first_event():生成 目標tg_id的第一個事件generate_data
event_handler(): 檢查該BS的事件是否在 event_handler_dict 內，若在則執行 event_handler_dict 內事件 連接到GenerateData.execute


--------------------------------------------------------------------------------------------------------------------

問題1:tgid是甚麼東西
問題2:BaseStation.py 內的 event_details 在 BsProcessData 和 BsSched內表現不同