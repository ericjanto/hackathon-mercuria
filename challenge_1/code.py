import json
import pandas as pd
import requests
import statistics

from datetime import date, datetime
from geopy.distance import geodesic
from typing import List, Tuple, Union
def get_ais_hourly(start_date: date, end_date: date) -> Union[str, None]:
    """
    Retrieves hourly AIS data for the given date-range.

    Writes the data to file and then returns file path if successful.
    """
    sdate_str, edate_str = str(start_date), str(end_date)
    url = f"https://api.hackathon.mercuria-apps.com/api/ais-hourly/?start_date={sdate_str}&end_date={edate_str}"
    headers = {
        "Authorization": "Token f1048ff37ed94fbdfe5df4798d5860ca4c18b13c",
    }

    payload = {'start_date': start_date, 'end_date': end_date}

    r = requests.get(url=url, headers=headers)

    path = None
    if r.status_code == 200:
        path = f'ais-hourly-{sdate_str}-{edate_str}.json'
        with open(path, 'w') as f:
            f.write(r.text)
    else:
        print('Dates not in data.')
        print(r.json())
    return path
def calculate_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calculates the distance between two coordinates, returns km.
    """
    return geodesic(coord1, coord2).km
def calculate_velocity_1h(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    d = calculate_distance(coord1, coord2)
    return d/1

def json_file_to_df(path: str) -> pd.DataFrame:
    with open(path, 'r') as f:
        json_contents = json.load(f)
        return pd.json_normalize(json_contents['results'])

def is_roughly_eta(this_eta: datetime, original_eta: datetime) -> bool:
    """
    Determines whether a date is more or less around the original ETA.
    """
    return abs(this_eta - original_eta) <= 5

def calculate_speed(speed_points):

    vessel_speed_point = 0
    for i in range(len(speed_points)):
        vessel_speed_point += speed_points[i]

    average_speed = vessel_speed_point/len(speed_points)
    return average_speed


# August 2022
start_date = date(2022, 8, 1)
end_date = date(2022, 8, 30)

path = 'data.json'

df = json_file_to_df(path)
df.sort_values(by=['position_timestamp'], inplace=True)

df_lat = df['ais_lat'].tolist()
df_lon = df['ais_lon'].tolist()
df_speed = df['ais_speed'].tolist()

# print(df_speed[0])

total_distance = 0
dist = []

for i in range(len(df_lat)-1):
    distance = calculate_distance((df_lat[i], df_lon[i]), (df_lat[i+1], df_lon[i+1]))
    total_distance += distance
    dist.append(distance)

distances = df[['imo', 'position_timestamp']][:-1]
distances['dist'] = dist
# vessel_average_speed = calculate_speed(df_speed)

vessel_speed_point = 0
for i in range(len(df_speed)):
    vessel_speed_point += float(df_speed[i])

average_speed = vessel_speed_point/len(df_speed)

# print(average_speed)
print(total_distance/len(df_lat))
# print(type(distances))
# distances.to_csv('distance.csv')
# for_median = distances['dist'].tolist()

# print(statistics.median(for_median))


