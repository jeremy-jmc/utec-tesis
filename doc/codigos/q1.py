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
    guangdong_crimes = crimes_df[(crimes_df['incident_province'] == 'Guangdong Province') & 
                                  (crimes_df['formatted_datetime'].dt.year == 2019)].copy()
    
    # Step 2: Define night-time hours (6 PM to 6 AM)
    guangdong_crimes['hour'] = guangdong_crimes['formatted_datetime'].dt.hour
    night_time_crimes = guangdong_crimes[(guangdong_crimes['hour'] < 6) | (guangdong_crimes['hour'] >= 18)]
    
    # Step 3: Count total crimes in Guangdong Province for 2019
    total_crimes_count = guangdong_crimes.shape[0]
    
    # Step 4: Count night-time crimes
    night_time_crimes_count = night_time_crimes.shape[0]
    
    # Step 5: Calculate the percentage drop in overall crime
    if total_crimes_count > 0:
        percentage_drop = (night_time_crimes_count / total_crimes_count) * 100
    else:
        percentage_drop = 0  # No crimes means no percentage drop
    
    # Step 6: Prepare the result message
    result = (f"If all night-time crimes in Guangdong Province were completely prevented in 2019, "
              f"the overall crime would drop by {percentage_drop:.2f}%. "
              f"This represents {night_time_crimes_count} night-time crimes prevented out of {total_crimes_count} total crimes.")
    
    return result