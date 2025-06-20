import pandas as pd
import numpy as np
import geopandas as gpd
from datetime import datetime
import shapely.geometry
import pandas as pd
import geopandas as gpd
from datetime import datetime
import os

def solve(crimes_df: gpd.GeoDataFrame, streets_df: gpd.GeoDataFrame, geometries_df: gpd.GeoDataFrame) -> None:
    
    # Step 1: Filter for Guangdong Province and 2019 crimes
    guangdong_crimes = crimes_df[
        (crimes_df['incident_province'] == 'Guangdong Province') & 
        (crimes_df['year'] == 2019)
    ]
    
    print(f"Found {len(guangdong_crimes)} crimes in Guangdong Province for 2019")
    
    # Step 2: Count crimes per county
    county_crime_counts = guangdong_crimes.groupby('incident_county').size().reset_index(name='crime_count')
    
    # Step 3: Sort by crime count in descending order
    county_crime_counts = county_crime_counts.sort_values('crime_count', ascending=False)
    
    # Step 4: Get current top 10 safest counties
    current_top_10 = county_crime_counts.head(10)
    print("Current Top 10 Safest Counties:")
    print(current_top_10[['incident_county', 'crime_count']])
    
    # Step 5: Filter for Zhongshan City crimes
    zhongshan_crimes = guangdong_crimes[guangdong_crimes['incident_city'] == 'Zhongshan City']
    
    # Step 6: Calculate adjusted crime counts
    adjusted_counts = county_crime_counts.copy()
    adjusted_counts.loc[adjusted_counts['incident_county'] == 'Zhongshan City', 'crime_count'] *= 1.15
    
    # Step 7: Sort adjusted counts
    adjusted_top_10 = adjusted_counts.sort_values('crime_count', ascending=False).head(10)
    
    # Step 8: Print results
    print("Adjusted Top 10 Safest Counties (15% increase in Zhongshan City):")
    print(adjusted_top_10[['incident_county', 'crime_count']])