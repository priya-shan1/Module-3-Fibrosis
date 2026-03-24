'''Module 3: count black and white pixels and compute the percentage of white pixels in a .jpg image and extrapolate points'''

from termcolor import colored
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd
import time
start_time = time.perf_counter()
# Load the images you want to analyze
filenames = [
    r"/Users/priya/Documents/Comp_Bio/GitHub/Module-3-Fibrosis/images/MASK_SK658 Llobe ch010039.jpg",
    r"/Users/priya/Documents/Comp_Bio/GitHub/Module-3-Fibrosis/images/MASK_SK658 Slobe ch010066.jpg",
    r"/Users/priya/Documents/Comp_Bio/GitHub/Module-3-Fibrosis/images/MASK_SK658 Slobe ch010147.jpg",
    r"/Users/priya/Documents/Comp_Bio/GitHub/Module-3-Fibrosis/images/MASK_SK658 Slobe ch010110.jpg",
    r"/Users/priya/Documents/Comp_Bio/GitHub/Module-3-Fibrosis/images/MASK_SK658 Slobe ch010130.jpg",
    r"/Users/priya/Documents/Comp_Bio/GitHub/Module-3-Fibrosis/images/MASK_SK658 Slobe ch010114.jpg",
]

#filenames = [r"C:\Users\dance\OneDrive - University of Virginia\Computational BME\Module-3-Fibrosis\images\MASK_Sk658 Llobe ch010039.jpg", r"C:\Users\dance\OneDrive - University of Virginia\Computational BME\Module-3-Fibrosis\images\MASK_Sk658 Llobe ch010067.jpg", r"C:\Users\dance\OneDrive - University of Virginia\Computational BME\Module-3-Fibrosis\images\MASK_SK658 Slobe ch010147.jpg", r"C:\Users\dance\OneDrive - University of Virginia\Computational BME\Module-3-Fibrosis\images\MASK_SK658 Slobe ch010110.jpg", r"C:\Users\dance\OneDrive - University of Virginia\Computational BME\Module-3-Fibrosis\images\MASK_SK658 Slobe ch010130.jpg", r"C:\Users\dance\OneDrive - University of Virginia\Computational BME\Module-3-Fibrosis\images\MASK_SK658 Slobe ch010114.jpg"]
# Enter the depth of each image (in the same order that the images are listed above; you can find these in the .csv file provided to you which is tilted: "Filenames and Depths for Students")

depths = [
    15,
    1000,
    3000,
    5300,
    7000,
    9900
]

# Results storage
results = []

# Single loop for all logic
for file, depth in zip(filenames, depths):
    img = cv2.imread(file, 0)
    
    if img is None:
        print(colored(f"Warning: Could not load {file}", "red"))
        continue

    # Use a binary threshold
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    
    # Vectorized counting
    white_count = np.count_nonzero(binary)  # Faster than np.sum(binary == 255)
    total_pixels = binary.size
    black_count = total_pixels - white_count
    white_percent = (white_count / total_pixels) * 100

    # Print results immediately
    print(colored(f"File: {file}", "red"))
    print(f"White: {white_count} | Black: {black_count}")
    print(f"Fibrosis: {white_percent:.2f}% | Depth: {depth} microns\n")

    # Store data for CSV
    results.append({
        'Filenames': file,
        'Depths': depth,
        'White Counts': white_count,
        'White percents': white_percent
    })

# Create DataFrame and Export
df = pd.DataFrame(results)
df.to_csv('Percent_White_Pixels.csv', index=False)

print(colored("Success: 'Percent_White_Pixels.csv' created.", "green"))

print("The .csv file 'Percent_White_Pixels.csv' has been created.")

'''the .csv writing subroutine ends here'''
end_time = time.perf_counter()

execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

##############
# LECTURE 2: UNCOMMENT BELOW

# # Interpolate a point: given a depth, find the corresponding white pixel percentage

# interpolate_depth = float(input(colored(
#     "Enter the depth at which you want to interpolate a point (in microns): ", "yellow")))

# x = depths
# y = white_percents

# # You can also use 'quadratic', 'cubic', etc.
# i = interp1d(x, y, kind='linear')
# interpolate_point = i(interpolate_depth)
# print(colored(
#     f'The interpolated point is at the x-coordinate {interpolate_depth} and y-coordinate {interpolate_point}.', "green"))

# depths_i = depths[:]
# depths_i.append(interpolate_depth)
# white_percents_i = white_percents[:]
# white_percents_i.append(interpolate_point)


# # make two plots: one that doesn't contain the interpolated point, just the data calculated from your images, and one that also contains the interpolated point (shown in red)
# fig, axs = plt.subplots(2, 1)

# axs[0].scatter(depths, white_percents, marker='o', linestyle='-', color='blue')
# axs[0].set_title('Plot of depth of image vs percentage white pixels')
# axs[0].set_xlabel('depth of image (in microns)')
# axs[0].set_ylabel('white pixels as a percentage of total pixels')
# axs[0].grid(True)


# axs[1].scatter(depths_i, white_percents_i, marker='o',
#                linestyle='-', color='blue')
# axs[1].set_title(
#     'Plot of depth of image vs percentage white pixels with interpolated point (in red)')
# axs[1].set_xlabel('depth of image (in microns)')
# axs[1].set_ylabel('white pixels as a percentage of total pixels')
# axs[1].grid(True)
# axs[1].scatter(depths_i[len(depths_i)-1], white_percents_i[len(white_percents_i)-1],
#                color='red', s=100, label='Highlighted point')


# # Adjust layout to prevent overlap
# plt.tight_layout()
# plt.show()
