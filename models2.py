
from geopy.distance import geodesic
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from support_func2 import get_cluster_stats, get_cluster_stats_radius
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

#CLUSTERING KMEANS (Starting)

# Calculate the radius of a cluster
def calculate_radius(cluster_points, center):
    distances = [geodesic((lat, lon), center).km for lat, lon in cluster_points]
    return max(distances) if distances else 0


#Initial clusters

def initial_kmeans_clustering(data, n_clusters, conv, random):

    if conv=='max_iter':
        if random=='fixed':
            kmeans = KMeans(n_clusters=n_clusters, 
                    random_state=0, #to allow reproducibility
                    n_init=1,
                    init='k-means++',
                    max_iter=300)
        else:
            kmeans = KMeans(n_clusters=n_clusters, 
                    n_init=10,
                    init='k-means++',
                    max_iter=300)
    elif conv=='tol':
        if random=='fixed':
            kmeans = KMeans(n_clusters=n_clusters, 
                    random_state=0, #to allow reproducibility
                    init='k-means++',
                    n_init=1,
                    tol=300)
        else:
            kmeans = KMeans(n_clusters=n_clusters,
                    init='k-means++',
                    n_init=10,
                    tol=300)
    else:
        print('Insert convergence condition.')
        return
    
    data['cluster'] = kmeans.fit_predict(data[['latitude', 'longitude']])
    
    #Centroids
    centers = kmeans.cluster_centers_
    data['cluster_center'] = data['cluster'].apply(lambda x: (centers[x][0], centers[x][1]))
    
    return data, centers


#Heuristic for splitting

def adjust_capacity_constraints(data, max_quantity, max_points):

    new_clusters = []
    new_centroids = []
    cluster_max_number = data['cluster'].max() #to keep track of the current cluster max number assigned
    
    for cluster_id in data['cluster'].unique():
        cluster_data = data[data['cluster'] == cluster_id]
        
        # Check quantity/points
        total_quantity = cluster_data['quantity'].sum()
        total_points = len(cluster_data)

        # Original Centroid
        original_centroid = cluster_data['cluster_center'].iloc[0]
        
        # If not respected, split it
        if total_quantity > max_quantity or total_points > max_points:

            print('cluster to split due to capacity ', cluster_id, total_points, total_quantity)

            #NEW KMEANS

            #new cluster numbers
            n_subclusters = int(max(total_quantity // max_quantity, total_points // max_points) + 1)
            sub_kmeans = KMeans(n_clusters=n_subclusters, random_state=0, n_init=1, init='k-means++', max_iter=300)
            cluster_data['sub_cluster'] = sub_kmeans.fit_predict(cluster_data[['latitude', 'longitude']])
            

            #new centroids coordinates
            centers = sub_kmeans.cluster_centers_

            for sub_cluster_id in range(n_subclusters):
                
                sub_cluster_data = cluster_data[cluster_data['sub_cluster'] == sub_cluster_id]
                cluster_number=0
                
                if sub_cluster_id == 0:
                    # Use the original cluster_id 
                    sub_cluster_data['cluster'] = cluster_id
                    cluster_number = cluster_id
                else:
                    # Assign a new cluster ID
                    cluster_max_number += 1
                    sub_cluster_data['cluster'] = cluster_max_number
                    cluster_number=cluster_max_number

                new_centroids.append((cluster_number,(centers[sub_cluster_id][0], centers[sub_cluster_id][1])))
                new_clusters.append(sub_cluster_data.drop(columns='sub_cluster'))
        else:
            cluster_data['cluster'] = cluster_id  # Keep as is
            new_centroids.append((cluster_id,original_centroid))
            new_clusters.append(cluster_data)
        
    
    # Add new Clusters
    adjusted_data = pd.concat(new_clusters, ignore_index=True)
    # Add new centroids
    centroid_dict = {cluster_number: (latitude, longitude) for cluster_number, (latitude, longitude) in new_centroids}
    adjusted_data['cluster_center'] = adjusted_data['cluster'].apply(lambda cluster_number: centroid_dict.get(cluster_number, None))
    
    return adjusted_data

def enforce_radius_constraint(data, max_radius, radius_splitting):

    new_clusters = []
    new_centroids = []
    cluster_max_number = data['cluster'].max() #to keep track of the current cluster max number assigned

    for cluster_id in data['cluster'].unique():
        cluster_data = data[data['cluster'] == cluster_id]

        # Check radius
        original_centroid = cluster_data['cluster_center'].iloc[0]
        radius = calculate_radius(cluster_data[['latitude', 'longitude']].values, original_centroid)
        
        if radius > max_radius:
            print('cluster to split due to radius ',cluster_id, radius)

            #splitting method
            if radius_splitting=='double':
                n_subclusters = 2
            else:
                n_subclusters = int(radius / max_radius) + 1

            #new clusters and centroids
            sub_kmeans = KMeans(n_clusters=n_subclusters, random_state=0, n_init=1, init='k-means++', max_iter=300)
            cluster_data['sub_cluster'] = sub_kmeans.fit_predict(cluster_data[['latitude', 'longitude']])
            centers = sub_kmeans.cluster_centers_

            #reassign clusters
            for sub_cluster_id in range(n_subclusters):
                
                sub_cluster_data = cluster_data[cluster_data['sub_cluster'] == sub_cluster_id]
                cluster_number=0
                
                if sub_cluster_id == 0:
                    # Use the original cluster_id 
                    sub_cluster_data['cluster'] = cluster_id
                    cluster_number = cluster_id
                else:
                    # Assign a new cluster ID
                    cluster_max_number += 1
                    sub_cluster_data['cluster'] = cluster_max_number
                    cluster_number=cluster_max_number

                new_centroids.append((cluster_number,(centers[sub_cluster_id][0], centers[sub_cluster_id][1])))
                new_clusters.append(sub_cluster_data.drop(columns='sub_cluster'))
            
        else:
            cluster_data['cluster'] = cluster_id  # Keep as is
            new_centroids.append((cluster_id,original_centroid))
            new_clusters.append(cluster_data)
    
    # Add new Clusters
    adjusted_data = pd.concat(new_clusters, ignore_index=True)
    # Add new centroids
    centroid_dict = {cluster_number: (latitude, longitude) for cluster_number, (latitude, longitude) in new_centroids}
    adjusted_data['cluster_center'] = adjusted_data['cluster'].apply(lambda cluster_number: centroid_dict.get(cluster_number, None))
    
    return adjusted_data

def clustering_kmeans(data, initial_clusters, max_radius, max_quantity, max_points, conv, random, radius_splitting):
    
    # Initial Clustering
    data1, centers1 = initial_kmeans_clustering(data, initial_clusters, conv, random)

    data1['cluster_label'] = data1['cluster'].apply(lambda x: f'Cluster {x}')
    
    # Capacity constraints
    data2 = data1.copy()

    current_max_points, current_max_quantity, cluster_quantity_sum, cluster_sizes, quantity_stats = get_cluster_stats(data2)

    print('CLUSTERS TOTAL QUANTITIES')
    print(cluster_quantity_sum)
    print('CLUSTERS TOTAL POINTS')
    print(cluster_sizes)

    while current_max_points > max_points or current_max_quantity > max_quantity:
        
        data2 = adjust_capacity_constraints(data2, max_quantity, max_points)
        
        current_max_points, current_max_quantity, cluster_quantity_sum, cluster_sizes, quantity_stats = get_cluster_stats(data2)

        print('CLUSTERS TOTAL QUANTITIES')
        print(cluster_quantity_sum)
        print('CLUSTERS TOTAL POINTS')
        print(cluster_sizes)

    data2['cluster_label'] = data2['cluster'].apply(lambda x: f'Cluster {x}')

    # Radius constraints

    data3 = data2.copy()

    current_max_radius, clusters_radius = get_cluster_stats_radius(data3)

    print('CLUSTERS MAX RADIUS')
    print(clusters_radius)

    while current_max_radius > max_radius:
        
        data3 = enforce_radius_constraint(data3, max_radius, radius_splitting)
        
        current_max_radius, clusters_radius = get_cluster_stats_radius(data3)

        print('CLUSTERS MAX RADIUS')
        print(clusters_radius)

    data3['cluster_label'] = data3['cluster'].apply(lambda x: f'Cluster {x}')
    
    return data1, data2, data3


#TSP OR-Tools by Google
def solve_tsp(distance_matrix, cluster_locations):
    tsp_size = len(distance_matrix)
    if tsp_size <= 1:
        return {'total_distance': 0, 'route': []}

    manager = pywrapcp.RoutingIndexManager(tsp_size, 1, 0)
    routing = pywrapcp.RoutingModel(manager)
    transit_callback_index = routing.RegisterTransitCallback(lambda from_index, to_index: distance_matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)])
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_parameters)
    
    # Total distance and route
    total_distance = 0
    route = []
    if solution:
        index = routing.Start(0)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))  # Track the route
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            total_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        route.append(manager.IndexToNode(index))

    route_with_ids = [cluster_locations[i] for i in route]

    print("Route:", route_with_ids)
    print("Total Distance:", total_distance)
    
    return {'total_distance': total_distance, 'route': route_with_ids}