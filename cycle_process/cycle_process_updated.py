from copy import copy
import pandas as pd 
from datetime import datetime
from datetime import timedelta
import numpy as np

pop_sheet = 'Population' 
visits_sheet = 'Visits'
file_name = 'population.xlsx' 
df_pop = pd.read_excel(file_name, sheet_name = pop_sheet )
df_visits = pd.read_excel(file_name, sheet_name = visits_sheet)
print("pop sheet test :")
print(df_pop.head())

print("visits sheet test :")
print(df_visits.head())

#dataframe pop select columns 
df1 = df_pop[['ESN', 'AMC starting Date' , 'AMC Ending date', 'TOTAL VISITS ']]
print("test : ")
print(df1.head())

#visits select columns
df2 = df_visits[['ESN/Alternator No.','Opened','VISIT TYPE','Hours/KMs Run','Customer Requested On','VISIT BCD','SR #']]
print("test2 :")
print(df2.head())
df2['Customer Requested On'] = pd.to_datetime(df2['Customer Requested On'], errors='coerce')

#visit type inputs : BD VISIT , OIL SERVICE , PM VISIT
# pop_hash_only_date = {}
# for arr in df1 :
#     pop_hash_only_date[str(arr[0])] = parser.parse(arr[1]).date()
    
# print ("after stripping time :")
# print(pop_hash_only_date)

numpy_df_pop = df1.to_numpy(dtype=str)
numpy_df_vis = df2.to_numpy(dtype=str)
print (numpy_df_pop)
print (numpy_df_vis)


population_hash = {}
population_hash_end = {}


for arr in numpy_df_pop:
    arr[0] = arr[0].strip()
    #key = esn number , val = start date 
    population_hash[arr[0]] = arr[1]
    population_hash_end[arr[0]] = arr[2]


visits_hash = {}
visit_type_hash = {}
visit_num_km_rq_hash = {}

for arr in numpy_df_vis :
    arr[0] = arr[0].strip()
    if arr[0] in visits_hash.keys():
        visits_hash[arr[0]].append(arr[1])
        visit_type_hash[arr[0]].append(arr[2])
        visit_num_km_rq_hash[arr[0]].append([arr[3],arr[4],arr[5],arr[2],arr[6]])
    else :
        visits_hash[arr[0]] = [arr[1]]
        visit_type_hash[arr[0]] = [arr[2]]
        visit_num_km_rq_hash[arr[0]] = [[arr[3],arr[4],arr[5],arr[2],arr[6]]]

# print ("visits hash : ")
# print (visits_hash)

#print(visit_num_km_rq_hash)
# hash format  esn ->visits : '25316320': ['2019-01-28 12:59:46', '2019-02-22 11:46:05', '2019-03-22 11:19:42', '2019-04-29 13:58:58', '2019-05-21 09:40:26', '2019-06-28 11:05:00', '2019-07-25 10:18:35', '2019-08-27 16:45:33', '2019-09-03 10:21:11']
# visit type inputs : BD VISIT , OIL SERVICE , PM VISIT

ans_hash = {}
max_b = 0
max_c = 0 
max_d = 0
max_pm = 0
for pop_keys in population_hash.keys():
    start_date = population_hash[pop_keys]
    start_date = start_date.split(" ")[0]
    end_date = population_hash_end[pop_keys]
    end_date = end_date.split(" ")[0]
    
    ans = 0
    bd_visit = 0 
    oil_service = 0
    pm_visit = 0
    b_check_date_arr = []
    b_check_hrs_arr = []
    b_check_srn_arr = []
    c_check_date_arr = []
    c_check_hrs_arr = []
    c_check_srn_arr = []
    d_check_date_arr = []
    d_check_hrs_arr = []
    d_check_srn_arr = []
    pm_check_date_arr = []
    pm_check_hrs_arr = []
    pm_check_srn_arr = []
    ans_hash[pop_keys] = [0] * 10
    next_bc = 0
    next_visit = 0 
    if pop_keys in visits_hash.keys():
        visits_info = visits_hash[pop_keys]
        index=0
        for each_visit in visits_info :
            if '/' in each_visit:  # Check if date is in MM/DD/YYYY format
                each_visit = str(datetime.strptime(each_visit, '%m/%d/%Y'))
            else:
                each_visit = str(datetime.strptime(each_visit, '%Y-%m-%d %H:%M:%S'))
            each_visit = each_visit.split(" ")[0]
            if (each_visit >= start_date ) and (each_visit <= end_date) :
                ans = ans + 1 
                if visit_type_hash[pop_keys][index].strip() == "BD VISIT" :
                    bd_visit = bd_visit+1
                elif visit_type_hash[pop_keys][index].strip() == "OIL SERVICE":
                    oil_service = oil_service + 1 
                elif visit_type_hash[pop_keys][index].strip() == "PM VISIT":
                    pm_visit = pm_visit + 1
            index = index+1

    if pop_keys in visit_num_km_rq_hash.keys() :
        #sort according to the date .
        #data : 'Hours/KMs Run','Customer Requested On','VISIT BCD','VISIT TYPE',"SRN NO"
        visit_num_km_rq_hash[pop_keys].sort(key=lambda x:x[1])
        for arr_each_entry in visit_num_km_rq_hash[pop_keys] :
            date_rm = arr_each_entry[1].split(" ")[0]
            if (date_rm >= start_date ) and (date_rm <= end_date) :
                if arr_each_entry[-2] == "OIL SERVICE" :
                    if arr_each_entry[2] == "B CHECK" :
                        if date_rm != 0 and date_rm != 'NaT' :
                            b_check_date_arr.append(date_rm) #remove time
                            b_check_hrs_arr.append(arr_each_entry[0])
                            b_check_srn_arr.append(arr_each_entry[-1])
                        
                    elif arr_each_entry[2] == "C CHECK" :
                        if date_rm != 0 and date_rm != 'NaT' :
                            c_check_date_arr.append(date_rm)
                            c_check_hrs_arr.append(arr_each_entry[0])
                            c_check_srn_arr.append(arr_each_entry[-1])
                    elif arr_each_entry[2] == "D CHECK" :
                        if date_rm != 0 and date_rm != 'NaT' :
                            d_check_date_arr.append(date_rm)
                            d_check_hrs_arr.append(arr_each_entry[0])
                            d_check_srn_arr.append(arr_each_entry[-1])
                elif arr_each_entry[-2] == "PM VISIT" :
                    if date_rm != 0 and date_rm != 'NaT' :
                        pm_check_date_arr.append(date_rm)
                        pm_check_hrs_arr.append(arr_each_entry[0])
                        pm_check_srn_arr.append(arr_each_entry[-1])
    max_pm = max(max_pm,len(pm_check_date_arr))
    max_b = max(max_b,len(b_check_date_arr))
    max_c = max(max_c,len(c_check_date_arr))
    max_d = max(max_d,len(d_check_date_arr))
    dates_list_bc = []
    dates_list_bc.extend(b_check_date_arr)
    dates_list_bc.extend(c_check_date_arr)
    dates_list_bc.extend(d_check_date_arr)
    dates_list = copy(dates_list_bc)
    dates_list.extend(pm_check_date_arr)
    d_list = []
    if len(dates_list_bc) != 0:
        d_list = [datetime.strptime(d, '%Y-%m-%d') for d in dates_list_bc]
    d_list=sorted(d_list)
    # we need to get latest date + 300 days to get next b check
    # next_bc
    if len(d_list) >= 1:
        next_bc = d_list[-1] + timedelta(days=334) #+11 months
        next_bc = str(next_bc).split(" ")[0]
    
    d_list_vis = []
    if len(dates_list) != 0:
        d_list_vis = [datetime.strptime(d, '%Y-%m-%d') for d in dates_list]
    d_list_vis=sorted(d_list_vis)
    # next_visit
    if len(d_list_vis) >= 1:
        next_visit = d_list_vis[-1] + timedelta(days=183) #+6 months
        next_visit = str(next_visit).split(" ")[0]

    ans_hash[pop_keys] = [ans,bd_visit,oil_service,pm_visit,pm_check_date_arr,pm_check_hrs_arr,pm_check_srn_arr,b_check_date_arr,b_check_hrs_arr,b_check_srn_arr,c_check_date_arr,c_check_hrs_arr,c_check_srn_arr,d_check_date_arr,d_check_hrs_arr,d_check_srn_arr,next_bc,next_visit]


file = open("solution_updated.csv" , 'w')

#generate title 
str_title = "ESN,Visits,BD Visit,Oil Service,PM Visit" 
for i in range(max_pm) : 
    str_title += f",PM-{i+1} Visit,Hours,SRN"
for i in range(max_b) : 
    str_title += f",BC-{i+1} Visit,Hours,SRN"
for i in range(max_c) : 
    str_title += f",CC-{i+1} Visit,Hours,SRN"
for i in range(max_d) : 
    str_title += f",DC-{i+1} Visit,Hours,SRN"
str_title += ",Next BC,Next Visit"
str_title += "\n"

file.write(str_title)

for arr in numpy_df_pop : 
    str_data = f"{arr[0]},{ans_hash[arr[0]][0]},{ans_hash[arr[0]][1]},{ans_hash[arr[0]][2]},{ans_hash[arr[0]][3]}"
    for i in range(max_pm) : 
        if i < len(ans_hash[arr[0]][4]) : 
            str_data += f",{ans_hash[arr[0]][4][i]},{ans_hash[arr[0]][5][i]},{ans_hash[arr[0]][6][i]}"
        else : 
            str_data += ",0,0,0"
    for i in range(max_b) : 
        if i < len(ans_hash[arr[0]][7]) : 
            str_data += f",{ans_hash[arr[0]][7][i]},{ans_hash[arr[0]][8][i]},{ans_hash[arr[0]][9][i]}"
        else : 
            str_data += ",0,0,0"
    for i in range(max_c): 
        if i < len(ans_hash[arr[0]][10]) : 
            str_data += f",{ans_hash[arr[0]][10][i]},{ans_hash[arr[0]][11][i]},{ans_hash[arr[0]][12][i]}"
        else : 
            str_data += ",0,0,0"
    for i in range(max_d): 
        if i < len(ans_hash[arr[0]][13]) : 
            str_data += f",{ans_hash[arr[0]][13][i]},{ans_hash[arr[0]][14][i]},{ans_hash[arr[0]][15][i]}"
        else : 
            str_data += ",0,0,0"
    str_data += f",{ans_hash[arr[0]][16]},{ans_hash[arr[0]][17]}"
    str_data += "\n"
    file.write(str_data)
file.close()

# with open("solution.csv" , 'w') as f : 
#     f.write("ESN,Visits,BD Visit,Oil Service,PM Visit,B CHECK SRN,B CHECK DATE,B CHECK HOURS,C CHECK SRN,C CHECK DATE,C CHECK HOURS,D CHECK SRN,D CHECK DATE,D CHECK HOURS,NEXT BC\n")
#     for arr in numpy_df_pop:
#         f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(arr[0],ans_hash[arr[0]][0],ans_hash[arr[0]][1],ans_hash[arr[0]][2],ans_hash[arr[0]][3], \
#                                                       ans_hash[arr[0]][4],ans_hash[arr[0]][5],ans_hash[arr[0]][6],ans_hash[arr[0]][7], \
#                                                       ans_hash[arr[0]][8],ans_hash[arr[0]][9],ans_hash[arr[0]][10],ans_hash[arr[0]][11],ans_hash[arr[0]][12],ans_hash[arr[0]][13]))

    
