import numpy as np
import shapely.geometry
import os
from datetime import datetime
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def solve(crimes_df: gpd.GeoDataFrame, streets_df: gpd.GeoDataFrame, geometries_df: gpd.GeoDataFrame) -> None:
    
    # Define the central point
    central_point = Point(113.392723, 22.516998)
    
    # Calculate the 70 km radius
    radius = 70 * 1000  # Convert km to meters
    buffer = central_point.buffer(radius)
    
    # Get neighboring counties
    neighboring_counties = geometries_df[
        geometries_df.geometry.intersects(buffer)
    ].geom_type.unique()
    
    print(f"Neighboring counties: {neighboring_counties}")
    
    # Filter crimes within the buffer
    crimes_in_buffer = crimes_df[
        crimes_df.geometry.within(buffer)
    ].copy()
    
    print(f"Total crimes in buffer: {len(crimes_in_buffer)}")
    
    # Calculate current average crime rate
    current_avg = crimes_in_buffer['case_type'].value_counts().mean()
    print(f"Current average crime rate: {current_avg:.2f}")
    
    # Simulate 20% reduction
    reduced_crimes = crimes_in_buffer.sample(frac=0.8)
    reduced_avg = reduced_crimes['case_type'].value_counts().mean()
    print(f"Simulated reduced crime rate: {reduced_avg:.2f}")
    
    # Calculate percentage change
    change = ((current_avg - reduced_avg) / current_avg) * 100
    print(f"Percentage change: {change:.2f}%")
    
    # Print final result
    print(f"The average crime rate in neighboring counties would decrease by {change:.2f}% if crime at the central point were reduced by 20%.")"]