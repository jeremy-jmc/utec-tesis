import calendar
import json
import os
import random
import re
import warnings
from collections import Counter, defaultdict
from datetime import datetime, time, timedelta
import geopandas as gpd
import numpy as np
import pandas as pd
from pandas.tseries.offsets import MonthEnd
from shapely import geometry
from shapely.geometry import (LineString,MultiLineString,MultiPoint,MultiPolygon,Point,Polygon,box,mapping)
from shapely.ops import nearest_points, unary_union
from tqdm import tqdm

def solve(crimes_df: gpd.GeoDataFrame, streets_df: gpd.GeoDataFrame, geometries_df: gpd.GeoDataFrame) -> str:
    # Step 1: Filter for crimes in Guangdong Province for the year 2019
    guangdong_crimes_2019 = crimes_df[(crimes_df['incident_province'] == 'Guangdong Province') & 
                                       (crimes_df['formatted_datetime'].dt.year == 2019)]
    
    # Step 2: Count crimes per county
    county_crime_counts = guangdong_crimes_2019['incident_county'].value_counts().reset_index()
    county_crime_counts.columns = ['incident_county', 'crime_count']
    
    # Step 3: Identify the top 10 safest counties based on crime counts
    safest_counties = county_crime_counts.nlargest(10, 'crime_count')
    
    # Step 4: Get the crime count for Zhongshan City
    zhongshan_crime_count = safest_counties[safest_counties['incident_county'] == 'Zhongshan City']['crime_count'].values[0]
    
    # Step 5: Calculate the new crime count after a 15% increase
    new_crime_count = zhongshan_crime_count * 1.15
    
    # Step 6: Update the crime count for Zhongshan City
    safest_counties.loc[safest_counties['incident_county'] == 'Zhongshan City', 'crime_count'] = new_crime_count
    
    # Step 7: Reorder the counties based on the updated crime counts
    updated_rankings = safest_counties.sort_values(by='crime_count', ascending=False)
    
    # Step 8: Prepare the result message
    result = "Top 10 safest counties in Guangdong Province (2019):\n"
    for index, row in updated_rankings.iterrows():
        result += f"{row['incident_county']}: {row['crime_count']} crimes\n"
    
    # Step 9: Include the impact of the increase in Zhongshan City
    result += f"Zhongshan City's crime count increased from {zhongshan_crime_count} to {new_crime_count}.\n"
    
    return result