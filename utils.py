import pandas as pd
import xml.etree.ElementTree as ET

def parse_tcx(file):
    ns = {'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
    root = ET.parse(file).getroot()
    trackpoints = root.findall('.//tcx:Trackpoint', ns)

    data = []
    for pt in trackpoints:
        time_elem = pt.find('tcx:Time', ns)
        hr_elem = pt.find('tcx:HeartRateBpm/tcx:Value', ns)
        dist_elem = pt.find('tcx:DistanceMeters', ns)

        if time_elem is None:
            continue

        time = pd.to_datetime(time_elem.text)
        heart = int(hr_elem.text) if hr_elem is not None else None
        dist = float(dist_elem.text) / 1000 if dist_elem is not None else None
        data.append({'time': time, 'heart_rate': heart, 'distance_km': dist})

    df = pd.DataFrame(data).dropna()
    df['elapsed_min'] = (df['time'] - df['time'].min()).dt.total_seconds() / 60
    df['pace_min_per_km'] = df['elapsed_min'] / df['distance_km']
    return df

def summarize_run(df):
    return {
        '距離 (km)': round(df['distance_km'].max(), 2),
        '時間 (分)': round(df['elapsed_min'].max(), 2),
        '平均ペース (分/km)': round(df['pace_min_per_km'].mean(), 2),
        '平均心拍数': round(df['heart_rate'].mean(), 1),
        '最高心拍数': int(df['heart_rate'].max())
    }
