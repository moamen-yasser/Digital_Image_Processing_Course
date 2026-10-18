# ==============================================================================
# Digital Image Processing (DIP) - Section 3
# Spatial Domain Transformations:
# 1. Brightness Adjustment (Vectorized Array Math vs. Pixel-by-Pixel Loop)
# 2. Contrast Stretching (Min-Max Normalization per RGB Channel)
# 3. Gamma Correction (Vectorized Power-Law Transformation)
# 4. Gamma Correction (Manual Pixel-by-Pixel Loop)
# 5. Histogram Equalization (Grayscale CDF & LUT Mapping)
# ==============================================================================

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


# ------------------------------------------------------------------------------
# 1. Brightness Adjustment (Vectorized vs. Pixel-by-Pixel Loop)
# ------------------------------------------------------------------------------
print("--- 1. Brightness Adjustment ---")

# Load image
img = Image.open("image.png").convert("RGB")
arr = np.array(img)   # shape (H, W, 3)
H, W, C = arr.shape
print("Image shape:", arr.shape)

# Brightness factor (bias)
bias = 50

# Method 1: Vectorized (array math)
bright_arr = arr.astype(np.int32) + bias
bright_arr = np.clip(bright_arr, 0, 255).astype(np.uint8)

# Method 2: Pixel-by-pixel loop (manual way)
bright_manual = np.zeros_like(arr, dtype=np.uint8)

for i in range(H):
    for j in range(W):
        for k in range(C):
            new_val = int(arr[i, j, k]) + bias
            # clamp 0-255
            if new_val > 255:
                new_val = 255
            elif new_val < 0:
                new_val = 0
            bright_manual[i, j, k] = new_val

# Display
plt.figure(figsize=(12, 6))

plt.subplot(1, 3, 1)
plt.imshow(arr)
plt.title("Original")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(bright_arr)
plt.title(f"Brightened (Array Math, +{bias})")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(bright_manual)
plt.title(f"Brightened (Pixel by Pixel, +{bias})")
plt.axis("off")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------------------------
# 2. Contrast Stretching (Min-Max Normalization per Channel)
# ------------------------------------------------------------------------------
print("\n--- 2. Contrast Stretching ---")

# 1. Load the colored image
image = Image.open("image.png").convert("RGB")
img = np.array(image)

# 2. Apply contrast stretching to each RGB channel
stretched = np.zeros_like(img)

for c in range(3):
    channel = img[:, :, c].astype(np.float32)

    r_min = np.min(channel)
    r_max = np.max(channel)

    if r_max > r_min:
        stretched[:, :, c] = np.clip((channel - r_min) * 255.0 / (r_max - r_min), 0, 255).astype(np.uint8)
    else:
        stretched[:, :, c] = channel.astype(np.uint8)

# 3. Display original and enhanced images
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title("Original Color Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(stretched)
plt.title("Contrast-Stretched Color Image")
plt.axis("off")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------------------------
# 3. Gamma Correction (Vectorized Power-Law Transformation)
# ------------------------------------------------------------------------------
print("\n--- 3. Gamma Correction (Vectorized) ---")

# 1. Load the colored image
image = Image.open("image.png").convert("RGB")
img = np.array(image)

# 2. Set the gamma value
gamma = 0.5

# 3. Normalize pixel values to [0, 1]
normalized = img.astype(np.float32) / 255.0

# 4. Apply gamma correction to all RGB channels
corrected = np.power(normalized, gamma)

# 5. Convert values back to [0, 255]
corrected = np.clip(corrected * 255.0, 0, 255).astype(np.uint8)

# 6. Display original and corrected images
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title("Original Color Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(corrected)
plt.title(f"Gamma-Corrected Image (Vectorized, γ={gamma})")
plt.axis("off")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------------------------
# 4. Gamma Correction (Manual Pixel-by-Pixel Loop)
# ------------------------------------------------------------------------------
print("\n--- 4. Gamma Correction (Pixel by Pixel) ---")

# 1. Load the color image
image = Image.open("image.png").convert("RGB")
img = np.array(image)

# Get image dimensions
height, width, channels = img.shape

# 2. Set gamma
gamma = 0.5

# Create output image
corrected_manual = np.zeros_like(img)

# 3. Apply gamma correction pixel by pixel
for i in range(height):
    for j in range(width):
        for c in range(3):
            pixel = img[i, j, c] / 255.0

            value = pixel ** gamma

            corrected_manual[i, j, c] = int(
                np.clip(value * 255.0, 0, 255)
            )

# 4. Display original and corrected images
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title("Original Color Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(corrected_manual)
plt.title(f"Pixel-by-Pixel Gamma (γ={gamma})")
plt.axis("off")

plt.tight_layout()
plt.show()


# ------------------------------------------------------------------------------
# 5. Histogram Equalization (Grayscale CDF & LUT Mapping)
# ------------------------------------------------------------------------------
print("\n--- 5. Histogram Equalization ---")

# 1. Load the image in grayscale (using histogramImage.png)
image = Image.open("histogramImage.png").convert("L")
img = np.array(image)

# 2. Calculate the histogram
hist = np.bincount(img.ravel(), minlength=256)

# 3. Calculate the cumulative distribution function (CDF)
cdf = hist.cumsum()

# 4. Find the first nonzero CDF value
cdf_min = cdf[cdf > 0].min()
total_pixels = img.size

# 5. Create the equalization lookup table (LUT)
if total_pixels > cdf_min:
    lut = np.round(
        (cdf - cdf_min) * 255.0 / (total_pixels - cdf_min)
    )
    lut = np.clip(lut, 0, 255).astype(np.uint8)
else:
    lut = np.arange(256, dtype=np.uint8)

# 6. Apply histogram equalization
equalized = lut[img]

# 7. Display original and equalized images
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(img, cmap="gray", vmin=0, vmax=255)
plt.title("Original Grayscale Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(equalized, cmap="gray", vmin=0, vmax=255)
plt.title("Histogram Equalized Image")
plt.axis("off")

plt.tight_layout()
plt.show()

# 8. Display histograms
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.hist(img.ravel(), bins=256, range=(0, 256), color="steelblue", edgecolor="none")
plt.title("Original Histogram")
plt.xlabel("Intensity Value (0-255)")
plt.ylabel("Pixel Count")

plt.subplot(1, 2, 2)
plt.hist(equalized.ravel(), bins=256, range=(0, 256), color="darkorange", edgecolor="none")
plt.title("Equalized Histogram")
plt.xlabel("Intensity Value (0-255)")
plt.ylabel("Pixel Count")

plt.tight_layout()
plt.show()

# 9. Save the equalized image
Image.fromarray(equalized).save("histogram_equalized_gray.jpg")
print("Saved equalized image to 'histogram_equalized_gray.jpg'")