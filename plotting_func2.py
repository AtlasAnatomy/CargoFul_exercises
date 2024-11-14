import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import matplotlib.pyplot as plt

def initial_scatter(df):
    # min/max longitude/latitude
    min_longitude, max_longitude = df['longitude'].min(), df['longitude'].max()
    min_latitude, max_latitude = df['latitude'].min(), df['latitude'].max()
    
    # Scatter plot + Distributions
    fig = px.scatter(
        df,
        x='longitude',
        y='latitude',
        hover_name='location_id', 
        hover_data={'quantity': True, 'occurrences': True},
        title='2D Map of Locations with Distributions',
        labels={'longitude': 'Longitude', 'latitude': 'Latitude'},
        marginal_x="histogram",
        marginal_y="histogram"
    )
    
    # Markers
    fig.update_traces(
        marker=dict(
            line=dict(
                color='black',
                width=1 
            )
        )
    )
    
    # Layout
    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(
            range=[min_longitude - 1, max_longitude + 1],
            scaleanchor='y', scaleratio=1
        ),
        yaxis=dict(
            range=[min_latitude - 1, max_latitude + 1],
        ),
        title=dict(x=0.5),
        width=800,
        height=600
    )
    
    return fig


def outliers_scatter(df):
    # min/max longitude/latitude
    min_longitude, max_longitude = df['longitude'].min(), df['longitude'].max()
    min_latitude, max_latitude = df['latitude'].min(), df['latitude'].max()
    
    # Scatter plot + Distributions with color based on 'is_outlier'
    fig = px.scatter(
        df,
        x='longitude',
        y='latitude',
        color='is_outlier',  # Color based on the 'is_outlier' column
        color_discrete_map={True: 'red', False: 'green'},  # Mapping colors
        hover_name='location_id', 
        hover_data={'quantity': True, 'occurrences': True},
        title='2D Map of Locations with Outliers',
        labels={'longitude': 'Longitude', 'latitude': 'Latitude'}
    )
    
    # Markers
    fig.update_traces(
        marker=dict(
            line=dict(
                color='black',
                width=1 
            )
        )
    )
    
    # Layout
    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(
            range=[min_longitude - 1, max_longitude + 1],
            scaleanchor='y', scaleratio=1
        ),
        yaxis=dict(
            range=[min_latitude - 1, max_latitude + 1],
        ),
        title=dict(x=0.5),
        width=800,
        height=600
    )
    
    return fig


def scatter_hub(df):
    
    # min/max longitude/latitude
    min_longitude, max_longitude = df['longitude'].min(), df['longitude'].max()
    min_latitude, max_latitude = df['latitude'].min(), df['latitude'].max()
    
    # Scatter plot + Distributions
    fig = px.scatter(
        df,
        x='longitude',
        y='latitude',
        hover_name='hub_id', 
        hover_data={'location_ids': True},
        title='2D Map of Locations with Distributions',
        labels={'longitude': 'Longitude', 'latitude': 'Latitude'},
        marginal_x="histogram",
        marginal_y="histogram"
    )
    
    # Markers
    fig.update_traces(
        marker=dict(
            line=dict(
                color='black',
                width=1 
            )
        )
    )
    
    # Layout
    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(
            range=[min_longitude - 1, max_longitude + 1],
            scaleanchor='y', scaleratio=1
        ),
        yaxis=dict(
            range=[min_latitude - 1, max_latitude + 1],
        ),
        title=dict(x=0.5),
        width=800,
        height=600
    )
    
    return fig


def plot_clusters_with_centers(df1):
    
    # Extract clusters + centers coordinates
    df = df1.copy()
    df = df.sort_values(by='cluster')
    centers = pd.DataFrame(df['cluster_center'].tolist(), columns=['latitude', 'longitude'])
    
    
    min_longitude, max_longitude = df['longitude'].min(), df['longitude'].max()
    min_latitude, max_latitude = df['latitude'].min(), df['latitude'].max()

    #Colors
    unique_clusters = sorted(df['cluster'].unique())
    num_clusters = len(unique_clusters)
    color_list = (
    list(plt.get_cmap('tab20').colors) + 
    list(plt.get_cmap('tab20b').colors) + 
    list(plt.get_cmap('tab20c').colors) + 
    list(plt.get_cmap('Set1').colors) + 
    list(plt.get_cmap('Set2').colors) + 
    list(plt.get_cmap('Set3').colors) + 
    list(plt.get_cmap('Accent').colors)
    )

    # Limit to 100 colors
    color_list = color_list[:100]

    df['cluster_color'] = df['cluster'].apply(lambda x: color_list[x])
    df['cluster_label'] = df['cluster'].apply(lambda x: f'Cluster {x}')
    
    # Scatter plot for locations with dynamic colors based on the cluster
    fig = px.scatter(
        df,
        x='longitude',
        y='latitude',
        color='cluster_color',  # Use the new cluster color column
        hover_name='location_id', 
        hover_data={'cluster_label': True, 'quantity': True, 'occurrences': True},  # Display the cluster label
        title='2D Map of Locations + Clusters',
        labels={'longitude': 'Longitude', 'latitude': 'Latitude'}
    )
    
    fig.update_traces(
        marker=dict(
            line=dict(
                color='black',  # Border color for data points
                width=0.5          # Border width
            ),
            opacity=1       # Set transparency for data point markers (50% transparent)
        ),
        selector=dict(mode='markers')  # Apply to marker traces only
    )

    # Add markers for cluster centers (as 'x' markers) with a higher zorder to ensure they appear on top
    fig.add_trace(
        go.Scatter(
            x=centers['longitude'],
            y=centers['latitude'],
            mode='markers',
            marker=dict(
                symbol='star', 
                color='yellow',  # color of the center markers
                size=12,  # size of the center markers
                line=dict(width=1, color='black')  # Border for the center markers
            ),
            name='Centroids'
        )
    )
    
    # Layout
    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(
            range=[min_longitude - 1, max_longitude + 1],
            scaleanchor='y', scaleratio=1
        ),
        yaxis=dict(
            range=[min_latitude - 1, max_latitude + 1],
        ),
        title=dict(x=0.5),
        width=800,
        height=600,
        legend=dict(
            title="Legend",
            x=0.85,  # Position of the legend
            y=1,
            tracegroupgap=0,  # Group related traces together in the legend
        ),
    )

    for i, cluster in enumerate(unique_clusters):
        fig.data[i].name = f'Cluster {cluster}'

    d = fig.to_dict()

    for i in range(len(d["data"]) - 1):
        d["data"][i]["type"] = "scatter"
    
    return d

def sse_cluster_trends(clusters, sse_values, n_cluster):
    
    plt.figure(figsize=(15, 6))
    
    # Plot 1: SSE against the Initial clusters 
    plt.subplot(1, 3, 1)
    plt.plot(clusters, sse_values, marker='o', color='b')
    plt.xlabel('Initial Clusters')
    plt.ylabel('SSE')
    plt.title('SSE Trend & Initial Clusters')
    plt.grid(True)
    
    # Plot 2: SSE against the Total Clusters
    plt.subplot(1, 3, 2)
    plt.plot(n_cluster, sse_values, marker='o', color='r')
    plt.xlabel('Total Clusters')
    plt.ylabel('SSE')
    plt.title('SSE Trend & Total Clusters')
    plt.grid(True)
    
    # Plot 3: Total Clusters against Initial clusters
    plt.subplot(1, 3, 3)
    plt.plot(clusters, n_cluster, marker='o', color='g')
    plt.xlabel('Initial Clusters')
    plt.ylabel('Total Clusters')
    plt.title('Initial Clusters vs Total Clusters')
    plt.grid(True)
    
    plt.tight_layout()
    return plt

def TSP_route_plot(clusters_list, colors, route_distances, final_cluster, df):
    
    # Determine the number of rows and columns for subplots (3 per row)
    num_clusters = len(clusters_list)
    num_cols = 3
    num_rows = (num_clusters + num_cols - 1) // num_cols  # Calculate rows needed
    
    # Create subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))
    axes = axes.flatten()  # Flatten for easy indexing
    
    for i, cluster_id in enumerate(clusters_list):
        route = route_distances[i]  # Get the route for the current cluster (including centroid at start and end)
        
        # Get centroid coordinates (tuple: (latitude, longitude))
        centroid_coords = final_cluster[final_cluster['cluster'] == cluster_id]['cluster_center'].iloc[0]
        centroid_lat, centroid_lon = centroid_coords  # Unpack centroid coordinates
        
        # Get route coordinates, excluding the centroid (index 0 at start and end)
        route_locs = route[1:-1]
        route_coords = df[df['location_id'].isin(route_locs)][['location_id', 'latitude', 'longitude']]
        route_coords = route_coords.set_index('location_id').loc[route_locs]  # Ensure ordered by route
        
        # Extract latitude and longitude
        latitudes = route_coords['latitude'].values
        longitudes = route_coords['longitude'].values
        
        # Plot on the specific subplot
        ax = axes[i]
        color = colors[i % len(colors)]  # Use the expanded color list
        
        # Plot the route path with color and connect it back to the centroid
        ax.plot([centroid_lon] + list(longitudes) + [centroid_lon], 
                [centroid_lat] + list(latitudes) + [centroid_lat], 
                marker='o', linestyle='-', color=color, label="Route Path")
        
        # Plot the centroid distinctly
        ax.plot(centroid_lon, centroid_lat, marker='D', color='r', markersize=8, label="Centroid")
        
        # Annotate each location_id on the route
        '''for j, location_id in enumerate(route_locs):
            ax.text(longitudes[j], latitudes[j], str(location_id), fontsize=2, ha='right')'''
        
        # Set title and labels
        ax.set_title(f"TSP Route for Cluster {cluster_id}")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.legend()
        
    # Hide any unused subplots if clusters aren't a multiple of three
    for j in range(i + 1, num_rows * num_cols):
        fig.delaxes(axes[j])
    
    # Display the entire grid
    plt.tight_layout()

    return plt


