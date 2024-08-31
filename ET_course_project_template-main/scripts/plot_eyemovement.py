import os

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import seaborn as sns

"""
change Hyperparameters according to your needs.
The plots are saved in resume/subject-{id}/
"""
############## HYPERPARAMETER ###################
subject_id = 12
do_plot_eyemovement = True
do_plot_xy = True
do_plot_heatmap = True
##################################################



# Load the data
df = pd.read_csv(f'ET_course_project_template-main/data/raw/subject-{subject_id}/subject-{subject_id}.tsv', delimiter='\t', low_memory=False)

# Get all indices for which the USER column is not NaN
user_indices = df[df['USER'].notna()].index.tolist()

# Get the corresponding values for the indices
user_values_dict = {idx: df.at[idx, 'USER'] for idx in user_indices}


# Get the index range for each resume
def get_index_range(user_values_dict):
    image_ranges = {}
    current_start = None
    current_image = None
    for idx, event in sorted(user_values_dict.items()):
        if "DISPLAYED" in event:
            current_start = idx
            current_image = event.split(' DISPLAYED')[0]
        elif "HIDDEN" in event:
            if current_image is None:
                continue
            elif current_image in event:
                image_ranges[current_image] = (current_start, idx)
                current_start = None
                current_image = None
    return image_ranges


image_range = get_index_range(user_values_dict)

# Edge reference for resume: left edge 0.3151, right edge 0.68490, top edge 0.0370, bottom edge 0.9630
left_edge = 0.3151
right_edge = 0.68490
top_edge = 0.0370
bottom_edge = 0.9630


# Function to clamp and adjust gaze coordinates
def adjust_coordinates(x, y, x_drift, y_drift, left_edge, right_edge, top_edge, bottom_edge, img_width, img_height):
    # drift_correction
    x = x + x_drift
    y = y + y_drift
    # Clamp the coordinates to the bounds of the resume
    x = max(min(x, right_edge), left_edge)
    y = max(min(y, bottom_edge), top_edge)

    # Map the clamped coordinates to the image size
    adjusted_x = (x - left_edge) / (right_edge - left_edge) * img_width
    adjusted_y = (y - top_edge) / (bottom_edge - top_edge) * img_height

    return adjusted_x, adjusted_y


# Function to calculate drift based on previous 500 entries
def calculate_drift(df, start_index, num_entries=60):
    # Ensure we do not go out of bounds
    start_fixation_index = max(0, start_index - num_entries)
    fixation_data = df.loc[start_fixation_index:start_index-1]  #
    x_drift = fixation_data['BPOGX'].mean() - 0.5
    y_drift = fixation_data['BPOGY'].mean() - 0.5
    return x_drift, y_drift


# Function to average every n samples
def average_samples(df, n=10):
    numeric_cols = df.select_dtypes(include='number').columns
    return df[numeric_cols].groupby(df.index // n).mean()


def plot_eyemovement(image_name, img, adjusted_coords):
    plt.figure(figsize=(10, 6))
    plt.imshow(img)
    plt.plot(adjusted_coords['x'], adjusted_coords['y'], c='black', label='Movement Path', alpha=0.5)
    plt.scatter(adjusted_coords['x'].iloc[0], adjusted_coords['y'].iloc[0], s=50, c='green', label='First Gaze Point')
    plt.scatter(adjusted_coords['x'].iloc[-1], adjusted_coords['y'].iloc[-1], s=50, c='yellow', label='Last Gaze Point')

    # Identify and plot border points in red
    border_points = adjusted_coords[
        (adjusted_coords['x'] == 0) |
        (adjusted_coords['x'] == img.shape[1]) |
        (adjusted_coords['y'] == 0) |
        (adjusted_coords['y'] == img.shape[0])
    ]
    plt.scatter(border_points['x'], border_points['y'], s=50, c='red', label='Border Points')

    plt.title(f'Eye Movement for Image {image_name}')
    plt.axis('on')
    plt.legend(loc='lower right', framealpha=0.5)
    os.makedirs(f"ET_course_project_template-main/plots/eyemovement/subject-{subject_id}", exist_ok=True)
    plt.savefig(f"ET_course_project_template-main/plots/eyemovement/subject-{subject_id}/{image_name.lower()}")
    plt.show()

def plot_xy(image_name, duration, data_subset):
    # Additional plot for BPOGX and BPOGY over duration
    plt.figure(figsize=(10, 6))
    plt.plot(duration, data_subset['BPOGX'], label='BPOGX', alpha=0.7)
    plt.plot(duration, data_subset['BPOGY'], label='BPOGY', alpha=0.7)
    plt.xlabel('Duration')
    plt.ylabel('Gaze Coordinates')
    plt.title(f'Gaze Coordinates over Duration for Image {image_name}')
    plt.legend()
    os.makedirs(f"ET_course_project_template-main/plots/eyemovement/subject-{subject_id}", exist_ok=True)
    plt.savefig(f"ET_course_project_template-main/plots/eyemovement/subject-{subject_id}/{image_name.lower()}_time_series.jpg")
    plt.show()
    print(1)


def plot_kde(image_name, img, adjusted_coords, x_max, y_max):
    dummy_points = pd.DataFrame({
        'x': [0, x_max],
        'y': [y_max, 0]
    })
    adjusted_coords = pd.concat([adjusted_coords, dummy_points])

    plt.figure(figsize=(10, 6))
    plt.imshow(img)  # Ensure the image spans the specified rang

    sns.kdeplot(
        x=adjusted_coords['x'],
        y=adjusted_coords['y'],
        fill=True,
        cmap="viridis",
        thresh=0,
        levels=100,
        alpha=0.3  # Adjust transparency here
    )

    # Set axis limits
    plt.xlim(0, x_max)
    plt.ylim(y_max, 0)

    plt.colorbar(label='Density')
    plt.title(f'KDE of Eye Movement for Image {image_name}')
    plt.axis('on')
    os.makedirs(f"ET_course_project_template-main/plots/eyemovement/subject-{subject_id}", exist_ok=True)
    plt.savefig(f"ET_course_project_template-main/plots/eyemovement/subject-{subject_id}/{image_name.lower()}_kde.jpg")
    plt.show()






# Plot all images
for idx, (image_name, image_range) in enumerate(image_range.items()):
    img = mpimg.imread(f"resume/images/{image_name.lower()}")
    data_subset = df.loc[image_range[0]:image_range[1]]
    # Only plot the valid points
    data_subset = data_subset[data_subset['BPOGV'] == 1]
    data_subset = data_subset[data_subset['FPOGV'] == 1]
    # Calculate drift correction using the previous 500 entries before the image display period
    x_drift, y_drift = 0, 0
    # Average every 10 samples in data_subset
    data_subset_avg = average_samples(data_subset, 1)

    # Calculate the width and height of the image
    img_width = img.shape[1]
    img_height = img.shape[0]
    # Adjust gaze coordinates to match the resume's position
    adjusted_coords = data_subset_avg.apply(
        lambda row: adjust_coordinates(row['BPOGX'], row['BPOGY'], x_drift, y_drift, left_edge, right_edge, top_edge,
                                       bottom_edge, img_width, img_height), axis=1)
    adjusted_coords = pd.DataFrame(adjusted_coords.tolist(), columns=['x', 'y'])


    # Calculate duration from the first time point
    start_time = data_subset['TIME'].iloc[0]
    duration = data_subset['TIME'] - start_time

    if do_plot_eyemovement:
        plot_eyemovement(image_name, img, adjusted_coords)
    if do_plot_xy:
        plot_xy(image_name, duration, data_subset)
    if do_plot_heatmap:
        plot_kde(image_name, img, adjusted_coords, x_max=img_width, y_max=img_height)