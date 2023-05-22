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
        if i == 0:
            column = l
        elif i > 1:
            csv_list.append(l)
        i = i + 1

    f.close()

    #for i in range(6):
    #    column.append(' ')

    df = pd.DataFrame(csv_list, columns = column)
    df = df.sort_values(by='startDate' ,ascending=True)

    # mapping raw_data to participant_data
    df.rename(columns = {'creationDate' : 'timestamp'}, inplace = True)
    df.rename(columns = {'device' : 'device_id'}, inplace = True)

    participant_data = pd.DataFrame(df['timestamp'], columns=['timestamp'])
    participant_data['device_id'] = df['device_id']

    if sensor == "APPLE_HEARTRATE":
      participant_data['heartrate'] = df[ df['type'] == "HeartRate" ]['value']

    if sensor == "APPLE_STEPCOUNT":
      participant_data['stepcount'] = df[ df['type'] == "StepCount" ]['value']

    s = participant_data['device_id'][0]
    idx = s.find('HKDevice') + 10
    val = s[idx:idx+11]
    participant_data['device_id'] = val

    participant_data = participant_data.dropna(axis=0)

    return(participant_data)

