import pandas as pd
import numpy as np
import geopandas as gpd
from datetime import datetime
import shapely.geometry
import os
from datetime import datetime
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def solve(crimes_df: gpd.GeoDataFrame, streets_df: gpd.GeoDataFrame, geometries_df: gpd.GeoDataFrame) -> None:
    
    # Define the target coordinates
    target_lat = 22.516998
    target_lon = 113.392723
    
    # Create a point geometry for the target location
    target_point = Point(target_lon, target_lat)
    
    # Calculate the 70 km radius buffer
    buffer = target_point.buffer(70e3)
    
    # Filter crimes within the buffer
    crimes_in_area = crimes_df[
        crimes_df.geometry.within(buffer)
    ].copy()
    
    # Get the current crime count
    current_crimes = len(crimes_in_area)
    
    # Calculate the new crime count with 20% reduction
    new_crimes = current_crimes * 0.8
    
    # Calculate the percentage change
    percentage_change = (current_crimes - new_crimes) / current_crimes * 100
    
    # Print the results
    print(f"Current crime count in the 70 km radius: {current_crimes}")
    print(f"New crime count with 20% reduction: {new_crimes:.0f}")
    print(f"Percentage change: {percentage_change:.2f}%")