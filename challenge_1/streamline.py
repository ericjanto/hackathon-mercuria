import json
import os
import pandas as pd
import re
import requests

from geopy.distance import geodesic
from rich.progress import Progress
from typing import Tuple

class AutomatedReport:
    def __init__(self, imo: str, start_date: str, end_date: str):
        with Progress() as p:
            t = p.add_task('[green]Creating automated report...', total=3)  
            self.imo = imo
            self.start_date = start_date
            self.end_date = end_date
            print("Fetching data...")
            self.res_df = fetch_all_imo_data(imo, start_date, end_date)
            p.advance(t)
            print("Calculating distance...")
            self.total_dist = calculate_overall_distance(df)
            p.advance(t)
            print("Calculating velocity...")
            self.avg_velocity = self.total_dist / self.res_df.shape[0]
            p.advance(t)


    def __str__(self):
        return f"Automated report for IMO {self.imo} voyage from {self.start_date} to {self.end_date}:\nTotal dist: {self.total_dist}, velocity: {self.avg_velocity}"



def get_valid_input(input_descriptor: str, pattern: str) -> str:
    current = input(input_descriptor)
    while not re.findall(pattern, current):
        print(f"Input needs to be of this format: {pattern}")
        current = input(input_descriptor)
    return current

def fetch_all_imo_data(imo: str, start_date: str, end_date: str):
    path = f"ais-hourly-{imo}-{start_date}-{end_date}.json"

    if os.path.isfile(path):
        print("Loading from locally cached data instead of calling API 🌳✅")
        with open(path, 'r') as f:
            return pd.json_normalize(json.load(f)["results"])
    else:
        url = f"https://api.hackathon.mercuria-apps.com/api/ais-hourly/?start_date={start_date}&end_date={end_date}&page_size=10000&imo={imo}"
        headers = {
            "Authorization": "Token f1048ff37ed94fbdfe5df4798d5860ca4c18b13c",
        }
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            res = r.json()
            if len(res["results"]) == 0:
                print(f"No data available for dates {start_date} - {end_date}")
            else:
                with open(path, "w") as f:
                    f.write(r.text)
                return pd.json_normalize(res["results"])

def calculate_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calculates the distance between two coordinates, returns km.
    """
    return geodesic(coord1, coord2).km

def calculate_overall_distance(df: pd.DataFrame) -> float:
    df.sort_values(by=['position_timestamp'], inplace=True)
    df_lat = df['ais_lat'].tolist()
    df_lon = df['ais_lon'].tolist()
    total_distance = 0
    for i in range(len(df_lat)-1):
        total_distance += calculate_distance((df_lat[i], df_lon[i]), (df_lat[i+1], df_lon[i+1]))
    return total_distance

if __name__ == '__main__':
    imo = get_valid_input(input_descriptor="IMO: ", pattern=r'^[0-9]{7}')
    start_date = get_valid_input(input_descriptor="Start date: ", pattern=r'\d{4}-\d{2}-\d{2}')
    end_date = get_valid_input(input_descriptor="End date: ", pattern=r'\d{4}-\d{2}-\d{2}')
    # imo = 9643271
    # start_date = '2022-08-01'
    # end_date = '2022-08-30'

    df = fetch_all_imo_data(imo, start_date, end_date)
    # df.to_csv("test.csv", index=False)
    report = AutomatedReport(imo, start_date, end_date)
    print(report)