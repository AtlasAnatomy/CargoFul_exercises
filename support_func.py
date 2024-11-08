
import pandas as pd

# IQR Method
def trim_outliers(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return series.clip(lower=lower_bound, upper=upper_bound)

#Pivot for week number / weekday
def pivot_weekday(df_withoutGEO,location_id_filter):
    df_filtered = df_withoutGEO[df_withoutGEO['location_id'].astype(str).str.contains(location_id_filter)]

    df_pivot = df_filtered.pivot_table(
        index='week_number', 
        columns='weekday', 
        values='quantity1', 
        aggfunc='sum', 
        fill_value=0
    )

    df_pivot.reset_index(inplace=True)
    return df_pivot

#Concatenate weekday stats 
def combined_weekly_stats(locations_selected, weekly_stats):
    location_dfs = []
    
    for location_id in locations_selected:
        location_data = weekly_stats[weekly_stats['location_id'].astype(str) == str(location_id)][['weekday', 'mean', 'var']]
        
        location_data = location_data.set_index('weekday')
        location_data.columns = [f"Location_{location_id}_mean", f"Location_{location_id}_var"]
        
        location_dfs.append(location_data)

    # Concatenate
    combined_df = pd.concat(location_dfs, axis=1)
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    combined_df.sort_values(by="weekday", key=lambda column: column.map(lambda e: weekday_order.index(e)), inplace=True)
    combined_df = combined_df.fillna('-')

    return combined_df