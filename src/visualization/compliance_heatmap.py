import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.graph_objects as go
import datetime

def getComplianceMatrix(dates, compliance_bins):
    compliance_matrix = []
    for date in dates:
        date_bins = compliance_bins[compliance_bins["local_date"] == date]
        compliance_matrix.append(((date_bins["has_row"]>0).astype(int)).tolist())
    return compliance_matrix

def getComplianceHeatmap(dates, compliance_matrix, pid, output_path, bin_size):
    bins_per_hour = int(60 / bin_size)
    x_axis_labels = ["{0:0=2d}".format(x // bins_per_hour) + ":" + \
                    "{0:0=2d}".format(x % bins_per_hour * bin_size) for x in range(24 * bins_per_hour)]
    plot = go.Figure(data=go.Heatmap(z=compliance_matrix,
                                     x=x_axis_labels,
                                     y=dates,
                                     colorscale=[[0, "rgb(255, 255, 255)"],[1, "rgb(120, 120, 120)"]]))
    plot.update_layout(title="Five minutes has_row heatmap for " + pid)
    pio.write_html(plot, file=output_path, auto_open=False)

# get current patient id
pid = snakemake.params["pid"]
sensors_dates = []
sensors_five_minutes_row_is = pd.DataFrame()
for sensor_path in snakemake.input:
    sensor_data = pd.read_csv(sensor_path)

    # create a dataframe contains 2 columns: local_date_time, has_row
    sensor_data["has_row"] = [1]*sensor_data.shape[0]
    sensor_data["local_date_time"] = pd.to_datetime(sensor_data["local_date_time"])
    sensed_bins = sensor_data[["local_date_time", "has_row"]]

    # get the first date and the last date of current sensor
    start_date = datetime.datetime.combine(sensed_bins["local_date_time"][0].date(), datetime.time(0,0,0))
    end_date = datetime.datetime.combine(sensed_bins["local_date_time"][sensed_bins.shape[0]-1].date(), datetime.time(23,59,59))

    # add the above datetime with has_row=0 to our dataframe
    sensed_bins.loc[sensed_bins.shape[0], :] = [start_date, 0]
    sensed_bins.loc[sensed_bins.shape[0], :] = [end_date, 0]
    # get bins with 5 min
    sensor_five_minutes_row_is = pd.DataFrame(sensed_bins.resample("5T", on="local_date_time")["has_row"].sum())
    # merge current sensor with previous sensors
    if sensors_five_minutes_row_is.empty:
        sensors_five_minutes_row_is = sensor_five_minutes_row_is
    else:
        sensors_five_minutes_row_is = pd.concat([sensors_five_minutes_row_is, sensor_five_minutes_row_is]).groupby("local_date_time").sum()


sensors_five_minutes_row_is.reset_index(inplace=True)
# resample again to impute missing dates
sensors_five_minutes_row_is_successive = pd.DataFrame(sensors_five_minutes_row_is.resample("5T", on="local_date_time")["has_row"].sum())

# get sorted date list
sensors_five_minutes_row_is_successive.reset_index(inplace=True)
sensors_five_minutes_row_is_successive["local_date"] = sensors_five_minutes_row_is_successive["local_date_time"].apply(lambda x: x.date())
dates = list(set(sensors_five_minutes_row_is_successive["local_date"]))
dates.sort()
compliance_matrix = getComplianceMatrix(dates, sensors_five_minutes_row_is_successive)

# get heatmap
getComplianceHeatmap(dates, compliance_matrix, pid, snakemake.output[0], 5)