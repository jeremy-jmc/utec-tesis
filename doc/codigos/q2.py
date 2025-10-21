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
    # Step 1: Define the central point of interest
    central_point = Point(113.392723, 22.516998)

    # Step 2: Convert all GeoDataFrames to EPSG:3857 for accurate distance calculations
    crimes_df = crimes_df.to_crs(epsg=3857)
    geometries_df = geometries_df.to_crs(epsg=3857)

    # Step 3: Create a buffer of 1000 km around the central point
    buffer_distance = 1000000  # 1000 km in meters
    central_buffer = central_point.buffer(buffer_distance)

    # Step 4: Identify all counties within the buffer
    counties_within_buffer = geometries_df[geometries_df.geometry.within(central_buffer)]

    # Step 5: Filter crimes that occur within the counties identified
    crimes_within_buffer = crimes_df[crimes_df.geometry.within(central_buffer)]

    # Step 6: Count the number of crimes in the buffer
    total_crimes = len(crimes_within_buffer)

    # Step 7: Calculate the decrease in crime if the central point's crime falls by 20%
    decrease_percentage = 0.20
    decrease_amount = total_crimes * decrease_percentage

    # Step 8: Calculate the new total crime count after the decrease
    new_total_crimes = total_crimes - decrease_amount

    # Step 9: Prepare the result message
    result = f"If crime at the central point fell by 20%, the overall crime would decrease by {int(decrease_amount)} incidents, resulting in a new total of {int(new_total_crimes)} crimes across all counties within 1000 km."

    return result