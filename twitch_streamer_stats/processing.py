import requests 
import json 

url = "https://api.streamersonglist.com/v1/streamers"
streamer_name = "cornyears"
rest_query = "playHistory"
response_limit = "size=100000"
rest_cmd_url = url+"/"+streamer_name+"/"+rest_query+"?"+response_limit
rest_api_response = requests.get(rest_cmd_url)

if rest_api_response.status_code != 200 :
    raise Exception("Communcation with REST API gone bad , please check error code {}".format(rest_api_response.status_code))


response_json = rest_api_response.json() #type dict

chat_requests = {}
for data in response_json["items"] : 
    if len(data["requests"]) != 0 :
        #print("**********")
        #print(data)
        if data["requests"][0]["name"] != "" :
            if data["requests"][0]["name"] not in chat_requests.keys() :
                chat_requests[data["requests"][0]["name"]] = 1
            else :
                chat_requests[data["requests"][0]["name"]] += 1


#TODO : plot the chat requests data 
# from bokeh.plotting import figure, output_file, show

# output_file('test.html')
# p = figure(plot_width=400, plot_height=400)
# y_axis =[chat_requests[x] for x in chat_requests.keys() ]
# x_axis = [ x for x in range(1,len(chat_requests.keys())+1)]
# p.vbar(x=x_axis, width=0.5, bottom=0,
#        top= y_axis, color="firebrick")

# show(p)
