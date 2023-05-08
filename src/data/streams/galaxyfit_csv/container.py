from pathlib import Path
import pandas as pd
import yaml
import csv
import os


def pull_data(data_configuration, device, sensor, container, columns_to_download):
    print("-----------------------For Debugging---------------------")
    print("data_configuration: ", data_configuration) # { 'FOLDER': 'data/external/galaxyfit_csv }
    print("device: ", device) # 'p01'
    print("sensor: ", sensor) # galaxyfit_heartrate
    print("container: ", container) # heartrate
    print("columns_to_download: ", columns_to_download)

    current_dir = os.getcwd() 
    p = "./" + data_configuration['FOLDER'] + '/' + container
    print("path: ", p)

    print("---------------------------------------------------------")

    # open csv file
    try: 
        f = open(p)
    except:
        raise FileNotFoundError("can not find the file")

    reader = csv.reader(f)
    csv_list = []

    i = 0
    for l in reader:
        if i > 0:
            if i == 1:
                colunm = l
    
            if i > 1:
                del l[-1]
                csv_list.append(l)
        i = i + 1

    f.close()

    if sensor == "GALAXYFIT_HEARTRATE":
        df = pd.DataFrame(csv_list, columns = colunm)
        df.rename(columns = {'com.samsung.health.heart_rate.start_time' : 'timestamp'}, inplace = True)
        df.rename(columns = {'com.samsung.health.heart_rate.deviceuuid' : 'device_id'}, inplace = True)
        df.rename(columns = {'com.samsung.health.heart_rate.heart_rate' : 'heartrate'}, inplace = True)

        participant_data = pd.DataFrame(df['timestamp'], columns=['timestamp'])
        # participant_data = pd.DataFrame(df['local_date_time'], columns=['local_date_time'])
        participant_data['device_id'] = df['device_id']
        participant_data['heartrate'] = df['heartrate']
    
    if sensor == "GALAXYFIT_STEPCOUNT":
        df = pd.DataFrame(csv_list, columns = colunm)

        df.rename(columns = {'com.samsung.health.step_count.start_time' : 'timestamp'}, inplace = True)
        df.rename(columns = {'com.samsung.health.step_count.count' : 'step_count'}, inplace = True)
        df.rename(columns = {'com.samsung.health.step_count.distance' : 'distance'}, inplace = True)
        df.rename(columns = {'com.samsung.health.step_count.deviceuuid' : 'device_id'}, inplace = True)

        participant_data = pd.DataFrame(df['timestamp'], columns=['timestamp'])
        # participant_data = pd.DataFrame(df['local_date_time'], columns=['local_date_time'])
        participant_data['step_count'] = df['step_count']
        participant_data['distance'] = df['distance']
        participant_data['device_id'] = df['device_id']

    len = participant_data.shape[0]
    # print(len)

    for i in range(len):
      temp = participant_data['timestamp'][i]
      participant_data['timestamp'][i] = temp.replace(".000", "")

    print(participant_data['timestamp'][0])
    return(participant_data)

