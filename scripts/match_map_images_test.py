import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

# Load your map image as a numpy array
map_image = plt.imread('grand teton park map.jpg')

# Convert the image to grayscale if it's not already
if map_image.ndim == 3:
    map_image = np.mean(map_image, axis=2)

# Apply a Gaussian filter to smooth the image
smoothed_image = ndimage.gaussian_filter(map_image, sigma=2)

# Find local maxima (peaks)
peaks = ndimage.maximum_filter(smoothed_image, size=20)
peaks = np.logical_and(peaks == smoothed_image, smoothed_image > np.mean(smoothed_image))
peak_indices = np.where(peaks)

# Visualize the results
plt.imshow(map_image, cmap='gray')
plt.plot(peak_indices[1], peak_indices[0], 'ro', markersize=5)
plt.savefig('map_peaks_output.png')  # Save to file
plt.close()  # Clean up the plot