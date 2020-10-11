import pandas as pd 
import numpy as np
from datetime import datetime
from datetime import date
from dateutil import parser
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
df2 = df_visits[['ESN/Alternator No.','Opened']]
print("test2 :")
print(df2.head())

#TODO : implement scheduling functionality
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
    #key = esn number , val = start date 
    population_hash[arr[0]] = arr[1]
    population_hash_end[arr[0]] = arr[2]
    



# for i in population_hash.keys():
#     print("************")
#     print(i)
#     print(population_hash[i])
#     print("************")    

visits_hash = {}
for arr in numpy_df_vis :
    if arr[0] in visits_hash.keys():
        visits_hash[arr[0]].append(arr[1])
    else :
        visits_hash[arr[0]] = [arr[1]]

# print ("visits hash : ")
# print (visits_hash)

# hash format  esn ->visits : '25316320': ['2019-01-28 12:59:46', '2019-02-22 11:46:05', '2019-03-22 11:19:42', '2019-04-29 13:58:58', '2019-05-21 09:40:26', '2019-06-28 11:05:00', '2019-07-25 10:18:35', '2019-08-27 16:45:33', '2019-09-03 10:21:11']

ans_hash = {}
for pop_keys in population_hash.keys():
    start_date = population_hash[pop_keys]
    start_date = start_date.split(" ")[0]
    end_date = population_hash_end[pop_keys]
    end_date = end_date.split(" ")[0]
    
    ans = 0
    if pop_keys in visits_hash.keys():
        visits_info = visits_hash[pop_keys]
        
        for each_visit in visits_info :
            each_visit = each_visit.split(" ")[0]
            if (each_visit >= start_date ) and (each_visit <= end_date) :
                ans = ans + 1 
    ans_hash[pop_keys] = ans

# for each_key in ans_hash.keys():
#     print("******************")
#     print (each_key)
#     print ( ans_hash[each_key])
#     print("******************")

with open("solution.csv" , 'w') as f : 
    f.write("ESN,Visits\n")
    for arr in numpy_df_pop:
        f.write("%s,%s\n"%(arr[0],ans_hash[arr[0]]))

#create calender schedule 


#print(visits_hash)

# for i in visits_hash.keys():
#     print("************")
#     print(i)
#     print(visits_hash[i])
#     print("************")
    

# for arr in numpy_df_pop :
#    for ele in arr :
#        print(ele) 
    
