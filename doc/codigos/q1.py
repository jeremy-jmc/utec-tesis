import pandas as pd
import numpy as np
import geopandas as gpd
from datetime import datetime
import shapely.geometry
import os

def solve(crimes_df: gpd.GeoDataFrame, streets_df: gpd.GeoDataFrame, geometries_df: gpd.GeoDataFrame) -> None:
    
    # Filter for Guangdong Province crimes in 2019
    guangdong_crimes = crimes_df[
        (crimes_df['incident_province'] == 'Guangdong Province') &
        (crimes_df['formatted_datetime'].dt.year == 2019)
    ]
    
    print(f"Total crimes in Guangdong Province during 2019: {len(guangdong_crimes)}")
    
    # Filter for night-time crimes (6 PM to 6 AM)
    night_crimes = guangdong_crimes[
        (guangdong_crimes['formatted_datetime'].dt.hour >= 18) | 
        (guangdong_crimes['formatted_datetime'].dt.hour < 6)
    ]
    
    print(f"Night-time crimes in Guangdong Province during 2019: {len(night_crimes)}")
    
    # Calculate percentage reduction
    total_crimes = len(guangdong_crimes)
    night_crimes_count = len(night_crimes)
    
    if total_crimes == 0:
        print("No crimes in Guangdong Province during 2019")
    else:
        reduction_percentage = (night_crimes_count / total_crimes) * 100
        print(f"Percentage reduction in overall crime if all night-time crimes were prevented: {reduction_percentage:.2f}%")
