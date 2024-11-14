import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from geopy.distance import geodesic

# Calculate the radius of a cluster
def calculate_radius2(cluster_points, center, points):
    
    distances = [geodesic((lat, lon), center).km for lat, lon in cluster_points]
    
    # Find the maximum distance and its index
    max_distance = max(distances)
    max_distance_index = distances.index(max_distance)
    
    # Get the point and corresponding coordinates (lat, lon)
    max_point = points[max_distance_index]  # Assuming 'points' contains the actual data/points for each location
    corresponding_coords = cluster_points[max_distance_index]
    
    return max_distance, max_point, corresponding_coords

def calculate_distances(cluster_points, center):
    distances = [geodesic((lat, lon), center).km for lat, lon in cluster_points]
    return distances

# Haversine formula
def haversine_matrix(df):
    locations = np.radians(df[['latitude', 'longitude']].to_numpy()) #convert longitude/latitude in radians
    latitudes = locations[:, 0][:, np.newaxis]
    longitudes = locations[:, 1][:, np.newaxis]
    dlat = latitudes - latitudes.T
    dlon = longitudes - longitudes.T
    a = np.sin(dlat / 2) ** 2 + np.cos(latitudes) * np.cos(latitudes.T) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    earth_radius = 6378  # Radius of the Earth in km
    return earth_radius * c

def create_cluster_summary(data):
    
    # Group by the 'cluster'
    cluster_summary = data.groupby('cluster').agg({
        'location_id': lambda x: list(x), # list of location_ids
        'cluster_center': 'first'  # Cluster center longitude/latitude
    }).reset_index()

    # modify the new dataframe
    cluster_summary[['latitude', 'longitude']] = pd.DataFrame(cluster_summary['cluster_center'].tolist(), index=cluster_summary.index)
    cluster_summary.rename(columns={'cluster': 'hub_id', 'location_id': 'location_ids'}, inplace=True)
    cluster_summary.drop(columns=['cluster_center'], inplace=True)
    
    return cluster_summary


def haversine_matrix_hubs(data, hubs):
    
    kmeans = KMeans(n_clusters=hubs,
                    random_state=0,  # to allow reproducibility
                    n_init=10,
                    max_iter=300)

    data['cluster'] = kmeans.fit_predict(data[['latitude', 'longitude']])

    # Centroids
    centers = kmeans.cluster_centers_
    data['cluster_center'] = data['cluster'].apply(lambda x: (centers[x][0], centers[x][1]))

    cluster_df = create_cluster_summary(data)

    locations = np.radians(cluster_df[['latitude', 'longitude']].to_numpy())  # convert longitude/latitude in radians
    latitudes = locations[:, 0][:, np.newaxis]
    longitudes = locations[:, 1][:, np.newaxis]
    dlat = latitudes - latitudes.T
    dlon = longitudes - longitudes.T
    a = np.sin(dlat / 2) ** 2 + np.cos(latitudes) * np.cos(latitudes.T) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    earth_radius = 6378  # Radius of the Earth in km
    return earth_radius * c, cluster_df

def cluster_statistics(clustered_data):
    
    # Group by cluster
    cluster_groups = clustered_data.groupby('cluster')
    
    # Calculate row count per cluster
    cluster_sizes = cluster_groups.size()
    max_rows = cluster_sizes.max()
    min_rows = cluster_sizes.min()
    avg_rows = cluster_sizes.mean()
    
    # Calculate statistics for 'quantity' and 'occurrences'
    quantity_sum = cluster_groups['quantity'].sum()
    quantity_stats = quantity_sum.agg(['max', 'min', 'mean'])
    occurrences_stats = cluster_groups['occurrences'].agg(['max', 'min', 'mean'])
    

    distance_stats = []
    for cluster, group in cluster_groups:
        center = group['cluster_center'].iloc[0]  # centroid
        cluster_points = list(zip(group['latitude'], group['longitude']))  # List of (latitude, longitude) tuples
        distances = calculate_distances(cluster_points, center)
        
        max_distance = max(distances)
        min_distance = min(distances)
        avg_distance = sum(distances) / len(distances)
        
        distance_stats.append({
            'cluster': cluster,
            'Max Distance': max_distance,
            'Min Distance': min_distance,
            'Avg Distance': avg_distance
        })

    # Convert distance statistics to a DataFrame for further aggregation
    distance_stats_df = pd.DataFrame(distance_stats).set_index('cluster')
    
    # Find the max of max distances, min of min distances, and average of average distances
    max_of_max_distances = distance_stats_df['Max Distance'].max()
    min_of_min_distances = distance_stats_df['Min Distance'].min()
    avg_of_avg_distances = distance_stats_df['Avg Distance'].mean()

    # Assemble statistics into a dictionary for DataFrame creation
    stats = {
        'row_count': [max_rows, min_rows, avg_rows],
        'quantity': [quantity_stats['max'].max(), quantity_stats['min'].min(), quantity_stats['mean'].mean()],
        'occurrences': [occurrences_stats['max'].max(), occurrences_stats['min'].min(), occurrences_stats['mean'].mean()],
        'distance': [max_of_max_distances, min_of_min_distances, avg_of_avg_distances]
    }
    
    # Convert stats dictionary to DataFrame with 'max', 'min', 'average' as the index
    stats_df = pd.DataFrame(stats, index=['max', 'min', 'average'])

    return stats_df

def concatenate_stats(stats_df_noCon, stats_df_wCC, stats_df_wCR):
    
    # Concatenate the DataFrames
    concatenated_df = pd.concat(
        [stats_df_noCon, stats_df_wCC, stats_df_wCR],
        keys=['Without Constraints', 'With Constraints [C]','With Constraints [C+R]']
    )
    
    concatenated_df.index.names = ['Condition', 'Statistic']
    
    return concatenated_df

def get_cluster_stats(data2):
        
        cluster_groups = data2.groupby('cluster')
        cluster_sizes = cluster_groups.size()
        cluster_quantity_sum = cluster_groups['quantity'].sum()
        quantity_stats = cluster_quantity_sum.agg(['max', 'min', 'mean'])
        
        current_max_points = cluster_sizes.max()
        current_max_quantity = quantity_stats['max'].max()
        
        return current_max_points, current_max_quantity, cluster_quantity_sum, cluster_sizes, quantity_stats

def get_cluster_stats_radius(data3):

        clusters = data3['cluster'].unique()
        clusters_maxradius=[]
        clusters_maxpoint=[]
        clusters_maxpoint_cord=[]
        centers = []

        for cluster_id in clusters:
            
            cluster_data = data3[data3['cluster'] == cluster_id]
            center = cluster_data['cluster_center'].iloc[0]
            radius, max_point, corresponding_coords = calculate_radius2(cluster_data[['latitude', 'longitude']].values, center, cluster_data['location_id'].values)
            
            clusters_maxradius.append(radius)
            clusters_maxpoint.append(max_point)
            clusters_maxpoint_cord.append(corresponding_coords)
            centers.append(center)
        
        clusters_radius = pd.DataFrame({
        'cluster': clusters,
        'centroids': centers,
        'max_radius': clusters_maxradius,
        'max_point': clusters_maxpoint,
        'max_point_coord':clusters_maxpoint_cord
        })
        
        current_max_radius = max(clusters_maxradius)
        
        return current_max_radius, clusters_radius


def calculate_sse(final_cluster):
    """
    Calculate the Sum of Squared Errors (SSE) for a clustering result.
    
    """
    sse = 0.0
    for _, row in final_cluster.iterrows():
        # Get the latitude and longitude of the data point
        point = (row['latitude'], row['longitude'])
        # Get the cluster center (latitude, longitude) for the assigned cluster
        center = row['cluster_center']
        
        # Calculate the squared distance between the point and the cluster center
        distance = geodesic(point, center).km  # Calculate distance in kilometers
        squared_distance = distance ** 2       # Square the distance
        
        # Add to SSE
        sse += squared_distance
        
    return sse

# Build distance matrix for OR-Tools
def create_distance_matrix(cluster_locations, filtered_matrix):
    distance_matrix = []
    for loc_id_from in cluster_locations:
        row = []
        for loc_id_to in cluster_locations:
            row.append(filtered_matrix[str(loc_id_to)].loc[loc_id_from])
        distance_matrix.append(row)
    return distance_matrix