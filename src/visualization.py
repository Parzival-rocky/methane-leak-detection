import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

def plot_methane_distribution(data: pd.DataFrame, time_filter=None, show=True, save_path=None, tracer_column='tracer_concentration'):
    """
    Plots a scatter map of methane tracer concentration over geographical coordinates.
    
    Parameters:
      data (pd.DataFrame): DataFrame containing at least 'latitude', 'longitude', 'tracer concentration'.
      time_filter (optional): Either a specific timestamp or a tuple (start, end) to filter data on the 'Time (UTC)' column.
      show (bool): Whether to display the plot.
      save_path (str, optional): If provided, the figure will be saved to this file path.
    
    Returns:
      fig, ax: The matplotlib figure and axes objects.
    """
    # If a time_filter is provided and 'Time (UTC)' exists, filter the data accordingly.
    if time_filter and 'Time (UTC)' in data.columns:
        if isinstance(time_filter, tuple) and len(time_filter) == 2:
            data = data[(data['Time (UTC)'] >= time_filter[0]) & (data['Time (UTC)'] <= time_filter[1])]
        else:
            data = data[data['Time (UTC)'] == time_filter]
    
    lat = data['latitude']
    lon = data['longitude']
    tracer = data[tracer_column]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(lon, lat, c=tracer, cmap='viridis', s=50, edgecolor='k')
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Tracer Concentration')
    
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Methane Distribution Map')
    
    # Highlight the point with the highest tracer concentration as a potential leak source.
    if not data.empty:
        idx_max = tracer.idxmax()
        max_lat = lat.loc[idx_max]
        max_lon = lon.loc[idx_max]
        ax.plot(max_lon, max_lat, marker='*', markersize=15, color='red', label='Potential Leak Source')
        ax.legend()
    
    if save_path:
        plt.savefig(save_path)
    if show:
        plt.show()
    return fig, ax

def animate_methane_distribution(data: pd.DataFrame, interval=1000, save_path=None):
    """
    Creates an animation showing the evolution of methane tracer concentration over time.
    
    Parameters:
      data (pd.DataFrame): DataFrame containing at least 'Time (UTC)', 'latitude', 'longitude', 'tracer concentration'.
      interval (int): Delay between frames in milliseconds.
      save_path (str, optional): If provided, the animation will be saved to this file (e.g., 'animation.mp4').
    
    Returns:
      ani: The matplotlib.animation.FuncAnimation object.
    """
    # Ensure 'Time (UTC)' is a datetime object.
    if data['Time (UTC)'].dtype == 'O':
        data['Time (UTC)'] = pd.to_datetime(data['Time (UTC)'])
    
    times = np.sort(data['Time (UTC)'].unique())
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    def update(frame):
        ax.clear()
        current_time = times[frame]
        subset = data[data['Time (UTC)'] == current_time]
        lat = subset['latitude']
        lon = subset['longitude']
        tracer = subset['tracer_concentration']
        scatter = ax.scatter(lon, lat, c=tracer, cmap='viridis', s=50, edgecolor='k')
        ax.set_title(f'Methane Distribution at {current_time}')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Tracer Concentration')
        
        # Highlight the point with the maximum tracer concentration.
        if not subset.empty:
            idx_max = tracer.idxmax()
            max_lat = lat.loc[idx_max]
            max_lon = lon.loc[idx_max]
            ax.plot(max_lon, max_lat, marker='*', markersize=15, color='red', label='Potential Leak Source')
            ax.legend()
    
    ani = animation.FuncAnimation(fig, update, frames=len(times), interval=interval, repeat=True)
    
    if save_path:
        ani.save(save_path)
    
    plt.show()
    return ani

if __name__ == "__main__":
    print("Visualization module - this module provides functions for visualizing methane concentration data")
    print("Import and use this module in other scripts rather than running it directly.")
