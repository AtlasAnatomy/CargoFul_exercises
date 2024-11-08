import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from support_func import pivot_weekday
import warnings

def location3D(df_GEO):
    
    fig = make_subplots(rows=1, cols=2,
                        specs=[[{'type': 'scatter3d'}, {'type': 'scatter3d'}]],
                        subplot_titles=("Quantity Volumes", "Events Count"))
    
    fig.add_trace(go.Scatter3d(
        x=df_GEO['longitude'],
        y=df_GEO['latitude'],
        z=df_GEO['quantity'],
        mode='markers',
        marker=dict(
            size=5,
            color=df_GEO['quantity'],
            colorscale='Viridis',
            colorbar=dict(
                title='Quantity',
                tickvals=[df_GEO['quantity'].min(), df_GEO['quantity'].max()],
                ticktext=[f"{df_GEO['quantity'].min():.2f}", f"{df_GEO['quantity'].max():.2f}"],
                len=0.75,
                x=0.45,
                xanchor='left'
            )
        ),
        text=df_GEO['location_id'],
        hovertemplate="Location ID: %{text}<br>Latitude: %{y}<br>Longitude: %{x}<br>Quantity: %{z}",
        showlegend=False
    ), row=1, col=1)
    
    for i in range(len(df_GEO)):
        fig.add_trace(go.Scatter3d(
            x=[df_GEO['longitude'].iloc[i], df_GEO['longitude'].iloc[i]],
            y=[df_GEO['latitude'].iloc[i], df_GEO['latitude'].iloc[i]],
            z=[0, df_GEO['quantity'].iloc[i]],
            mode='lines',
            line=dict(color='blue', width=3),
            showlegend=False,
            hoverinfo="none"
        ), row=1, col=1)
    
    fig.add_trace(go.Scatter3d(
        x=df_GEO['longitude'],
        y=df_GEO['latitude'],
        z=df_GEO['events_count'],
        mode='markers',
        marker=dict(
            size=5,
            color=df_GEO['events_count'],
            colorscale='Cividis',
            colorbar=dict(
                title='Events',
                tickvals=[df_GEO['events_count'].min(), df_GEO['events_count'].max()],
                ticktext=[f"{df_GEO['events_count'].min():.0f}", f"{df_GEO['events_count'].max():.0f}"],
                len=0.75,
                x=1.2,
                xanchor='right'
            )
        ),
        text=df_GEO['location_id'],
        hovertemplate="Location ID: %{text}<br>Latitude: %{y}<br>Longitude: %{x}<br>Events Count: %{z}",
        showlegend=False
    ), row=1, col=2)
    
    for i in range(len(df_GEO)):
        fig.add_trace(go.Scatter3d(
            x=[df_GEO['longitude'].iloc[i], df_GEO['longitude'].iloc[i]],
            y=[df_GEO['latitude'].iloc[i], df_GEO['latitude'].iloc[i]],
            z=[0, df_GEO['events_count'].iloc[i]],
            mode='lines',
            line=dict(color='orange', width=3),
            showlegend=False,
            hoverinfo="none"
        ), row=1, col=2)
    
    fig.update_layout(
        title="Quantity Volumes and Events Count by Location Geo-spatial Data",
        scene=dict(
            xaxis_title="Longitude",
            yaxis_title="Latitude",
            zaxis_title="Quantity"
        ),
        scene2=dict(
            xaxis_title="Longitude",
            yaxis_title="Latitude",
            zaxis_title="Events Count"
        ),
        width=1200,
        height=600,
        coloraxis_showscale=False,
        showlegend=False
    )
    
    return fig


def quantity_trends(locations_selected, df, weekly_data, daily_data, df_withoutGEO):

    # rows
    num_rows = len(locations_selected)
    num_cols = 4
    # Plot data for each location_id
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 5 * num_rows))
    fig.suptitle('Quantity for Each Location', fontsize=16)
    axes = axes.flatten()
    
    # seaborn colors
    pastel_colors = sns.color_palette("pastel", 3)
    

    for i, location_id in enumerate(locations_selected):
        location_data = df[df['location_id'].astype(str) == location_id]
    
        # 1. Period data bar plot
        event_data = location_data[location_data['is_event'] == 1]
        axes[i*num_cols].bar(event_data['delivery_date'], event_data['quantity1'], color=pastel_colors[0], label='Events')
        axes[i*num_cols].set_xlabel('Date')
        axes[i*num_cols].set_ylabel('Quantity')
        axes[i*num_cols].set_title(f'Location {location_id} - Period')
        axes[i*num_cols].legend()
    
        if not event_data.empty:
            axes[i*num_cols].set_xticks(event_data['delivery_date'])
            axes[i*num_cols].set_xticklabels(event_data['delivery_date'], rotation=45, ha='right')
    
        # 2. Weekly data bar plot
        weekly_loc_data = weekly_data[weekly_data['location_id'].astype(str) == location_id]
        non_zero_weeks = weekly_loc_data[weekly_loc_data['quantity1'] > 0]
        axes[i*num_cols + 1].bar(non_zero_weeks['week_number'], non_zero_weeks['quantity1'], color=pastel_colors[1])
        axes[i*num_cols + 1].set_xlabel('Week Number')
        axes[i*num_cols + 1].set_ylabel('Quantity')
        axes[i*num_cols + 1].set_title(f'Location {location_id} - Weekly Quantity')
        axes[i*num_cols + 1].set_xticks(non_zero_weeks['week_number'])
        axes[i*num_cols + 1].set_xticklabels(non_zero_weeks['week_number'], rotation=45, ha='right')
        
        # 3. Daily data box plot and violin plot
        pivot = pivot_weekday(df_withoutGEO, location_id)
        pivot_melted = pivot.melt(id_vars=["week_number"], 
                                  value_vars=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                  var_name="weekday", 
                                  value_name="quantity")
        
        sns.boxplot(x='weekday', y='quantity', data=pivot_melted, ax=axes[i*num_cols + 2])

        # Set labels and title
        axes[i*num_cols + 2].set_xlabel('Day of the Week')
        axes[i*num_cols + 2].set_ylabel('Quantity')
        axes[i*num_cols + 2].set_title(f'Location {location_id} - Weekday Box')
        weekday=pivot_melted['weekday'].unique()
        unique_weekdays = pivot_melted['weekday'].unique()
        axes[i*num_cols + 2].set_xticks(range(len(unique_weekdays)))
        axes[i*num_cols + 2].set_xticklabels(unique_weekdays, rotation=45, ha='right')

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            sns.violinplot(x='weekday', y='quantity', data=pivot_melted, split=True, palette="Set2",ax=axes[i*num_cols + 3], inner="box",cut=0)
        
        # Set labels and title
        axes[i*num_cols + 3].set_xlabel('Day of the Week')
        axes[i*num_cols + 3].set_ylabel('Quantity')
        axes[i*num_cols + 3].set_title(f'Location {location_id} - Weekday Violin')
        axes[i*num_cols + 3].set_xticks(range(len(unique_weekdays)))
        axes[i*num_cols + 3].set_xticklabels(unique_weekdays, rotation=45, ha='right')
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    return plt

