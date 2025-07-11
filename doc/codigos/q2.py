import pandas as pd
import numpy as np
import geopandas as gpd
from datetime import datetime
import shapely.geometry
import pandas as pd
import geopandas as gpd
from datetime import datetime
import os
from shapely.geometry import Point
import numpy as np

def solve(crimes_df: gpd.GeoDataFrame, streets_df: gpd.GeoDataFrame, geometries_df: gpd.GeoDataFrame) -> None:
    
    # Define the target point
    target_point = Point(113.392723, 22.516998)
    
    # Calculate the 70 km radius
    radius = 70 * 1000  # Convert km to meters
    buffer = target_point.buffer(radius)
    
    # Filter crimes within the radius
    crimes_in_radius = crimes_df[crimes_df.geometry.within(buffer)]
    print(f"Found {len(crimes_in_radius)} crimes within the 70 km radius")
    
    # Get unique counties
    counties = crimes_in_radius['incident_county'].unique()
    print(f"Counties within the radius: {counties}")
    
    # Count crimes per county
    crime_counts = crimes_in_radius['incident_county'].value_counts()
    print("Crime counts per county:")
    print(crime_counts)
    
    # Calculate the 20% reduction
    reduced_counts = crime_counts * 0.8
    
    # Calculate the percentage change
    percentage_change = (crime_counts - reduced_counts) / crime_counts * 100
    
    # Print the results
    print("Results:")
    print(f"Original crime counts: {crime_counts}")
    print(f"Reduced crime counts (20%): {reduced_counts}")
    print(f"Percentage change: {percentage_change:.2f}%")